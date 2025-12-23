import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.kis_auth import get_current_price

print("--- Fetching Data for 005930 ---")
data = get_current_price("005930")

if data:
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print("Failed to fetch data")
