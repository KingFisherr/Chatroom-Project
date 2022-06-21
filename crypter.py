from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

#AES (Advanced Encryption Standard)
#note: make sure you use 1 instance of AESCrypter per client connection
#note2: make sure you encrypt/decrypt messages sequentially
# iv = initialization vector 

class AESCrypter:
    def __init__(self):
        self.key = (
            b'\xf4\x77\xe5\x1b\x1c\xf8\x08\x72'
            b'\xaa\xc7\x01\x52\xea\xe4\x76\x86'
            b'\x42\x34\x76\x70\x37\xc0\x55\x83'
            b'\xb9\xb4\xf9\xa5\x1f\x0c\xc0\x70'
        ) # 256 bit key
        self.cipher_send = None
        self.cipher_recv = None
        
    #expects 16 byte IVs
    def init_cipher(self, send_iv, recv_iv):
        self.cipher_send = AES.new(self.key, AES.MODE_OFB, send_iv)
        self.cipher_recv = AES.new(self.key, AES.MODE_OFB, recv_iv)
        
    #takes in a plain text string and returns an encrypted b64 encoded string
    def encrypt_string(self, pt_string):
        #encrypt it
        ct = self.cipher_send.encrypt(pt_string.encode())
        #return b64 version of cipher text
        return b64encode(ct)
        
    #takes in an encrypted and (base)b64 encoded string and returns plain text
    def decrypt_string(self, ct_string_b64):
        #decode b64 encoded to byte string
        ct_b = b64decode(ct_string_b64)
        #decrypt
        pt = self.cipher_recv.decrypt(ct_b)
        #return plain text
        return pt

#this code is just to test the above class
if __name__ == '__main__':
    plain_text = "hello world"

    server_crypter = AESCrypter()
    client_crypter = AESCrypter()
    
    sc_send_iv = get_random_bytes(16)
    sc_recv_iv = get_random_bytes(16)
    
    #server will generate random send and recv ivs
    server_crypter.init_cipher(sc_send_iv, sc_recv_iv)
    #client will receive the random ivs from the server on connect
    client_crypter.init_cipher(sc_recv_iv, sc_send_iv) # servers send iv = clients recv iv and vice versa

    ct_b64 = server_crypter.encrypt_string(plain_text)
    print(ct_b64)
    decrypted_pt = client_crypter.decrypt_string(ct_b64)
    print(decrypted_pt)

    x = server_crypter.encrypt_string("booyah")
    y = client_crypter.decrypt_string(x)
    print(y)
