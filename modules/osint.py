# modules/osint.py

import requests
import shodan
import os
import socket

OUTPUT_FILE = "outputs/osint.txt"

def save_output(data):
    os.makedirs("outputs", exist_ok=True)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except Exception as e:
        msg = f"[!] Erreur de résolution DNS pour {target} : {e}"
        save_output(msg)
        return None

def ipinfo_lookup(ip, config):
    print("[+] Interrogation ipinfo.io")
    token = config.get("ipinfo_token", "")
    try:
        r = requests.get(f"https://ipinfo.io/{ip}?token={token}")
        result = "[IPINFO.IO]\n" + r.text + "\n"
        save_output(result)
        return result
    except Exception as e:
        msg = f"[IPINFO.IO] Erreur : {e}"
        save_output(msg)
        return msg

def ipapi_lookup(ip):
    print("[+] Interrogation ip-api.com")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        result = "[IP-API.COM]\n" + r.text + "\n"
        save_output(result)
        return result
    except Exception as e:
        msg = f"[IP-API.COM] Erreur : {e}"
        save_output(msg)
        return msg

def abuseipdb_lookup(ip, config):
    print("[+] Interrogation abuseipdb.com")
    key = config.get("abuseipdb_key", "")
    try:
        headers = {
            "Key": key,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }
        r = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)
        result = "[ABUSEIPDB.COM]\n" + r.text + "\n"
        save_output(result)
        return result
    except Exception as e:
        msg = f"[ABUSEIPDB.COM] Erreur : {e}"
        save_output(msg)
        return msg

def shodan_lookup(ip, config):
    print("[+] Interrogation shodan.io")
    key = config.get("shodan_key", "")
    try:
        api = shodan.Shodan(key)
        host = api.host(ip)
        result = "[SHODAN.IO]\n"
        result += f"IP: {host['ip_str']}\n"
        result += f"Organisation: {host.get('org', 'N/A')}\n"
        result += f"OS: {host.get('os', 'N/A')}\n"
        for item in host['data']:
            result += f"Port: {item['port']}\n"
            result += f"Banner: {item.get('data', '')[:100]}\n"
        save_output(result)
        return result
    except Exception as e:
        msg = f"[SHODAN.IO] Erreur : {e}"
        save_output(msg)
        return msg

def run(target, config):
    ip = resolve_target(target)
    if not ip:
        return f"[OSINT] Erreur : Impossible de résoudre {target}"

    save_output(f"\n--- OSINT pour {target} ---\n")
    summary = f"\n--- OSINT pour {target} ---\n"

    # Domain name check (whois or direct query possible)
    if not target.replace('.', '').isdigit():
        summary += f"[INFO] Domaine soumis : {target}\n"
        try:
            domain_data = requests.get(f"https://api.hackertarget.com/hostsearch/?q={target}").text
            save_output("[HOSTSEARCH - HACKERTARGET]\n" + domain_data + "\n")
            summary += "[HOSTSEARCH] Résultat ajouté.\n"
        except Exception as e:
            msg = f"[HOSTSEARCH] Erreur : {e}"
            save_output(msg)
            summary += msg + "\n"

    summary += f"\n--- OSINT IP liée : {ip} ---\n"
    summary += ipinfo_lookup(ip, config)
    summary += ipapi_lookup(ip)
    summary += abuseipdb_lookup(ip, config)
    summary += shodan_lookup(ip, config)
    summary += "--- Fin OSINT ---\n"
    return summary
