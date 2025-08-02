# modules/crypto_tools.py

import hashlib
import base64
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

OUTPUT_FILE = "outputs/crypto_results.txt"
os.makedirs("outputs", exist_ok=True)

def save_output(data):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def hash_text(text):
    hashes = {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA256": hashlib.sha256(text.encode()).hexdigest()
    }
    result = "[Crypto Tools]\n"
    for k, v in hashes.items():
        result += f"{k}: {v}\n"
    save_output(result)
    return hashes

def aes_encrypt(text):
    key = hashlib.sha256("blackpyreconx".encode()).digest()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    encrypted = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    save_output(f"AES Encrypted: {encrypted}")
    return encrypted
