import socket
import argparse
from common import make_string_to_send, parse_message
import sys
sys.path.append('./../security')
import security_functions

def pair(arg):
    return arg.split(',')

def  main_funcion_client(client_identifier, type_request, arg_list):

    serverAddressPort   = ("127.0.0.1", 20001)
    fakeAddress   = ("127.0.1.1", 20102)

    bufferSize          = 1024

    name_file_with_key = f'../client/{client_identifier}.key'
    #name_file_with_key = f'../client/Cli2.key'

    # TODO: Remover segundo argumento para obrigar a inserir password. Password pode ser configurável
    # Está em comentário duas linhas a seguir
    cipher = security_functions.get_cipher(name_file_with_key, client_identifier)
    #cipher = security_functions.get_cipher(name_file_with_key, "Cli2")
    if not cipher:
        quit()

    checksum = security_functions.generate_encrypted_checksum(cipher)


    if type_request == "GET":
        type_request = 1
    elif type_request == "SET":
        type_request = 2
    else:
        Exception("Invalid arg")

    # Identifier of client/reques
    P = -1 

    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Pares")
    print(arg_list)

    request_string = make_string_to_send(client_identifier, str(type_request), arg_list, checksum)


    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytes(request_string, 'utf-8'), serverAddressPort)

    

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    

    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)
    request = parse_message(msg)
    return request

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    #argParser.add_argument("-n", "--number_elements", help="number of elements in list", action="store") 
    argParser.add_argument("-l", "--list", help="number of elements in list",action="store", required=True, type=pair, nargs='+') 
    argParser.add_argument("-r", "--type_request", help="Type of request (GET or SET).", required=True, action="store",choices=['SET', 'GET'],type=str) 
    argParser.add_argument("-id", "--client-identifier", help="Identifier to set keys and haver permissions.", required=True, action="store",type=str) 
    args = argParser.parse_args()
    main_funcion_client(args.client_identifier, args.type_request, args.list)


#def  main_funcion_client(client_identifier, type_request, arg_list):