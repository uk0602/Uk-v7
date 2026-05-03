"""
King Kashmiri - Token Updater
- Extracts access_token from WebSocket URL
- Updates config.yaml automatically
"""
import yaml
import re
from pathlib import Path
import sys
import os

# Configuration path set karein
CONFIG_PATH = Path("config/config.yaml")

def extract_token_from_url(ws_url: str) -> str:
    """URL se token nikalne wala logic"""
    match = re.search(r'access_token=([^&\s]+)', ws_url)
    if match:
        return match.group(1)
    return None

def update_config(new_token: str):
    """config.yaml mein naya token save karein"""
    if not CONFIG_PATH.exists():
        # Agar file nahi hai toh basic structure ke saath bana dega
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_config = {'authentication': {'access_token': ''}}
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f)
    
    # Purani config load karein
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {'authentication': {}}
    
    # Token update karein
    if 'authentication' not in config:
        config['authentication'] = {}
    config['authentication']['access_token'] = new_token
    
    # Save karein
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print("✅ [SUCCESS] Token updated in config/config.yaml")

def main():
    print("="*60)
    print("🔱 KING KASHMIRI - TOKEN UPDATER")
    print("="*60)
    print("\n1. Go to: 1xBet Crash Game")
    print("2. DevTools > Network > WS")
    print("3. Copy Request URL from 'crash?ref='")
    
    ws_url = input("\nCollez l'URL WebSocket complète (Paste URL): ").strip()
    
    if not ws_url:
        print("❌ URL empty!")
        sys.exit(1)
    
    token = extract_token_from_url(ws_url)
    
    if not token:
        print("❌ Token not found in URL!")
        sys.exit(1)
    
    try:
        update_config(token)
        print(f"\n✅ Token Extracted (First 20 chars): {token[:20]}...")
        
        # JWT info (Optional: Requires pip install PyJWT)
        try:
            import jwt
            from datetime import datetime
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            if exp:
                print(f"🕒 Expires at: {datetime.fromtimestamp(exp)}")
        except ImportError:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
