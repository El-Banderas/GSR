import re

type_response = "0"

class Request:
    def __init__(self, client_id, P, S, Ns, list_Sec,  Y, N, list_args):
        self.S = S
        self.Ns = Ns
        self.list_Sec = list_Sec
        self.client_id = client_id         
        self.P = P        
        self.Y = Y
        self.N = N
        self.list_args = []
        list_args_separated = list_args.split(",") 
        for x in range(0, len(list_args_separated), 2):
            # Get address
            ooid = re.search('((\d+\.)*\d+)' ,list_args_separated[x])
            # Get number to get
            match = re.search("\'(\w+)\'", list_args_separated[x+1])
            pair_add_num = (ooid.group(1), match.group(1))
            self.list_args.append(pair_add_num)


def parse_message(message):
    (client_id, S, Ns, list_Sec, P, Y, N, list_args) = message.split(";")
    request = Request(client_id, P, S, Ns, list_Sec, Y, N, list_args)
    return request

def create_response(P,W,R):
    S = "0"
    Ns = "0"
    List_Security = []
    string_list_security = ''.join(str(x) for x in List_Security)
    string_list_pairs = '[' + ','.join(str(x) for x in W) + ']'
    string_list_errors = '[' + ','.join(str(x) for x in R) + ']'

    res = ";".join(["server", S, Ns, string_list_security, P, type_response, str(len(W)), string_list_pairs, str(len(R)), string_list_errors])
    print("[SERVER] Response to client")
    print(res)
    return res

def create_error_message(P, message):
    S = "0"
    Ns = "0"
    List_Security = []
    string_list_security = ''.join(str(x) for x in List_Security)
    string_list_pairs  = []
    string_list_errors = '['+ message +']'
    res = ";".join([S, Ns, string_list_security, P, type_response, str(len(string_list_pairs)), str(string_list_pairs), "1", string_list_errors])
    print("[SERVER] Response to client")
    print(res)
    return res
    
    