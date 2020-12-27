import pysodium
from base64 import b64encode, b64decode

private_key = pysodium.crypto_box_keypair()
public_key = pysodium.crypto_box_keypair()

print("Private Key:", private_key)
print("Public Key:", b64encode(public_key[0]), b64encode(public_key[1]))
