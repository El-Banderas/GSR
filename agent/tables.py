
from datetime import date, datetime, timedelta
from table_entry import Entry
import sys
sys.path.append('./../')

def print_table(matrix):
    print("TABLE: ")
    for k, row in matrix.items():
        print(k,end="->")
        for column in row:
            if isinstance(column, str):
                print(column, end=";")
            else:
                print(column.value, end=";")
            
        print()

def print_simple_table(matrix):
    print("TABLE: ")
    for column in matrix:
        if isinstance(column, str):
            print(column, end=";")
        else:
            print(column.value, end=";")
    print()
            
    '''
In case we receive an ooid for tables like 3.2 or 3.2.1, this funcion converts to:
3.2.1.1.0
'''
def convert_incomplet_ooid(ooid):
    if (len(ooid)) == 1:
        ooid.extend([1,1,0])
    if (len(ooid)) == 2:
        ooid.extend([1,0])
    if (len(ooid)) == 3:
        ooid.extend([0])
    return ooid




class Tables:
    

    ###########  INIT TABLES ########


    def init_system(self, params):
        today = date.today()
        today_string = today.strftime("%y%m%d")
        now = datetime.now()
        time = now.strftime("%H%M%S")

        # systemRestartDate (1) |  systemRestartTime (2)  |    systemKeySize (3) |  systemIntervalUpdate (4)
        # systemMaxNumberOfKeys (5) |  systemKeysTimeToLive (6)
        self.system = ["system" , 
                       Entry(today_string,  "ro", None, 'int'),
                       Entry(time,  "ro", None, 'int'),
                       Entry(params['K'],  "rw", None, 'int'),
                       Entry(params['T'],  "rw", None, 'int'),
                       Entry(params['X'],  "rw", None, 'int'),
                       Entry(params['V'],  "rw", None, 'int'),
                       ]
        self.keys_time_to_live = params['V']

    # Depois verificar se realmente usamos 255 coisas
    def init_config(self, params):
        self.config = ["config", 
                       Entry(params['M'],  "rw", None, 'str'),
                       Entry("0",  "rw", None, 'int'),
                       Entry("255",  "rw", None, 'int'),
                       ]

    #  dataNumberOfValidKeys | dataTableGeneratedKeys
    def init_data(self):
        dataNumberOfValidKeys = 0
        dataTableGeneratedKeysEntry = {}
        self.data_current_index = 1
        self.data = ["data", 
                    Entry(dataNumberOfValidKeys,  "ro", None, 'int'),
                    dataTableGeneratedKeysEntry
                    ]

    ###########  ADD KEY TO TABLES ########
    # Here we don't need to check authorizations
    def clean_old_keys(self):
        print("Clean old keys")
        now = datetime.today()
        date_now = int(now.strftime("%y%m%d"))
        time_now = int(now.strftime("%H%M%S"))
        number_deleted_keys = 0
        # Max line - number of available keys == position first key
        current_index = self.data_current_index - self.data[1].value
        while current_index < self.data_current_index:
            key_info = self.data[2][current_index]
            date_key = key_info[4].value
            time_key = key_info[5].value
            if date_key < date_now or time_key < time_now:
                print("Delete key")
                del self.data[2][current_index]
                number_deleted_keys+=1
                # Number of valid keys lost one key
                self.data[1].value = self.data[1].value-1
            current_index+=1
        # Update number of keys in table
        return number_deleted_keys
        


    # Key ID will be the line
    def add_key(self, keyValue, keyRequestor, keyVisibility ):
        # Compare current number of keys with maximum:
        if (self.data[1].value >= self.system[5].value ):
            # If maximum achieved, check if we can clean old keys
            n_deleted_keys = self.clean_old_keys()
            if n_deleted_keys == 0:
                return ([], '2')

        now = datetime.today()
        result = now + timedelta(seconds=self.keys_time_to_live)
        date = int(result.strftime("%y%m%d"))
        time = int(result.strftime("%H%M%S"))
        # If the keyVisibility is 0, we assume the key must be secure.
        if keyVisibility > 0:
            max_access = "rw"
        else:
            max_access = "ro"
        current_line = self.data_current_index
        self.data_current_index = current_line+1
        self.data[2][current_line] = ["---", 
                            self.data[1],
                            Entry(keyValue,  max_access, keyRequestor, 'str', keyVisibility),
                            Entry(keyRequestor,  max_access, keyRequestor, 'str', keyVisibility),
                            Entry(date,  max_access, keyRequestor, 'int', keyVisibility),
                            Entry(time,  max_access, keyRequestor, 'int', keyVisibility),
                            Entry(keyVisibility, max_access, keyRequestor, 'int', keyVisibility),
                             ]
        old_data_1 = self.data[1].value
        self.data[1] = Entry(old_data_1+1,  "ro", None, 'int')
        ooid = "3.2.6." + str(current_line) + ".0"
        print_table(self.data[2])
        error = []
        return ([(ooid, str(keyVisibility))], error)



    ###########  GET VALUES FROM TABLES ########
     # Return (ooid, value,error)
     # System and config are similiar tables, so it's possible to join them.
     # Here we don't have authorization problems, so we don't need to check.
    def get_config_or_system(self, ooid, value, table, number_table, requestor):
        print("Config|System table")
        print_simple_table(table)
        ids_values = []
        errors = []
        for i in range(int(value)):
            
            if len(ooid) == 2:
                column = ooid[0]+i
                if column >= len(table):
                    errors.append(1)
                    return (ids_values, errors)
                instance = ooid[1]
                current_ooid =  ".".join([number_table, str(column), str(instance)])
                if instance != 0:
                    errors.append((current_ooid,1))
                else:
                    ids_values.append((current_ooid,str(table[column].value) ))
            else:
                errors.append('1')
        return (ids_values, errors)
    
    # Normal ooid: 
    #(0) First number: [1,2]
    #(1) Second number: [1, 6] , max number of columns
    #(2) Third number: [1, number_keys]
    #(3) Fourth number: 0
    def get_next_ooid_data_table(self, ooid):
        if ooid == [ 1,0]:
            return [2,1, 0]
        if len(ooid) < 4:
            ooid = convert_incomplet_ooid(ooid)
        # Strange ooids, that are out of the table
        if ooid[2]+1 < self.data_current_index:
            return [ooid[0], ooid[1], ooid[2]+1 ,0 ]
        # If we haven't reached the end of the table (last line).
        if ooid[1] < 6:
            return [ooid[0], ooid[1]+1, 1, 0]
        # Return ooid and error
        return (f"3.2.6.{self.data_current_index}.0", '1' )

        # Return (ooid, value, error)
    def get_data_value_by_ooid(self, ooid, requestor):
        print("Get data")
        print(ooid)
        if ooid == [ 1,0]:
            return ([("3.1.0",str(self.data[1].value))], None)
        else:
            if len(ooid) < 4:
                ooid = convert_incomplet_ooid(ooid)
            # I could use the "dataNumberOfValidKeys", but I prefer this method.
            numer_lines = self.data_current_index

            column = ooid[1]
            line = ooid[2]
            convert_ooid_to_string = list(map(lambda num : str(num), ooid))
            current_ooid = ".".join(["3"]+convert_ooid_to_string)
            if line >= numer_lines or column > 6 or line < 1 or column < 0:
                return ([], (current_ooid, '1'))
            else:
                entry = self.data[2][line][column]
                if entry.check_to_read(requestor):
                    pair = (".".join(["3.2", str(column), str(line), "0"]), str(entry.value))
                    return (pair, None)
                else:
                    return ([], (current_ooid,'4'))

    def get_data(self, ooid, value, requestor):
        ooids_values = []
        errors = []
        for i in range(int(value) ):
            (value_ooid,  error) = self.get_data_value_by_ooid(ooid, requestor)
            if len(value_ooid) > 0:
                ooids_values.append(value_ooid)
            if error:
                errors.append(error)
            ooid = self.get_next_ooid_data_table(ooid)
            # If there are more requests, we should stop and return error.
            if type(ooid) == tuple and i+1 < int(value):
                errors.append(ooid)
                
                break 
            
        return (ooids_values, errors)

    def get_values(self, list_ooids, requestor):
        errors_final = []
        ids_values_final = []
        for (ooid_string, value) in list_ooids:

            ooid = ooid_string.split(".")
            ooid = list(map(lambda x : int(x), ooid))
            if ooid[0] == 1:
                print("Get SYSTEM")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_config_or_system(ooid, value, self.system, "1" , requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)
            elif ooid[0] == 2:
                print("Get CONFIG")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_config_or_system(ooid, value, self.config, "2" , requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)

            elif ooid[0] == 3:
                print("Get KEYS")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_data(ooid, value, requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)
            else:
                print("Error")
                errors.append("1", ooid_string)


        return (ids_values_final, errors_final)


    ###########  SET VALUES FROM TABLES ########
    # OOID 
    # 0 -> Table 
    # 1 -> Line 
    # 2 -> Value 0, instance 
    def set_config_or_system(self, ooid, value, table):
        print("Config|System table")
        print_simple_table(table)
        if len(ooid) != 3 or ooid[2] != 0:
            return ([] , '1') 
        column = ooid[1]
        instance = ooid[2]
        current_ooid =  ".".join([str(ooid[0]), str(column), str(instance)])
        if len(ooid) == 3:
            if column >= len(table):
                return ([],  '1')
            else:
                value_table = table[column]
                # Anyone can change this value
                (changed, maybeError) = value_table.check_to_change(None, value)
                print("After change")
                print_simple_table(table)
                if changed:
                    return ([(current_ooid, value_table.value)], [] )
                else:
                    return ([],  maybeError)
        else:
            return ([], '1')
    
    # OOID -> Not create key, process more complex
    # 0 -> 3, keys
    # 1 -> 2 (size table is read-only, should be implemented other way...) 
    # 2 -> line
    # 3 -> column [1, 6]
    # 4 -> Value 0, instance 
    def set_keys_table(self, ooid, value, table, requestor):
        print("Keys Table")
        if ooid == [3,1,0]:
            return ([], '3') 
        if len(ooid) != 5 or ooid[1] != 2 or ooid[4] != 0:
            return ([], '1') 
        column = ooid[2]
        line = ooid[3]
        ooid_strings = list(map(lambda num : str(num), ooid))
        current_ooid =  ".".join([*ooid_strings])
        if line >= len(table):
            return ([], '1')
        else:
            value_table = table[line][column]
            #table[line][column] = int(value)
            (changed, maybeError) = value_table.check_to_change(requestor, int(value))
            print("After change")
            print_table(table)
            if changed:
                return ((current_ooid,value_table.value), [] )
            else:
                return ([], maybeError)



    def set_values(self, ooid, value, requestor):

        ooid = ooid.split(".")
        ooid = list(map(lambda x : int(x), ooid))
        if ooid[0] == 1:
            print("Set SYSTEM")
            return self.set_config_or_system(ooid, value, self.system)
        elif ooid[0] == 2:
            print("Set CONFIG")
            return self.set_config_or_system(ooid, value, self.config )

        elif ooid[0] == 3:
            print("Set KEYS")
            return self.set_keys_table(ooid, value, self.data[2], requestor )
        else:

            return ([],'1' )


    def __init__(self, params):

        self.init_system(params)
        self.init_config(params)
        self.init_data()

 