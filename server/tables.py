
from datetime import date, datetime, timedelta
from errors import errors_dic

def print_table(matrix):
    print("TABLE: ")
    for row in matrix:
        for column in row:
            print(column, end=";")
        print()


class Tables:
    

    ###########  INIT TABLES ########


    def init_system(self, params):
        today = date.today()
        today_string = today.strftime("%y%m%d")
        now = datetime.now()
        time = now.strftime("%H%M%S")

        # systemRestartDate (1) |  systemRestartTime (2)  |    systemKeySize (3) |  systemIntervalUpdate (4)
        # systemMaxNumberOfKeys (5) |  systemKeysTimeToLive (6)
        self.system = ["system" , today_string, time, params['K'], params['T'],  params['X'],  params['V']]
        self.keys_time_to_live = params['V']

    # Depois verificar se realmente usamos 255 coisas
    def init_config(self, params):
        self.config = ["config", params['M'], "0", "255", ]

    #  dataNumberOfValidKeys | dataTableGeneratedKeys
    def init_data(self):
        dataNumberOfValidKeys = 0
        dataTableGeneratedKeysEntry = ["---"]
        self.data = ["data", dataNumberOfValidKeys, dataTableGeneratedKeysEntry]

    ###########  ADD KEY TO TABLES ########

    def clean_old_keys(self):
        print("Clean old keys")
        now = datetime.today()
        date_now = int(now.strftime("%y%m%d"))
        time_now = int(now.strftime("%H%M%S"))
        number_deleted_keys = 0
        for index, key_info in enumerate(self.data[2][1:]):
            date_key = key_info[4]
            time_key = key_info[5]
            if date_key < date_now or time_key < time_now:
                print("Delete key")
                del self.data[2][index-number_deleted_keys]
                number_deleted_keys+=1
        # Update number of keys in table
        self.data[1] = len(self.data[2]) - 1
        return number_deleted_keys
        


    # Key ID will be the line
    def add_key(self, keyValue, keyRequestor, keyVisibility ):
        # Compare current number of keys with maximum:
        if (self.data[1] >= self.system[5] -1):
            # If maximum achieved, check if we can clean old keys
            n_deleted_keys = self.clean_old_keys()
            if n_deleted_keys == 0:
                return ([], "Maximum number of keys attributed")
        current_line = self.data[1]

        now = datetime.today()
        result = now + timedelta(seconds=self.keys_time_to_live)
        date = int(result.strftime("%y%m%d"))
        time = int(result.strftime("%H%M%S"))
        # We add --- in the beggining because the position 0 should not be read.
        self.data[2].append(["---", current_line, keyValue, keyRequestor, date, time, keyVisibility])
        self.data[1] = len(self.data[2]) - 1
        ooid = "3.2." + str(current_line) + ".0"
        print_table(self.data[2])
        error = []
        return ([(ooid, keyVisibility)], error)



    ###########  GET VALUES FROM TABLES ########
     # Return (ooid, value,error)
     # System and config are similiar tables, so it's possible to join them.
    def get_config_or_system(self, ooid, value, table, number_table, requestor):
        print("Config|System table")
        print(table)
        ids_values = []
        errors = []
        for i in range(int(value)):
            
            if len(ooid) == 2:
                column = ooid[0]+i
                if column >= len(table):
                    errors.append("invalid ooid")
                    return (ids_values, errors)
                instance = ooid[1]
                current_ooid =  ".".join([number_table, str(column), str(instance)])
                if instance != 0:
                    errors.append((current_ooid,"ooid not instance"))
                else:
                    ids_values.append((current_ooid,table[column] ))
            else:
                errors.append("invalid ooid")
        return (ids_values, errors)
    
    # Normal ooid: 
    #(0) First number: [1,2]
    #(1) Second number: [1, max number of keys]
    #(2) Third number: [1, 6]
    #(3) Fourth number: 0
    def get_next_ooid_data_table(self, ooid):
        if ooid == [ 1,0]:
            return [2,1, 0]
        # Strange ooids, that are out of the table
        if ooid[0] > 2 or ooid[1] > 6:
            return None
        else:
            if ooid[2] < 6:
                return [ooid[0], ooid[1], ooid[2]+1 ,0 ]
            if ooid[1] < len(self.data[2]):
                return [ooid[0], ooid[1]+1, 1, 0]
        return None

    # Return (ooid, value, error)
    def get_data_value_by_ooid(self, ooid):
        if ooid == [ 1,0]:
            return (self.data[0], None)
        else:
            # I could use the "dataNumberOfValidKeys", but I prefer this method.
            numer_lines = len(self.data[2])

            line = ooid[1]
            column = ooid[2]
            if line > numer_lines or column > 6 or line < 1:
                return ([], "invalid ooid")
            else:
                return ((".".join(["3.2", str(line), str(column)]), self.data[2][line][column]), None)

    def get_data(self, ooid, value, requestor):
        ooids_values = []
        errors = []
        for i in range(int(value) ):
            (value_ooid,  error) = self.get_data_value_by_ooid(ooid)
            ooids_values.extend(value_ooid)
            if error:
                errors.append(error)
            ooid = self.get_next_ooid_data_table(ooid)
            if ooid == None:
                break 
            
        print("Devolve")
        print(ooids_values)
        print(errors)
        return (ooids_values, errors)

    def get_values(self, list_ooids, requestor):
        errors_final = []
        ids_values_final = []
        print("GET nas tables")
        for (ooid_string, value) in list_ooids:

            ooid = ooid_string.split(".")
            ooid = list(map(lambda x : int(x), ooid))
            if ooid[0] == 1:
                print("SYSTEM")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_config_or_system(ooid, value, self.system, "1" , requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)
            elif ooid[0] == 2:
                print("CONFIG")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_config_or_system(ooid, value, self.config, "2" , requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)

            elif ooid[0] == 3:
                print("KEYS")
                ooid = ooid[1:]
                (ids_values, errors) = self.get_data(ooid, value, requestor)
                ids_values_final.extend(ids_values)
                errors_final.extend(errors)
            else:
                print("Error")
                errors.append(errors_dic["invalid ooid"], ooid_string)
        print("Resposta:")
        print(ids_values_final)
        print(errors_final)


        return (ids_values_final, errors_final)


    ###########  SET VALUES FROM TABLES ########
    # OOID 
    # 0 -> Table 
    # 1 -> Line 
    # 2 -> Value 0, instance 
    def set_config_or_system(self, ooid, value, table):
        print("Config|System table")
        print(table)
        if len(ooid) != 3 or ooid[2] != 0:
            return ([] , "invalid ooid") 
        column = ooid[1]
        instance = ooid[2]
        current_ooid =  ".".join([str(ooid[0]), str(column), str(instance)])
        if len(ooid) == 3:
            if column >= len(table):
                return ([],  "invalid ooid")
            else:
                table[column] = value
                print("After change")
                print(table)
                return ([(current_ooid,table[column])], [] )
        else:
            return ([], "invalid ooid")
    
    # OOID -> Not create key, process more complex
    # 0 -> 3, keys
    # 1 -> 2 (size table is read-only, should be implemented other way...) 
    # 2 -> line
    # 3 -> column [1, 6]
    # 4 -> Value 0, instance 
    def set_keys_table(self, ooid, value, table):
        print("Keys Table")
        print(table)
        if len(ooid) != 5 or ooid[1] != 2 or ooid[4] != 0:
            return ([], "invalid ooid") 
        line = ooid[2]
        column = ooid[3]
        ooid_strings = list(map(lambda num : str(num), ooid))
        current_ooid =  ".".join([*ooid_strings])
        if line >= len(table):
            return ([], "invalid ooid")
        else:
            table[line][column] = int(value)
            print("After change")
            print(table)
            return ([(current_ooid,table[line][column])], [] )


    def set_values(self, ooid, value, requestor):
        print("SET nas tables")

        ooid = ooid.split(".")
        ooid = list(map(lambda x : int(x), ooid))
        if ooid[0] == 1:
            print("SYSTEM")
            return self.set_config_or_system(ooid, value, self.system)
        elif ooid[0] == 2:
            print("CONFIG")
            return self.set_config_or_system(ooid, value, self.config )

        elif ooid[0] == 3:
            print("KEYS")
            return self.set_keys_table(ooid, value, self.data[2] )
        else:

            return ([],"invalid ooid" )


    def __init__(self, params):

        self.init_system(params)
        self.init_config(params)
        self.init_data()

 