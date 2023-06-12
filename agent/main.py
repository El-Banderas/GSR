from asyncio import Event
import re
from matrixs import Matrixs
from agent.agent import parse_message, create_response, create_error_message
from tables import *
import socket
from update_keys import Update_Keys
from agent.agent_security import Security
import sys
sys.path.append('./../security')
import security_functions


default_file = "./input.txt"

params = {}

def read_file():
    pattern = re.compile("(\w)=(.+)$")
    for i, line in enumerate(open(default_file)):
        result = re.search(pattern, line)
        if result.group(1) == "M":
            params[result.group(1)] = result.group(2)
        else:
            params[result.group(1)] = int(result.group(2))


# Server info
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

class Main_Server:

    def __init__(self, params):
        self.matrixs = Matrixs(params)
        thread = Update_Keys(self.matrixs, params['T'])
        thread.start()
        self.tables = Tables(params)
        self.security = Security() 

    # Gets the message to send and encripts, appending in the end the checksum.
    def get_bytes_to_send(self, message, client_id):
            response_encr = security_functions.encript_string(message, self.security.get_fernet_client(client_id))
            checksum = security_functions.encript_string(message, self.security.get_fernet_client("server"))
            return ";".join(["server", response_encr.decode('utf-8'), checksum.decode('utf-8')]).encode()


    def run_server(self):
        # Create a datagram socket
        global UDPServerSocket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((localIP, localPort))
        while(True):

            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

            message = format(bytesAddressPair[0])[2:-1]

            address = bytesAddressPair[1]
            requestor_message_checksum = message.split(";")
            fernet_client = self.security.get_fernet_client("server")
            message_decoded = security_functions.decript_message(requestor_message_checksum[1], fernet_client)
            valid = self.security.verify_checksum(requestor_message_checksum[0], 
                                                   message_decoded,
                                                   requestor_message_checksum[2])
            if valid:
                request = parse_message(message_decoded.decode('utf-8'))
                (ooids_and_values, errors) = self.handle_request(request)
                str_to_send = create_response(request.P, ooids_and_values, errors)
                bytes_to_send = self.get_bytes_to_send(str_to_send, request.client_id)

                # Sending a reply to client
                UDPServerSocket.sendto(bytes_to_send, address)
            else:
                message_string = message_decoded.decode('utf-8')
                client_id = message_string.split(";")[0]
                str_to_send = create_error_message(client_id,7)
                bytes_to_send = ";".join(["server", str_to_send])
                UDPServerSocket.sendto(bytes_to_send.encode(), address)

    def handle_request(self, request):
        print("Handle request")
        if request.Y == "2":
            pairs_ooids_values = []
            errors = []
            for (ooid, num) in request.list_args:
                # To generate a key, you must have a number one as value
                if ooid == '3.2.6.0':
                    print("Get key") 
                    key = self.matrixs.get_key()
                    # Convert key to string
                    key = list(map(lambda byte : str(byte), key))
                    (pair_ooid_value, error) = self.tables.add_key("|".join(key), request.client_id, int(num))
                    if len(pair_ooid_value) > 0:
                        pairs_ooids_values.extend(pair_ooid_value)
                    if len(error) > 0:
                        error = (str(ooid), str(error))
                        errors.append(error)
                else:
                    (pair_ooid_value, error) = self.tables.set_values(ooid, num, request.client_id)
                    if len(pair_ooid_value) > 0:
                        pairs_ooids_values.append(pair_ooid_value)
                    if len(error) > 0:
                        error = (ooid, error)
                        errors.append(error)
            return (pairs_ooids_values, errors)
        if request.Y == "1":
            return self.tables.get_values(request.list_args, request.client_id)



if __name__ == "__main__":
    print("Server starting...")
    read_file()
    print(params)
    main_server = Main_Server(params) 
    
    main_server.run_server()



