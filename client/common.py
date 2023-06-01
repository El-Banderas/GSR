
# Constant variables related to securiry and PDU of messages
S = "0"
Ns = "0"
List_Security = []


# Type request:
# 0 = response, 1 = get, 2 = set
def make_string_to_send(P, type_request, list_pairs):
    string_list_security = ''.join(str(x) for x in List_Security)
    string_list_pairs = '[' + ','.join(str(x) for x in list_pairs) + ']'
    res = ";".join([S, Ns, string_list_security, P, type_request, str(len(list_pairs)), string_list_pairs])
    print(res)
    return res