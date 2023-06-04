
# Constant variables related to securiry and PDU of messages
S = "0"
Ns = "0"
List_Security = []
checksum = "CHECKSUM"


# Type request:
# 0 = response, 1 = get, 2 = set
def make_string_to_send(P, type_request, list_pairs):
    for pair in list_pairs:
        if len(pair) < 2:
            print(pair)
            raise Exception(f"Arguments of -l must be pairs: {pair}" )
    string_list_security = ''.join(str(x) for x in List_Security)
    string_list_pairs = '[' + ','.join(str(x) for x in list_pairs) + ']'
    res = ";".join([P, S, Ns, string_list_security, type_request, str(len(list_pairs)), string_list_pairs, checksum])
    print("Sending")
    print(res)
    return res


