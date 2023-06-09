
import re
# Constant variables related to securiry and PDU of messages
S = "0"
Ns = "0"
List_Security = []


# Type request:
# 0 = response, 1 = get, 2 = set
def make_string_to_send(client_id, P, type_request, list_pairs, checksum):
    for pair in list_pairs:
        if len(pair) < 2:
            print(pair)
            raise Exception(f"Arguments of -l must be pairs: {pair}" )
    string_list_security = ''.join(str(x) for x in List_Security)
    string_list_pairs = '[' + ','.join(str(x) for x in list_pairs) + ']'
    res = ";".join([client_id,  S, Ns, string_list_security, str(P),type_request, str(len(list_pairs)), string_list_pairs, checksum.decode()])
    print("Sending")
    print(res)
    return res

class Response:
    # Request type is always "response", so we don't store it.
    def __init__(self, client_id, P, S, Ns, list_Sec, Request_type, N, list_args, num_errors, errors):
        self.S = S
        self.Ns = Ns
        self.list_Sec = list_Sec
        self.P = P        
        self.client_id = client_id        
        self.N = N
        self.list_args = []
        list_args_separated = list_args.split(",") 
        if len(list_args_separated) > 1:
            for x in range(0, len(list_args_separated), 2):
                # Get address
                ooid = re.search('((\d+\.)*\d+)' ,list_args_separated[x])
                # Get number to get
                match = re.search("\'(\d+)\'", list_args_separated[x+1])
                pair_add_num = (ooid.group(1), match.group(1))
                self.list_args.append(pair_add_num)

        self.list_errors = []
        list_errors_separated = errors.split(",") 
        if len(list_errors_separated ) > 1:
            for x in range(0, len(list_errors_separated ), 2):
                ooid = re.search('((\d+\.)*\d+)' ,list_errors_separated[x])
                # Capture string inside ''
                error_value = re.search("\'([^\']+)\'.*" ,list_errors_separated[x+1])
                pair_ooid_error = (ooid.group(1), error_value.group(1))
                self.list_errors.append(pair_ooid_error)

def parse_message(message):
    (server_id, S, Ns, list_Sec, P, Request_type, N, list_args, num_errors, errors) = message.split(";")
    request = Response( server_id, P, S, Ns, list_Sec, Request_type, N, list_args, num_errors, errors)
    return request




