from asyncio import Event
import re
from matrixs import Matrixs
from server import parse_message, create_response
from tables import *
import socket
from update_keys import Update_Keys

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

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)


 

print("UDP server up and listening")

def run_server(matrixs, tables):
    # Create a datagram socket
    global UDPServerSocket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = format(bytesAddressPair[0])

        address = bytesAddressPair[1]
        request = parse_message(message[2:-1])
        handle_request(matrixs, tables, request, address)
        
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)

def handle_request(matrixs, tables, request, address):
    print("Handle request")
    if request.Y == "2":
        pairs_ooids_values = []
        errors = []
        print("Set")
        for (ooid, num) in request.list_args:
            # To generate a key, you must have a number one as value
            if ooid == '3.2.6.0' and int(num) == 1:
                print("Get key :)") 
                key = matrixs.get_key()
                # Convert key to string
                key = list(map(lambda byte : str(byte), key))
                (pair_ooid_value, error) = tables.add_key("|".join(key), request.P, 0)
                # TODO: Depois isto só é feito no fim :)
                response = create_response(request.P,[pair_ooid_value],[])
                UDPServerSocket.sendto(bytes(response, 'utf-8'), address)
                pairs_ooids_values.extend(pair_ooid_value)
                if len(error) > 0:
                    error = (ooid, error)
                errors.extend(error)
            else:
                print("SET NOT ADD KEY")
                (pair_ooid_value, error) = tables.set_values(ooid, num, request.P)
                pairs_ooids_values.extend(pair_ooid_value)
                if len(error) > 0:
                    error = (ooid, error)
                errors.extend(error)
        print("Devolve")
        print(pairs_ooids_values)
        print(errors)
        return
    if request.Y == "1":
        print("Get")
        info_to_response = tables.get_values(request.list_args, request.P)



if __name__ == "__main__":
    print("Olá da main (server)")
    read_file()
    print(params)

    matrixs = Matrixs(params)
    thread = Update_Keys(matrixs, params['T'])
    thread.start()
    tables = Tables(params)
    run_server(matrixs, tables)



