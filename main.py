from asyncio import Event
import re
from matrixs import Matrixs
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


def run_server(matrixs):
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = format(bytesAddressPair[0])

        address = bytesAddressPair[1]
        if "GET" in message :
            print("Recebeu um get")
            matrixs.get_key()
        elif "SET" in message :
            print("Recebeu um set")
        else: 
            print("O que recebeu? " , message)
        #clientMsg = "Message from Client:{}".format(message)
        #clientIP  = "Client IP Address:{}".format(address)
        
        #print(clientMsg)
        #print(clientIP)
        
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)


if __name__ == "__main__":
    print("Olá da main (server)")
    read_file()
    print(params)

    matrixs = Matrixs(params)
    thread = Update_Keys(matrixs, params['T'])
    thread.start()
    run_server(matrixs)



