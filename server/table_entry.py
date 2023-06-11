
from typing import Literal

max_access_available = Literal["rw", "ro"]

class Entry:
    # value = Value to store
    # max_access = {"rw" , "ro"} , read-write or read-only
    # creator = {None, id of client that created the value} , who can read/write the information 
    def __init__(self, value, max_access : max_access_available, creator, type, visibility=None):
        self.value = value
        self.max_access = max_access 
        self.creator = creator
        self.type = type
        self.visibility = visibility


    # Checks visibility of keys.
    def agent_can_get_or_set(self, agent):
        # No problem with visibility
        if self.visibility is None:
            return True
        # Anyone can see, 2 or higher
        if self.visibility > 1:
            return True
        # Visibility in [0,1]
        if self.creator == agent and self.visibility >= 0:
            # This way, a key with visibility of 0 can only be seen one time.
            if self.visibility == 0:
                self.visibility = -1
            return True
        return False
            



    # Check if the given agent can see the entrance
    # There could be problems with visibility, in case it's a key.
    def check_to_read(self, agent):
        if self.creator:
            return self.agent_can_get_or_set(agent)            
        else: 
            return True
    
    def correct_type(self, value):
        if self.type == 'str':
            return True
        if self.type == 'int':
            try:
                int(value)
                return True
            except ValueError:
                return False



    # Check if the given agent can change the value
    # Return if there were changes, and possible error
    def check_to_change(self, agent, new_value):
        if self.max_access == "ro":
            return (False, "3")
        if self.creator is not None:
            if self.agent_can_get_or_set(agent):
                if self.correct_type(new_value):
                    self.value = new_value
                    return (True, None)
                else:
                    return (False, "6")

            else:
                return (False, "5")
                
        if self.correct_type(new_value):
            self.value = new_value
            return (True, None)
        else:
            return (False, "6")

