import socket
import os
import platform
import subprocess
from datetime import datetime

OUTPUT_FILE = "outputs/scan_results.txt"

TOP_PORTS = [
    21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 123, 135, 137, 138, 139,
    143, 161, 162, 179, 389, 443, 445, 465, 514, 515, 587, 593, 636, 993, 995,
    1025, 1080, 1433, 1723, 2049, 2121, 3128, 3306, 3389, 5060, 5432, 5900,
    5938, 6000, 6667, 8000, 8008, 8080, 8443, 8888, 9000
]

PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 67: "DHCP",
    68: "DHCP", 69: "TFTP", 80: "HTTP", 110: "POP3", 111: "RPCbind",
    123: "NTP", 135: "RPC", 137: "NetBIOS", 138: "NetBIOS", 139: "SMB",
    143: "IMAP", 161: "SNMP", 162: "SNMP Trap", 179: "BGP", 389: "LDAP",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "Syslog", 515: "LPD",
    587: "SMTP", 593: "RPC", 636: "LDAPS", 993: "IMAPS", 995: "POP3S",
    1025: "Windows DCOM", 1080: "SOCKS Proxy", 1433: "MSSQL", 1723: "PPTP",
    2049: "NFS", 2121: "FTP", 3128: "Squid Proxy", 3306: "MySQL",
    3389: "RDP", 5060: "SIP", 5432: "PostgreSQL", 5900: "VNC",
    5938: "TeamViewer", 6000: "X11", 6667: "IRC", 8000: "HTTP-Alt",
    8008: "HTTP-Alt", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
    8888: "Alternate HTTP", 9000: "UDPCast"
}

def save_output(data):
    os.makedirs("outputs", exist_ok=True)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except Exception as e:
        return None

def detect_os_ttl(ip):
    print("[*] Détection de l’OS via TTL...")
    result = ""
    try:
        if platform.system().lower() == "windows":
            ping = subprocess.check_output(["ping", "-n", "1", ip]).decode()
        else:
            ping = subprocess.check_output(["ping", "-c", "1", ip]).decode()

        for line in ping.split("\n"):
            if "ttl" in line.lower():
                ttl = int(line.lower().split("ttl=")[1].split()[0])
                if ttl >= 128:
                    os_guess = "Windows"
                elif ttl >= 64:
                    os_guess = "Linux/Unix"
                else:
                    os_guess = "Inconnu"
                result = f"[TTL] Estimation OS : {os_guess} (TTL={ttl})\n"
                break
    except Exception as e:
        result = f"[TTL] Erreur : {e}\n"
    save_output(result)
    return result

def banner_grab(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((ip, port))

            # Envoie spécifique selon port
            if port in [80, 8080, 8000, 8008, 8888, 8443]:
                s.send(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())
            elif port == 25:
                s.send(b"EHLO scanner\r\n")

            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner if banner else "Aucune bannière reçue"
    except:
        return "Pas de bannière"

def scan_ports(ip):
    open_ports = []
    result = "[*] Scan des ports TCP...\n"
    for port in TOP_PORTS:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip, port))
            open_ports.append(port)
            banner = banner_grab(ip, port)
            service = PORT_NAMES.get(port, "Inconnu")
            entry = f"[PORT OUVERT] {port} ({service}): {banner}\n"
            save_output(entry)
            result += entry
            s.close()
        except:
            pass
    return open_ports, result

def draw_ascii_ports(open_ports):
    result = "\n--- ASCII des ports ouverts (0-1024) ---\n"
    line = ""
    for i in range(0, 1025):
        line += "|" if i in open_ports else "."
        if i % 64 == 0 and i > 0:
            result += line + "\n"
            line = ""
    if line:
        result += line + "\n"
    result += "----------------------------------------\n"
    save_output(result)
    return result

def run(target):
    ip = resolve_target(target)
    if not ip:
        return f"[!] Impossible de résoudre la cible : {target}"

    result = f"\n--- SCAN pour {target} ({ip}) ---\n"
    result += f"Date : {datetime.now()}\n"
    result += detect_os_ttl(ip)
    open_ports, ports_result = scan_ports(ip)
    result += ports_result
    result += draw_ascii_ports(open_ports)
    result += "--- Fin SCAN ---\n"
    return result
