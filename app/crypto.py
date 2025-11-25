from cryptography.fernet import Fernet

fernet = None

def init_fernet(app):
    global fernet
    key = app.config.get("FERNET_KEY")
    if not key:
        raise RuntimeError("FERNET_KEY or FERNET_KEYS não configurado")
    fernet = Fernet(key)

def get_fernet():
    if fernet is None:
        raise RuntimeError("Fernet não inicializado. Chame init_fernet(app) no factory.")
    return fernet

def encrypt_data(data:str):
    if not isinstance(data, str):
        return None
    try:
        fernet = get_fernet()
        return fernet.encrypt(data.encode()).decode()
    except Exception as e:
        print(f"Erro ao criptografar o dado {data}: {e}")
        return data

def decrypt_data(token:str):
    if not isinstance(token, str):
        return None
    try:
        fernet = get_fernet()
        return fernet.decrypt(token.encode()).decode()
    except Exception as e:
        print(f"Erro ao descriptografar o token {token}: {e}")
        return token
