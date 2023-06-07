# From https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/, at 6 june 2023

from cryptography.fernet import Fernet
import json

passwords_client = {
    "passwords":{
    "server" : "aaa",
    "cli1" : "b",
    "cli2" : "safaf",}
}

string_to_encript = json.dumps(passwords_client)


# key generation
key = Fernet.generate_key()
 
# string the key in a file
with open('filekey.key', 'wb') as filekey:
   filekey.write(key)

# using the generated key
fernet = Fernet(key)
 
# opening the original file to encrypt
#with open('input.txt', 'rb') as file:
#    original = file.read()
original = str.encode(string_to_encript)

# encrypting the file
encrypted = fernet.encrypt(original)
 
# opening the file in write mode and
# writing the encrypted data
with open('output.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)