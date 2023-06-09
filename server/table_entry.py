
from typing import Literal

max_access_available = Literal["rw", "ro"]

class Entry:
    # value = Value to store
    # max_access = {"rw" , "ro"} , read-write or read-only
    # creator = {None, id of client that created the value} , who can read/write the information 
    def __init__(self, value, max_access : max_access_available, creator):
        self.value = value
        self.max_access = max_access 
        self.creator = creator

    # Check if the given agent can see the entrance
    def check_to_read(self, agent):
        if self.creator is not None:
            print("Veirify")
            print(self.creator)
            print(agent)
            return self.creator == agent
        else: 
            return True

    # Check if the given agent can change the value
    # Return if there were changes, and possible error
    def check_to_change(self, agent, new_value):
        if self.max_access == "ro":
            return (False, "Setting to read-only value")
        if self.creator is not None:
            if self.creator == agent:
                self.value = new_value
                return (True, None)
            else:
                return (False, "No permissions to change")
                
        self.value = new_value
        return (True, None)

