from manager import main_function_manager
import unittest

import sys
sys.path.append('./../server')
from errors import errors_dic 
unittest.TestLoader.sortTestMethodsUsing = None



class TestStringMethods(unittest.TestCase):
    def test_flood_server(self):
        for i in range(52):
            much_requests = main_function_manager("manager0", "GET", [('2.2.0','1')] )
            if len(much_requests.list_errors) > 0:
                print("Comparou")
                self.assertEqual(much_requests.list_args, [])
                self.assertEqual(much_requests.list_errors, [('0.0', 'Too many requests')])
                break
                


debug = False
if debug:
    for i in range(52):
            main_function_manager("manager0", "GET", [('2.2.0','1')] )
    much_requests = main_function_manager("manager0", "GET", [('2.2.0','1')] )
    print("Erro de muitos pedidos")
    print(much_requests.list_args)
    print(much_requests.list_errors)
    #request_incomplete  = main_function_manager("manager0", "GET", [('2.4.0','23')] )
    #print("\n\nDebug")
    #print(request_incomplete.list_args)
    #print(request_incomplete.list_errors)
    #res=main_function_manager("Badmanagerent", "GET", [('2.2.0','1')] )
    #print("\n\nDebug")
    #print(res.list_args)
    #print(res.list_errors)
    #
if not debug:
    if __name__ == '__main__':
        unittest.main()