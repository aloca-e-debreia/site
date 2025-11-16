import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

KEY = os.environ.get("AES_SECRET_KEY")

def encrypt_data(data)

	if not data:
			return None

	try:
		return fernet.encrypt_data(data.encode()).decode()

	except Exception:
		return data

def decrypt_data(token):

	if not token:
		return None
	try
		return fernet.decrypt(token.encode()).decode()
	except Exception:
		return token
	