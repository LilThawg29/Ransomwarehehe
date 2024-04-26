import rsa

# Generate attacker RSA keypair
pubkey, privkey = rsa.newkeys(4096) 

# Export attacker public key to PEM format
public_key = pubkey.save_pkcs1().decode()
with open('attacker_public_key.pem', 'w') as f:
    f.write(public_key)
    
# Export attacker private key to PEM format    
private_key = privkey.save_pkcs1().decode()
with open('attacker_private_key.pem', 'w') as f:
    f.write(private_key)