import socket
import argparse
from common import make_string_to_send


def pair(arg):
    return arg.split(',')

argParser = argparse.ArgumentParser()
#argParser.add_argument("-n", "--number_elements", help="number of elements in list", action="store") 
argParser.add_argument("-l", "--list", help="number of elements in list",action="store", required=True, type=pair, nargs='+') 
argParser.add_argument("-r", "--type_request", help="Type of request (GET or SET).", required=True, action="store",choices=['SET', 'GET'],type=str) 
argParser.add_argument("-p", "--port_socket", help="Port to associate socket (identifier of client).",action="store",type=int) 


serverAddressPort   = ("127.0.0.1", 20001)
fakeAddress   = ("127.0.1.1", 20102)

bufferSize          = 1024
args = argParser.parse_args()

type_request = -1
if args.type_request == "GET":
    type_request = 1
elif args.type_request == "SET":
    type_request = 2
else:
    Exception("Invalid arg")

# Identifier of client/reques
P = -1 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
if args.port_socket:
    UDPClientSocket.bind(('127.0.0.1', args.port_socket))
    P = args.port_socket
else:
    # This useless message is to bind the socke to some address. 
    UDPClientSocket.sendto(bytes("---",  'utf-8'), fakeAddress)
    (addr , port ) =  UDPClientSocket.getsockname()
    P = port

print("Porta: " , P)
print("Pares")
print(args.list)

request_string = make_string_to_send(str(P), str(type_request), args.list)


# Send to server using created UDP socket

UDPClientSocket.sendto(bytes(request_string, 'utf-8'), serverAddressPort)

 

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

 

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)