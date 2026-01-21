import time
import asyncio
from django.core.management.base import BaseCommand
from stock_price.services.kis_rest_client import kis_rest_client
from stock_theme.services.sync_service import ThemeSyncService

class Command(BaseCommand):
    help = 'Runs the background worker for Real-time Theme Synchronization'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Real-time Theme Sync Worker... 🚀'))
        
        sync_service = ThemeSyncService()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.run_loop(sync_service))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nStopping Sync Worker...'))
        finally:
            loop.close()

    async def run_loop(self, sync_service):
        while True:
            # Market Time Check (09:00 ~ 15:30 + Buffer, Weekdays)
            from datetime import datetime
            now = datetime.now()
            
            # 주말(5=토, 6=일)이거나 09:00 이전, 16:00 이후면 휴식
            # (장 마감 후 조금 여유있게 16시까지는 수집 허용한다고 가정, 또는 사용자 요청대로 즉시 sleep)
            # 보통 장 종료 후 15:40~50분까지는 순위 확정될 수 있으므로 16시로 설정
            # 사용자 요청: "장이 종료되면" -> 15:30 이후
            is_weekend = now.weekday() >= 5
            is_market_open = 9 <= now.hour < 16 # 09:00 ~ 15:59 (simple check for now)
            
            # 더 정밀한 시간 체크 (09:00 ~ 15:30)
            current_time = now.time()
            start_time_limit = datetime.strptime("09:00:00", "%H:%M:%S").time()
            end_time_limit = datetime.strptime("15:30:00", "%H:%M:%S").time() # 정규장 종료
            
            in_operating_hours = start_time_limit <= current_time <= end_time_limit

            if is_weekend or not in_operating_hours:
                self.stdout.write(f"[{now.strftime('%H:%M:%S')}] Market Closed. Sleeping for 5 minutes... 🌙")
                await asyncio.sleep(300) # 5분 대기
                continue

            try:
                # 1. Fetch Current Ranking
                start_time = time.time()
                self.stdout.write(f"[{time.strftime('%H:%M:%S')}] Fetching Ranking API...", ending='')
                
                # KIS API Call (Async)
                ranks = await kis_rest_client.get_fluctuation_rank()
                
                if not ranks:
                    self.stdout.write(self.style.WARNING(" Empty Data (Market Closed or Error)"))
                else:
                    self.stdout.write(self.style.SUCCESS(f" OK ({len(ranks)} items)"))
                    
                    # 2. Detect & Process Changes (Incremental Analysis)
                    # 이 메서드 내부에서 Redis Diff -> LLM Analysis -> DB Save -> Cache Update 수행
                    processed = await sync_service.detect_and_process_changes(ranks)
                    
                    if processed:
                        self.stdout.write(self.style.SUCCESS(f"   -> New Entrants Processed: {processed}"))
                        # TODO: WebSocket Notification Trigger here (Optional if DB signals not used)
                    else:
                        self.stdout.write("   -> No changes or new entrants.")

                # 3. Wait for next cycle (e.g., 60 seconds)
                elapsed = time.time() - start_time
                wait_time = max(10, 60 - elapsed) # Ensure at least 60s interval
                await asyncio.sleep(wait_time)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\nError in sync loop: {e}"))
                await asyncio.sleep(10) # Error backoff
