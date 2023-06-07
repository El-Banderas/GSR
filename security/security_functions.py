from cryptography.fernet import Fernet
from generate_security_info import convert_password_to_key
from cryptography.fernet import InvalidToken
from base64 import urlsafe_b64encode


#password = input("Insert password, please: ")
#fernet = convert_password_to_key(password)

checksum = "CHECKSUM"

#with open('../client/Cli0.key', 'rb') as file:
#    key = file.read()
# using the key
 
# opening the encrypted file
#with open('output.txt', 'rb') as enc_file:
def get_cipher(path_to_file, password=None):
    if not password:
        password = input("Insert password, please: ")
    fernet = convert_password_to_key(password)
    with open(path_to_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    # decrypting the file
    try:
        decrypted = fernet.decrypt(encrypted)
        normal_string = decrypted.decode('utf-8')
        return (normal_string)
    except InvalidToken:
        print("Chave errada")
        return None

def generate_encrypted_checksum(fernet):
    fernet_clean = bytes(fernet.split(":")[1],'utf-8')
    #ai = urlsafe_b64encode(fernet_clean)
    print("Fernet clean")
    print(fernet_clean[2:-1])
    fernet_to_decript = Fernet(fernet_clean[2:-1])
    return fernet_to_decript.encrypt(checksum.encode())

def verify_checksum_with_fernet(encripted_checksum, fernet):
    try:
        checksum_decoded = fernet.decrypt(encripted_checksum.encode())
        print("Checksume decoded")
        print(checksum_decoded.decode())
        if checksum_decoded.decode() == checksum:
            return True
        else:
            return False
    except InvalidToken:
        print("Invalid checksum")
        return False