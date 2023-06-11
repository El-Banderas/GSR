
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#pass_from_user = input("Please enter your password")
#password = pass_from_user.encode()

user_password = "pa"
number_clients = 3
users_keys = {}


def convert_password_to_key(password):
    password = password.encode()
    mysalt = b'hC\xd3\xbb\xa5{\xe5\xf5\xa2sS\xfa) \xc9i'

    kdf = PBKDF2HMAC(
    algorithm = hashes.SHA256,
    length=32,
    salt=mysalt,
    iterations=1000000,
    backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

def generate_info(): 

    cipher = convert_password_to_key(user_password)

    # Generate keys
    for i in range(number_clients):
        users_keys[f'Cli{i}'] = Fernet.generate_key()
        users_keys["server"] = Fernet.generate_key()

    print(users_keys)
    
    for user, value in users_keys.items():
        if "server" not in user: 
            with open(f'../client/{user}.key', 'wb') as filekey:
                # If you want to change the password of the file, must change the cipher in next line
                # Choose other word as argument of function
                cipher = convert_password_to_key(user)
                to_write = f"{user}:{value};server:{users_keys['server']}"
                print("Writing to file: " + f'../client/{user}.key')
                print(to_write)
                encrypted_info = cipher.encrypt(to_write.encode())
                filekey.write(encrypted_info)

    with open(f'../server/server.key', 'wb') as filekey:
        to_write = ""
        for user, value in users_keys.items():
            cipher = convert_password_to_key("server")
            to_write = f"{user}:{value};"+to_write
        print("Write to server file")
        print(to_write)
        encrypted_info = cipher.encrypt(to_write.encode())
            #encrypted_info = cipher.encrypt()
        filekey.write(encrypted_info )


    '''
    # key generation
    key_server = Fernet.generate_key()
    
    # string the key in a file
    with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

    '''

if __name__ == "__main__":
    generate_info()