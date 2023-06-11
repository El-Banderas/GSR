from cryptography.fernet import Fernet
from generate_security_info import convert_password_to_key
from cryptography.fernet import InvalidToken
from base64 import urlsafe_b64encode


#password = input("Insert password, please: ")
#fernet = convert_password_to_key(password)

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
        print("Wrong key")
        return None

# When fernet is still in file, not converted to object
def generate_encrypted_string(string, fernet):
    fernet_clean = bytes(fernet.split(":")[1],'utf-8')
    #ai = urlsafe_b64encode(fernet_clean)
    fernet_to_decript = Fernet(fernet_clean[2:-1])
    return fernet_to_decript.encrypt(string.encode())

def generate_decrypted_string(string, fernet):
    fernet_clean = bytes(fernet.split(":")[1],'utf-8')
    #ai = urlsafe_b64encode(fernet_clean)
    fernet_to_decript = Fernet(fernet_clean[2:-1])
    return fernet_to_decript.decrypt(string.encode())


def encript_string(string, fernet_object):
    return fernet_object.encrypt(string.encode())


def decript_message(message, fernet):
    return fernet.decrypt(message.encode())

def decript_bytes(message, fernet):
    return fernet.decrypt(message)
