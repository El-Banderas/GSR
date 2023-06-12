
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import sys
sys.path.append('./../security')
import security_functions

class Security:  

    '''
    Gets the keys from the encripted file, and stores in the keys dictionary.
    First, we decript the file, that has each key separated by ";".
    After, we store in keys dictionary all the keys associated with each entity (client and server). 
    '''
    def __init__(self):
        name_file_with_key = f'../server/server.key'

        # TODO: Remover segundo argumento para obrigar a inserir password. Password pode ser configurável
        # Está em comentário duas linhas a seguir
        ciphers = security_functions.get_cipher(name_file_with_key, "server")
        #cipher = security_functions.get_cipher(name_file_with_key)
        if not ciphers:
            quit()

        self.keys = {}
        keys_splitted =ciphers.split(";")
        print("Reading security files")
        for key in keys_splitted:
            if ":" in key:
                line = key.split(":")
                self.keys[line[0]] = line[1]

    '''
    This function receives de client id, the message decoded, and checksum.
    Then, decripts the checksum with the client key, and compares to the message decripted.
    '''
    def verify_checksum(self, client, message, checksum):
        if client in self.keys:
            fernet_bytes = bytes(self.keys[client],'utf-8')[2:-1]
            fernet_to_decript = Fernet(fernet_bytes)
            decripted = security_functions.decript_message(checksum, fernet_to_decript)
            return decripted == message
        return False
    '''
    This function receives de client id, and the checksum, and verifies if the checksum is associated with the client key.
    '''
    def get_fernet_client(self, client):
        if client in self.keys:
            return Fernet(bytes(self.keys[client],'utf-8')[2:-1])
        return None


