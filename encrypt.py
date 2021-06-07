import hashlib, binascii
from Crypto.Protocol.KDF import scrypt
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import os
import glob

class Encrypt:
    key=""
    def __init__(self, folder=".\\profiles"):
        self.folder=folder
        self.passwordf=folder+"\\password"
        if not os.path.exists(folder):
            os.mkdir(folder)

    def create_password(self, password):
        f = open(self.passwordf, "w")
        hashd=self.hash_password(password)
        written = hashd[:160]  # hash used for authentification
        self.key = hashd[160:]  # key used for encryption
        f.write(written)
        f.close()
    def hash_password(self,password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        # pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
        key = scrypt(password.encode('utf-8'), salt, 64, N=2 ** 20, r=8, p=1)
        key = binascii.hexlify(key)
        # pwdhash = binascii.hexlify(pwdhash)
        return (salt + key).decode('ascii')

    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user"""
        try:
            f = open(self.passwordf, "r")
            stored_hash = f.read()
            f.close()
        except Exception as e:
            print(e)
            return 0
        salt = stored_hash[:64]
        stored_password = stored_hash[64:]
        key = scrypt(provided_password.encode('utf-8'), salt, 64, N=2 ** 20, r=8, p=1)
        pwdhash = binascii.hexlify(key).decode('ascii')
        if pwdhash[:96] == stored_password:
            self.key=pwdhash[96:]
            return True
        else:
            return False

    def decrypt_files(self, destinationf):
        for f in glob.glob(self.folder + "\\*.enc"):
            file=open(f, 'r')
            dump=file.read()
            b64 = json.loads(dump)
            file.close()
            nonce = b64decode(b64['nonce'])
            ct = b64decode(b64['ciphertext'])
            cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CTR, nonce=nonce)
            pt = cipher.decrypt(ct)
            pt=pt.decode()
            name=f.rsplit('.', 1)[0].rsplit('\\', 1)[1]
            with open(destinationf+"\\"+name+".xml", 'w') as outfile:
                outfile.write(pt)

    def encrypt_files(self, sourcef, form="\\*.xml"):
        for f in glob.glob(sourcef+ form):
            file = open(f)
            txt = file.read()
            file.close()
            cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CTR)
            ct_bytes = cipher.encrypt(txt.encode('utf-8'))
            nonce = b64encode(cipher.nonce).decode('utf-8')
            ct = b64encode(ct_bytes).decode('utf-8')
            name=f.rsplit('.', 1)[0].rsplit('\\', 1)[1]
            with open(self.folder+"\\"+name+".enc", 'w') as outfile:
                json.dump({'nonce':nonce, 'ciphertext':ct}, outfile)

    def remove_crypted_files(self):
        for f in glob.glob(self.folder + "\\*.enc"):
            os.remove(f)
