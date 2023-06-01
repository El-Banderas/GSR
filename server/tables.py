
from time import time 
from datetime import date, datetime, timedelta

class Tables:

    def init_system(self, params):
        today = date.today()
        today_string = today.strftime("%y%m%d")
        now = datetime.now()
        time = now.strftime("%H%M%S")

        # systemRestartDate (1) |  systemRestartTime (2)  |    systemKeySize (3) |  systemIntervalUpdate (4)
        # systemMaxNumberOfKeys (5) |  systemKeysTimeToLive (6)
        self.system = ["system" , today_string, time, params['K'], params['T'],  params['X'],  params['V']]
        self.keys_time_to_live = params['V']

    # TODO
    def init_config(self, params):
        self.config = ["config", params['M']]

    #  dataNumberOfValidKeys | dataTableGeneratedKeys
    def init_data(self):
        dataNumberOfValidKeys = 0
        dataTableGeneratedKeysEntry = []
        self.data = ["data", dataNumberOfValidKeys, dataTableGeneratedKeysEntry]

    # Key ID will be the line
    def add_key(self, keyValue, keyRequestor, keyVisibility ):
        current_line = self.data[1]
        print("Current line to insert key")
        print(current_line)

        now = datetime.today()
        result = now + timedelta(seconds=self.keys_time_to_live)
        date = int(result.strftime("%y%m%d"))
        time = int(result.strftime("%H%M%S"))
        print("Will expire in: " + str(date) )
        print(time)
        self.data[2].append([current_line, keyValue, keyRequestor, date, time, keyVisibility])
        ooid = "3.2." + str(current_line) + ".0"
        return (ooid, keyVisibility)



    def __init__(self, params):

        self.init_system(params)
        self.init_config(params)
        self.init_data()

    def update_matrix(self):
        print("Atualizar matrizes? " , -1)
 