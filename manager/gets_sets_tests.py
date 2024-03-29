from manager import main_function_manager
import unittest

import sys
sys.path.append('./../server')
from errors import errors_dic 

# Variables used to test
SystemKeySize = str(10)
systemIntervalUpdate = str(3000)

systemMaxNumberOfKeys = str(3)
systemKeysTimeToLive = str(5)

unittest.TestLoader.sortTestMethodsUsing = None



class TestStringMethods(unittest.TestCase):
    def test_Add_Key(self):
        res = main_function_manager("manager0", "SET", [('3.2.6.0', '1')] )
        self.assertEqual(res.list_args, [('3.2.6.1.0', '1')])
        self.assertEqual(res.list_errors, [])
    



    ## --------------  Test GETS -------------------
    # Data tables, extreme cases
    def test_Incomplete_OOID_Keys(self):
        request_incomplete = main_function_manager("manager0", "GET", [('3.2', '1')] )
        self.assertEqual(request_incomplete.list_args, [('3.2.1.1.0', '0')])
        self.assertEqual(request_incomplete.list_errors, [])

    # If the gets are received by column, correctly
    def test_data_look_by_collumns(self):
        main_function_manager("manager1", "SET", [('3.2.6.0', '2')] )
        request_clients_ids = main_function_manager("manager0", "GET", [('3.2.3', '2')] )
        self.assertEqual(request_clients_ids.list_args, [('3.2.3.1.0', 'manager0'), ('3.2.3.2.0', 'manager1')])
        self.assertEqual(request_clients_ids.list_errors, [])
    
    def test_too_much_ooids(self):
        request_too_much = main_function_manager("manager0", "GET", [('3.2.6', '9')] )
        self.assertEqual(request_too_much.list_args, [('3.2.6.1.0', '1'),('3.2.6.2.0', '2')])
        self.assertEqual(request_too_much.list_errors, [('3.2.6.3.0', 'invalid ooid')])
    


    # Only gets one value
    def test_Get_SystemTable_One(self):
        res=main_function_manager("manager1", "GET", [('1.3.0','1')] )

        self.assertEqual(res.list_args, [('1.3.0', SystemKeySize)])
        self.assertEqual(res.list_errors, [])
     
    def test_Get_SystemTable_Complex(self):
        res=main_function_manager("manager1", "GET", [('1.3.0','2'), ('1.5.0','2')] )

        self.assertEqual(res.list_args, [('1.3.0', SystemKeySize), ('1.4.0', systemIntervalUpdate),
                                        ('1.5.0', systemMaxNumberOfKeys) , ('1.6.0', systemKeysTimeToLive) ])
        self.assertEqual(res.list_errors, [])
    
    # Only gets one value
    def test_Get_ConfigTable_One(self):
        res=main_function_manager("manager1", "GET", [('2.2.0','1')] )

        self.assertEqual(res.list_args, [('2.2.0', '0')])
        self.assertEqual(res.list_errors, [])
     
    def test_Get_SystemTable_Complex(self):
        res=main_function_manager("manager1", "GET", [('2.2.0','2')] )

        self.assertEqual(res.list_args, [('2.2.0', '0'), ('2.3.0', '255')])
        self.assertEqual(res.list_errors, [])
    
    def test_get_OOID_Not_Exist(self):
        res = main_function_manager("manager0", "SET", [('2.4.0','23')] )
        self.assertEqual(res.list_args, [])
        self.assertEqual(res.list_errors, [('2.4.0', 'invalid ooid')])

    ## --------------  Test SETS -------------------
     
    # One client changes the value, and the next sees new value.
    # Server must be inicialize
    def test_Set_Config(self):
        res_before = main_function_manager("manager1", "GET", [('2.3.0','1')] )
        res = main_function_manager("manager0", "SET", [('2.3.0','23')] )
        res_after = main_function_manager("manager1", "GET", [('2.3.0','23')] )

        self.assertEqual(res_before.list_args, [('2.3.0', '255')])
        self.assertEqual(res_before.list_errors, [])
        
        self.assertEqual(res.list_args, [('2.3.0', '23')])
        self.assertEqual(res.list_errors, [])
        
        self.assertEqual(res_after.list_args, [('2.3.0', '23')])
        self.assertEqual(res_after.list_errors, [])
    
    # Try to change read only value
    def test_Set_On_RO(self):
        res = main_function_manager("manager0", "SET", [('1.1.0','23')] )

        self.assertEqual(res.list_args, [])
        self.assertEqual(res.list_errors, [('1.1.0', 'Setting to read-only value')])
        
    def test_set_OOID_Not_Exist(self):
        res = main_function_manager("manager0", "SET", [('2.4.0','23')] )

        self.assertEqual(res.list_args, [])
        self.assertEqual(res.list_errors, [('2.4.0', 'invalid ooid')])

    def test_types_of_values_SET(self):
        set_wrong_type = main_function_manager("manager0", "SET", [('2.2.0','a')] )
        self.assertEqual(set_wrong_type.list_args, [])
        self.assertEqual(set_wrong_type.list_errors, [('2.2.0', 'Type of value not accepted')])
        
        set_correct = main_function_manager("manager0", "SET", [('2.2.0','1')] )
        self.assertEqual(set_correct.list_args, [('2.2.0','1')])
        self.assertEqual(set_correct.list_errors, [])
    
    def test_user_not_authenticated(self):
        not_autenticated=main_function_manager("badManager", "GET", [('2.2.0','1')] )
        self.assertEqual(not_autenticated.list_args, [])
        self.assertEqual(not_autenticated.list_errors, [('0.0', 'User not authenticated')])


debug = False
if debug:
    res = main_function_manager("manager0", "SET", [('3.2.6.0', '1')] )
    #for i in range(52):
    #        main_function_manager("manager0", "GET", [('2.2.0','1')] )
    #much_requests = main_function_manager("manager0", "GET", [('2.2.0','1')] )
    print("Erro de muitos pedidos")
    print(res.list_args)
    print(res.list_errors)
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