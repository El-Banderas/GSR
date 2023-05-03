
from threading import Thread
from threading import Event
from matrixs import Matrixs
import time


class Update_Keys(Thread):
    def __init__(self, matrixs, refresh_time):
        Thread.__init__(self)
        self.matrixs = matrixs
        self.refresh_time = refresh_time #* 0.001

    def run(self):
        while True:
            # Em segundos
            time.sleep(self.refresh_time)
            self.matrixs.get_key()
