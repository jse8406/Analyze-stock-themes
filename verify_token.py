import sys
import os

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.kis_auth import get_access_token

print("--- Starting Verification ---")
# This should load from cache if available
token = get_access_token()
if token:
    print(f"Token Retrieved. Expiry: {token.get('access_token_token_expired')}")
else:
    print("Failed to retrieve token")
