import pysodium
from base64 import b64encode


class Keys:

    private_wg_key = None
    public_wg_key = None

    def gen_b64_keys(self):
        k = pysodium.crypto_box_keypair()
        self.private_wg_key = b64encode(k[0])
        self.public_wg_key = b64encode(k[1])

    def gen_byte_keys(self):
        k = pysodium.crypto_box_keypair()
        self.private_wg_key = k[0]
        self.public_wg_key = k[1]



