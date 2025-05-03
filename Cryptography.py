from cryptography.fernet import Fernet
import os
import base64
import hashlib

class Cryptography:
    def __init__(self):
        self.fernet = None
    
    def initialize(self, password, salt=None):
        if salt is None:
            self.password_salt = os.urandom(16)
        else:
            self.password_salt = salt

        password_salted = password.encode() + self.password_salt
        key = hashlib.sha256(password_salted).digest()
        fernet_key = base64.urlsafe_b64encode(key)
        self.fernet = Fernet(fernet_key)

    
    def encrypt(self, plaintext):
        """Encrypt plaintext"""
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext"""
        return self.fernet.decrypt(ciphertext.encode()).decode()