import asyncio
import websockets
import json
import yaml
from datetime import datetime
from pathlib import Path
import sys
import os

# Configuration Path
CONFIG_PATH = Path(__file__).parent / "config" / "config.yaml"

# Global Stats
stats = {
    "received": 0,
    "saved": 0,
    "errors": 0,
    "reconnections": 0
}

def log(message):
    """Simple Logger"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def load_config():
    """Loads configuration from yaml"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_to_database(crashes):
    """Saves to PostgreSQL using environment variables for safety"""
    if not crashes:
        return 0
    
    try:
        import psycopg2
        
        # Database credentials set via Environment Variables
        # laptop/termux dono pe work karega
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', '5432'),
            database=os.getenv('DATABASE_NAME', 'crash_db'),
            user=os.getenv('DATABASE_USER', 'crash_user'),
            password=os.getenv('DATABASE_PASSWORD', 'your_secure_password_here') # Update this!
        )
        
        cur = conn.cursor()
        saved = 0
        
        for crash in crashes:
            try:
                cur.execute(
                    """
                    INSERT INTO crash_games (game_id, multiplier, timestamp, source)
                    VALUES (%s, %s, %s, 'xbet')
                    ON CONFLICT (game_id) DO NOTHING
                    RETURNING game_id
                    """,
                    (crash['game_id'], crash['multiplier'], crash['timestamp'])
                )
                
                if cur.fetchone():
                    saved += 1
            
            except Exception as e:
                log(f"  ⚠️  Insertion Error {crash['game_id']}: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        return saved
    
    except Exception as e:
        log(f"❌ DB Error: {e}")
        stats['errors'] += 1
        return 0

def build_websocket_url(config):
    """Constructs URL from config"""
    auth = config['authentication']
    ws = config['scraper']['websocket']
    p = ws['params']
    
    return (
        f"{ws['base_url']}?"
        f"ref={p['ref']}&"
        f"gr={p['gr']}&"
        f"whence={p['whence']}&"
        f"fcountry={p['fcountry']}&"
        f"appGuid={p['appGuid']}&"
        f"lng={p['lng']}&"
        f"v={p['v']}&"
        f"access_token={auth['access_token']}"
    )

def get_headers(config):
    """Headers with Session/Token info"""
    auth = config['authentication']
    return {
        "Cookie": f"user_token={auth['user_token']}; SESSION={auth['session']}",
        "Origin": "https://ma-1xbet.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

async def scraper_loop():
    """Main Monitoring Loop"""
    attempt = 0
    max_attempts = 999999
    
    log("="*70)
    log("🔱 KING KASHMIRI - 1XBET CRASH ENGINE")
    log("="*70)
    log("📊 Mode: Real-time PostgreSQL Storage")
    
    while attempt < max_attempts:
        try:
            config = load_config()
            
            if attempt > 0:
                log(f"🔄 Reconnecting (Attempt {attempt})...")
                stats['reconnections'] += 1
                await asyncio.sleep(10)
            
            url = build_websocket_url(config)
            headers = get_headers(config)
            
            async with websockets.connect(url, additional_headers=headers) as ws:
                log("✅ Connected to 1xBet!")
                
                # SignalR Handshake
                await ws.send(json.dumps({"protocol":"json","version":1}) + "\x1e")
                await ws.recv()
                
                # Account Invocation
                account_id = config['authentication']['account_id']
                await ws.send(json.dumps({
                    "arguments": [{"activity": 30, "account": account_id}],
                    "invocationId": "0",
                    "target": "Account",
                    "type": 1
                }) + "\x1e")
                
                await asyncio.sleep(2)
                attempt = 0
                
                while True:
                    try:
                        raw_msg = await asyncio.wait_for(ws.recv(), timeout=60)
                        for frame in raw_msg.strip().split('\x1e'):
                            if not frame: continue
                            
                            data = json.loads(frame)
                            if data.get('type') == 1 and data.get('target') == 'OnCrash':
                                args = data.get('arguments', [])
                                if args:
                                    crash_data = args[0]
                                    stats['received'] += 1
                                    
                                    crash = {
                                        'game_id': str(crash_data.get('l')),
                                        'multiplier': float(crash_data.get('f')),
                                        'timestamp': datetime.fromtimestamp(int(crash_data.get('ts')) / 1000)
                                    }
                                    
                                    log(f"🎲 CRASH #{stats['received']}: {crash['game_id']} @ {crash['multiplier']}x")
                                    saved = save_to_database([crash])
                                    if saved > 0:
                                        stats['saved'] += saved
                            
                            elif data.get('type') == 6: # Keep-alive Ping
                                await ws.send(json.dumps({"type":6}) + "\x1e")
                    
                    except asyncio.TimeoutError:
                        continue
        
        except Exception as e:
            attempt += 1
            log(f"❌ Connection Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    if not CONFIG_PATH.exists():
        log("❌ config/config.yaml missing!")
        sys.exit(1)
    asyncio.run(scraper_loop())
