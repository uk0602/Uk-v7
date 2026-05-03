import os
import re
import sys
from pathlib import Path

# Colors for terminal
class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

def log(icon, message, color=Colors.END):
    print(f"{color}{icon} {message}{Colors.END}")

def main():
    print(f"{Colors.CYAN}{'='*70}")
    print(f"  🔐 VÉRIFICATION DE SÉCURITÉ (KING KASHMIRI)")
    print(f"{'='*70}{Colors.END}\n")

    all_good = True

    # 1. Vérifier .gitignore
    log("1️⃣", "Vérification du .gitignore...", Colors.YELLOW)
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        checks = {
            "config/config.yaml": "config/config\\.yaml",
            ".env": "\\.env",
            "*.log": "\\*\\.log"
        }
        for label, pattern in checks.items():
            if re.search(pattern, content):
                log("   ✅", f"{label} est ignoré", Colors.GREEN)
            else:
                log("   ❌", f"{label} N'EST PAS ignoré", Colors.RED)
                all_good = False
    else:
        log("   ❌", ".gitignore manquant", Colors.RED)
        all_good = False

    print("")

    # 2. Vérifier config.yaml.example
    log("2️⃣", "Vérification du config.yaml.example...", Colors.YELLOW)
    example_path = Path("config/config.yaml.example")
    if example_path.exists():
        log("   ✅", "config.yaml.example présent", Colors.GREEN)
        content = example_path.read_text()
        if "VOTRE_" in content:
            log("   ✅", "Contient des placeholders génériques", Colors.GREEN)
        else:
            log("   ⚠️ ", "Vérifiez que les valeurs sont génériques", Colors.YELLOW)
    else:
        log("   ❌", "config.yaml.example manquant", Colors.RED)
        all_good = False

    print("")

    # 3. Vérifier config.yaml (local)
    log("3️⃣", "Vérification du config.yaml (local)...", Colors.YELLOW)
    config_path = Path("config/config.yaml")
    if config_path.exists():
        log("   ✅", "config.yaml existe (local)", Colors.GREEN)
        content = config_path.read_text()
        if "VOTRE_" in content:
            log("   ⚠️ ", "config.yaml contient encore des placeholders", Colors.YELLOW)
        else:
            log("   ✅", "config.yaml configuré avec vos tokens", Colors.GREEN)
    else:
        log("   ⚠️ ", "config.yaml n'existe pas encore", Colors.YELLOW)

    print("")

    # 4. Vérifier les fichiers sensibles (JWT, IDs)
    log("4️⃣", "Recherche de fichiers sensibles...", Colors.YELLOW)
    sensitive_patterns = [
        r"eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*",
        r"[0-9]{9,}",
        r"[a-f0-9]{32}"
    ]
    sensitive_files = []
    for p in Path(".").rglob("*"):
        if p.suffix in [".py", ".md", ".txt"] and not any(x in str(p) for x in ["venv", ".git", "__pycache__"]):
            content = p.read_text(errors='ignore')
            for pattern in sensitive_patterns:
                if re.search(pattern, content):
                    if not any(x in p.name for x in ["README", "DOCKER", "GITHUB", "CHECKLIST", "example"]):
                        sensitive_files.append(p.name)
                        break
    
    if not sensitive_files:
        log("   ✅", "Aucun fichier sensible détecté", Colors.GREEN)
    else:
        for f in set(sensitive_files):
            log("   ⚠️ ", f"Fichier potentiellement sensible: {f}", Colors.YELLOW)

    print(f"\n{Colors.CYAN}{'='*70}")
    if all_good:
        log("✅", "TOUT EST BON! Prêt pour GitHub.", Colors.GREEN)
    else:
        log("❌", "PROBLÈMES DÉTECTÉS! Corrigez avant de publier.", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
