from cryptography.fernet import Fernet
import base64
import hashlib

class Cryptography:
    def __init__(self):
        self.fernet = None
    
    def initialize(self, password):
        """Initialize encryption with password"""
        # Derive key from password
        key = hashlib.sha256(password.encode()).digest()
        fernet_key = base64.urlsafe_b64encode(key)
        self.fernet = Fernet(fernet_key)
    
    def encrypt(self, plaintext):
        """Encrypt plaintext"""
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext"""
        return self.fernet.decrypt(ciphertext.encode()).decode()