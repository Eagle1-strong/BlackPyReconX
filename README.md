# 🕷️ BlackPyReconX

> Un outil d'audit et de reconnaissance offensif complet en Python, avec interface Telegram intégrée !

---

## ⚙️ Fonctionnalités principales

| Module          | Description |
|-----------------|-------------|
|  OSINT         | Recherches publiques sur IP/domaine (ipinfo, ip-api, abuseIPDB, Shodan) |
|  Scanner       | Scan de ports + détection OS via TTL + banner grabbing |
|  Web Exploit   | Détection de vulnérabilités basiques (XSS, SQLi, LFI) |
|  System Exploit | Reverse shell, keylogger, screenshot, webcam |
|  Persistance   | Ajout/suppression clé registre Windows |
|  Exfiltration  | Archive des données + envoi via Telegram |
|  Rapport       | Génération automatique en `.html`, `.pdf` et `.txt` |
|  Bot Telegram  | Interface Telegram interactive avec boutons & retour des résultats |

---

## 🛠️ Installation

1. Clone le dépôt :
```bash
git clone https://github.com/Eagle1-strong/BlackPyReconX.git
cd BlackPyReconX

Créer un environnement virtuel:

python -m venv venv
venv\Scripts\activate  # Windows

Installer les dépendances:
pip install -r requirements.txt

Interface Telegram:
python main.py --bot

Ligne de commande :
exemple: python main.py --target 187.15.224.50 --osint --scan --report

Avertissement légal:
BlackPyReconX est un outil d’audit à usage pédagogique et professionnel uniquement. Toute utilisation non autorisée contre des systèmes tiers est strictement interdite. Vous êtes seul responsable de son usage.
