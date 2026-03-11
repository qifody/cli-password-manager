import hashlib
import secrets
import hmac
import base64
import json

from cryptography.fernet import Fernet


# ---------- PASSWORD HASHING ----------

def generate_salt():
    return secrets.token_hex(16)


def hash_password(password, salt):
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    )
    return base64.b64encode(key).decode()


def verify_password(password, stored_hash, salt):
    new_hash = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)


# ---------- KEY DERIVATION ----------

def derive_key(password, salt):
    key_material = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    )
    return base64.urlsafe_b64encode(key_material)


# ---------- ENCRYPT / DECRYPT ----------

def encrypt_data(data, key):
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    token = f.encrypt(json_data)
    return token.decode()


def decrypt_data(token, key):
    f = Fernet(key)
    decrypted = f.decrypt(token.encode())
    return json.loads(decrypted.decode())