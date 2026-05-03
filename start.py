"""
King Kashmiri - Master Launcher
Lancement du scraper (Background) + Streamlit Dashboard
"""
import subprocess
import time
import sys
import os
from pathlib import Path

def log_header():
    print("="*60)
    print("🔱 KING KASHMIRI - SYSTEM CONTROL CENTER")
    print("="*60)

def check_requirements():
    """Zaruri settings check karein"""
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        print("❌ [ERROR] config/config.yaml not found!")
        print("➡️  Please create config first.")
        sys.exit(1)
    return config_path

def main():
    log_header()
    config_path = check_requirements()
    
    # 1. Database Connection Check
    print("🔍 Checking Database Connection...")
    try:
        import psycopg2
        # Docker ya Env variables ko priority dega
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', '5432'),
            database=os.getenv('DATABASE_NAME', 'crash_db'),
            user=os.getenv('DATABASE_USER', 'crash_user'),
            password=os.getenv('DATABASE_PASSWORD', 'your_password')
        )
        conn.close()
        print("✅ Database: CONNECTED")
    except Exception as e:
        print(f"❌ [DB ERROR]: {e}")
        print("➡️  Make sure PostgreSQL is running.")
        sys.exit(1)

    # 2. Launch Scraper in Background
    print("\n🚀 Launching Scraper Engine...")
    try:
        # Aapki scraper file ka naam 'app.py' ya 'run_scraper.py' ho sakta hai
        scraper_file = "app.py" 
        scraper_process = subprocess.Popen(
            [sys.executable, scraper_file],
            stdout=subprocess.DEVNULL, # Logs ko saaf rakhne ke liye background mein
            stderr=subprocess.PIPE
        )
        print(f"✅ Engine Started (PID: {scraper_process.pid})")
    except Exception as e:
        print(f"❌ Launch Failed: {e}")
        sys.exit(1)

    print("\n⏳ Initializing System (5s)...")
    time.sleep(5)

    # 3. Launch Dashboard
    print("\n🌐 Opening Streamlit Dashboard...")
    print("➡️  Access at: http://localhost:8051")
    print("="*60)
    print("💡 TO STOP:")
    print(f"   - Kill Scraper: taskkill /F /PID {scraper_process.pid} (Windows)")
    print(f"   - Kill Dashboard: Press Ctrl+C in this terminal")
    print("="*60)

    try:
        # Dashboard file ka sahi path check karein
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "dashboard/realtime_app.py",
            "--server.port", "8051"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard Stopped.")
        print(f"⚠️  Note: Scraper is still running in background (PID: {scraper_process.pid})")

if __name__ == "__main__":
    main()
