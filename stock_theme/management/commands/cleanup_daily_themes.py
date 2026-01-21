from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from datetime import date
from stock_theme.models import Theme, ThemeStock

class Command(BaseCommand):
    help = 'Cleans up duplicate themes and stock entries for the current day'

    def handle(self, *args, **options):
        today = date.today()
        self.stdout.write(f"Starting cleanup for {today}...")

        with transaction.atomic():
            # 1. Merge Duplicate Themes (Same Name)
            # Find names that appear more than once
            duplicates = Theme.objects.filter(date=today).values('name').annotate(count=Count('id')).filter(count__gt=1)
            
            for dup in duplicates:
                name = dup['name']
                themes = list(Theme.objects.filter(date=today, name=name).order_by('created_at'))
                
                # Keep the first one (master)
                master = themes[0]
                others = themes[1:]
                
                self.stdout.write(f"Merging {len(others)} duplicate themes for '{name}' into ID {master.id}")
                
                for other in others:
                    # Move stocks to master
                    for item in other.stocks.all():
                        # Check if master already has this stock
                        if not master.stocks.filter(stock=item.stock).exists():
                            item.theme = master
                            item.save()
                        else:
                            # If master already has it, just delete the duplicate entry
                            item.delete()
                    
                    # Delete the duplicate theme
                    other.delete()

            # 2. Strict Stock Deduplication (One Stock = One Theme per Day)
            # Find stocks that are in multiple themes today
            dup_stocks = ThemeStock.objects.filter(theme__date=today).values('stock').annotate(cnt=Count('id')).filter(cnt__gt=1)
            
            for d in dup_stocks:
                stock_id = d['stock']
                # Get all entries for this stock today
                entries = list(ThemeStock.objects.filter(theme__date=today, stock_id=stock_id).order_by('theme__created_at'))
                
                # Logic: Keep the one in the theme that has the MOST stocks (likely the major theme), or just the first one.
                # Here we just keep the first one created and delete others.
                
                keep = entries[0]
                remove = entries[1:]
                
                for r in remove:
                    self.stdout.write(f"Removing duplicate stock {r.stock.short_code} from extra theme '{r.theme.name}' (Keeping in '{keep.theme.name}')")
                    r.delete()
                    
                    # If the theme becomes empty, delete the theme too?
                    if r.theme.stocks.count() == 0:
                         self.stdout.write(f"Theme '{r.theme.name}' is now empty. Deleting.")
                         r.theme.delete()

        self.stdout.write(self.style.SUCCESS("Deep Cleanup completed."))
