from client_get import main_funcion_client
import unittest
import time
import sys
sys.path.append('./../server')
from errors import errors_dic 

# Variables used to test
SystemKeySize = str(10)
systemIntervalUpdate = str(3000)

systemMaxNumberOfKeys = str(3)
systemKeysTimeToLive = str(5)

constante_number_keys = -1

'''
This tests are statefull, so they depende on each other, because the state of the server (tables) matter.
So, when creating a new test, consider the previous state of the server.
'''

class TestStringMethods(unittest.TestCase):
    def test_Add_Key_And_Verify_Size(self):
        global constante_number_keys 
        res=main_funcion_client("Cli1", "GET", [('1.5.0','1')] )
        (_, number_keys_str) = res.list_args[0]
        constante_number_keys  = int(number_keys_str)
        res = main_funcion_client("Cli0", "SET", [('3.2.6.0', '1')] )
        print("Compares")
        print(res.list_args)
        print(res.list_errors)
        request_2 = main_funcion_client("Cli0", "GET", [('3.1.0', '1')] )
        (_, current_number_keys) = request_2.list_args[0]
        current_number_keys  = int(current_number_keys)

        self.assertEqual(res.list_args, [('3.2.6.1.0', '1')])
        self.assertEqual(res.list_errors, [])
        self.assertEqual(current_number_keys  , 1)


    # Table has one key, because of the previous test
    def test_Get_Full_Table_Keys_and_Error(self):
        global constante_number_keys 
        for i in range(constante_number_keys-1):
            res = main_funcion_client("Cli0", "SET", [('3.2.6.0', '1')] )
            # if i = 0 => analise line 2 of table
            self.assertEqual(res.list_args, [(f'3.2.6.{i+2}.0', '1')])
            self.assertEqual(res.list_errors, [])
        key_not_setted = main_funcion_client("Cli0", "SET", [('3.2.6.0', '1')] )
        # if i = 0 => analise line 2 of table
        self.assertEqual(key_not_setted.list_args, [])
        self.assertEqual(key_not_setted.list_errors, [(f'3.2.6.0', 'Maximum number of keys attributed')])
     
    def test_Keys_deleted_after_time(self):
        res_keys_time_to_live = main_funcion_client("Cli0", "GET", [('1.6.0', '1')] )
        (_, seconds) = res_keys_time_to_live.list_args[0]
        time.sleep(int(seconds)+0.5)
        res = main_funcion_client("Cli0", "SET", [('3.2.6.0', '1')] )
        # if i = 0 => analise line 2 of table
        self.assertEqual(res.list_args, [(f'3.2.6.1.0', '1')])
        self.assertEqual(res.list_errors, [])

        request_number_keys = main_funcion_client("Cli0", "GET", [('3.1.0', '1')] )
        (_, current_number_keys) = request_number_keys.list_args[0]
        current_number_keys  = int(current_number_keys)
        self.assertEqual(current_number_keys  , 1)
        # Table has one key
    

    # We use the previous key added by the client.
    def test_permission_to_see_key_other_client(self):
        other_client_tries_to_see = main_funcion_client("Cli1", "GET", [('3.2.2.1.0', '1')] )
        self.assertEqual(other_client_tries_to_see.list_args, [])
        self.assertEqual(other_client_tries_to_see.list_errors, [('3.2.2.1.0', 'No permissions to see')])
    
    def test_everybody_can_see(self):
        main_funcion_client("Cli0", "SET", [('3.2.6.0', '2')] )
        same_client = main_funcion_client("Cli0", "GET", [('3.2.6.2.0', '1')] )
        self.assertEqual(same_client.list_args, [('3.2.2.6.0', '2')])
        self.assertEqual(same_client.list_errors, [])

        other_client = main_funcion_client("Cli1", "GET", [('3.2.6.2.0', '1')] )
        self.assertEqual(other_client.list_args, [('3.2.2.6.0', '2')])
        self.assertEqual(other_client.list_errors, [])
    
    def test_visibility_zero(self):
        main_funcion_client("Cli0", "SET", [('3.2.6.0', '0')] )
        same_client = main_funcion_client("Cli0", "GET", [('3.2.6.3.0', '1')] )
        self.assertEqual(same_client.list_args, [('3.2.3.6.0', '0')])
        self.assertEqual(same_client.list_errors, [])

        same_client_again = main_funcion_client("Cli0", "GET", [('3.2.6.3.0', '1')] )
        self.assertEqual(same_client_again.list_args, [])
        self.assertEqual(same_client_again.list_errors, [('3.2.6.3.0', 'No permissions to see')])
        
        other_client_again = main_funcion_client("Cli1", "GET", [('3.2.6.3.0', '1')] )
        self.assertEqual(other_client_again.list_args, [])
        self.assertEqual(other_client_again.list_errors, [('3.2.6.3.0', 'No permissions to see')])


debug = False
if debug:

    main_funcion_client("Cli0", "SET", [('3.2.6.0', '2')] )
    same_client = main_funcion_client("Cli0", "GET", [('3.2.6.1.0', '1')] )
    print(same_client.list_args)
    print(same_client.list_errors)
    other_client = main_funcion_client("Cli0", "GET", [('3.2.6.1.0', '1')] )
    print(other_client.list_args)
    print(other_client.list_errors)

   #
if not debug:
    if __name__ == '__main__':
        unittest.main()