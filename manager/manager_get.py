import socket
import argparse
from parse_messages import make_string_to_send, parse_message
import random
import sys
sys.path.append('./../security')
import security_functions

socket_max_timeuot = 5

def pair(arg):
    return arg.split(',')

def  main_function_manager(client_identifier, type_request, arg_list):

    serverAddressPort   = ("127.0.0.1", 20001)

    bufferSize          = 1024

    name_file_with_key = f'../manager/{client_identifier}.key'
    #name_file_with_key = f'../client/Cli2.key'

    # TODO: Remover segundo argumento para obrigar a inserir password. Password pode ser configurável
    # Está em comentário duas linhas a seguir
    cipher = security_functions.get_cipher(name_file_with_key, client_identifier)
    #cipher = security_functions.get_cipher(name_file_with_key, "Cli2")
    if not cipher:
        quit()
    # Cipher is now: [client:Key, server:Key]
    cipher_client_server = cipher.split(";")



    if type_request == "GET":
        type_request = 1
    elif type_request == "SET":
        type_request = 2
    else:
        Exception("Invalid arg")

    # Identifier of client/reques
    P = random.randint(10, 5000)
    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(socket_max_timeuot)



    request_string = make_string_to_send(client_identifier, P, str(type_request), arg_list)

    request_encripted = security_functions.generate_encrypted_string(request_string, cipher_client_server[1])
    checksum = security_functions.generate_encrypted_string(request_string, cipher_client_server[0])

    # Send to server using created UDP socket
    final_message = ";".join([client_identifier, request_encripted.decode(), checksum.decode()])
    print("Final message")
    print(final_message)
    UDPClientSocket.sendto(bytes(final_message, 'utf-8'), serverAddressPort)

    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    except TimeoutError:
        print("Maximum waiting time passed. Server not responding, bye...")
        quit()

    

    msg = "Message from Server {}".format(msgFromServer[0])

    msg_string = msgFromServer[0].decode('utf-8')
    if msg_string.count(";") > 3:
        print("Error, agent not encripted message")
        print("Received message:")
        print(msg_string)
        return parse_message(msg_string)
        
    server_id, content_encripted, checksum = msg_string.split(";")
    content_decripted = security_functions.generate_decrypted_string(content_encripted, cipher_client_server[0])
    checksum_decripted = security_functions.generate_decrypted_string(checksum, cipher_client_server[1])
    if checksum_decripted != content_decripted:
        print("Differences")
        print(checksum_decripted )
        print(content_decripted )
        raise Exception("Message not from server")

    print("Message decripted")
    print(content_decripted.decode('utf-8'))
    request = parse_message(content_decripted.decode('utf-8'))
    if int(request.P) != P:
        raise Exception("Request with wrong number!")

    return request

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    #argParser.add_argument("-n", "--number_elements", help="number of elements in list", action="store") 
    argParser.add_argument("-l", "--list", help="number of elements in list",action="store", required=True, type=pair, nargs='+') 
    argParser.add_argument("-r", "--type_request", help="Type of request (GET or SET).", required=True, action="store",choices=['SET', 'GET'],type=str) 
    argParser.add_argument("-id", "--client-identifier", help="Identifier to set keys and haver permissions.", required=True, action="store",type=str) 
    args = argParser.parse_args()
    main_function_manager(args.client_identifier, args.type_request, args.list)


#def  main_funcion_client(client_identifier, type_request, arg_list):