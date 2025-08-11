import os
import json
from cryptography.fernet import Fernet

CONFIG_FILE = 'config.json'
TOKEN_FILE = 'token.enc'
KEY_FILE = 'secret.key'

def generate_key():
    """Generate a key for encryption and save it."""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_token(token):
    key = load_key()
    f = Fernet(key)
    encrypted = f.encrypt(token.encode())
    with open(TOKEN_FILE, 'wb') as token_file:
        token_file.write(encrypted)

def decrypt_token():
    key = load_key()
    f = Fernet(key)
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'rb') as token_file:
        encrypted = token_file.read()
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()

def save_config(config_data):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

if __name__ == '__main__':
    # Example usage
    config = {
        "github_repo": "user/repo",
        "user_name": "username"
    }
    save_config(config)
    token = "your_github_token_here"
    encrypt_token(token)
    print("Config and token saved securely.")
