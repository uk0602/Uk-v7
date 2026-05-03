"""
🔱 KING KASHMIRI - SECURITY GUARD
GitHub par upload karne se pehle ise zaroor chalaein!
"""
import os
import re
from pathlib import Path

def log(step, message, status="info"):
    colors = {"ok": "✅", "error": "❌", "warn": "⚠️", "info": "ℹ️"}
    print(f"{step} {colors.get(status, '•')} {message}")

def run_check():
    print("="*60)
    print("  🔐 SECURITY CHECK: KING KASHMIRI PROJECT")
    print("="*60)
    
    is_safe = True

    # 1. .gitignore Check
    log("1️⃣", "Checking .gitignore...")
    if Path(".gitignore").exists():
        content = Path(".gitignore").read_text()
        for file in ["config/config.yaml", ".env", "*.log"]:
            if file in content:
                log("  ", f"{file} is ignored.", "ok")
            else:
                log("  ", f"{file} IS EXPOSED! Add it to .gitignore.", "error")
                is_safe = False
    else:
        log("  ", ".gitignore missing!", "error")
        is_safe = False

    # 2. Template Check
    print("\n2️⃣ Checking Template Files...")
    templates = ["config/config.yaml.example", ".env.example"]
    for t in templates:
        if Path(t).exists():
            log("  ", f"{t} found.", "ok")
        else:
            log("  ", f"{t} is missing! Create it for others to use.", "warn")

    # 3. Sensitive Data Scanner
    print("\n3️⃣ Scanning for leaked Secrets (JWT/Tokens)...")
    secret_patterns = [
        r"eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*", # JWT
        r"access_token\s*:\s*['\"].+['\"]" # Hardcoded tokens
    ]
    
    found_leak = False
    for p in Path(".").rglob("*.py"):
        if "venv" in str(p) or ".git" in str(p): continue
        content = p.read_text(errors="ignore")
        for pattern in secret_patterns:
            if re.search(pattern, content) and "example" not in str(p):
                log("  ", f"DANGER: Potential secret in {p}", "error")
                found_leak = True
                is_safe = False
    
    if not found_leak:
        log("  ", "No hardcoded secrets found in Python files.", "ok")

    print("\n" + "="*60)
    if is_safe:
        print("✅ RESULT: All Clear! Safe to Push to GitHub.")
    else:
        print("❌ RESULT: Security Risks Found! Fix them before pushing.")
    print("="*60)

if __name__ == "__main__":
    run_check()
