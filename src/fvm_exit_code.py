from enum import Enum

class ExitCode(Enum):
    """ An FVM exit code. """
    
    OK = 0
    """ Exited without an error. """
    
    ERROR = 1
    """ Exited with a user-defined generic error. """
    
    FVM_CRASH = 255
    """ Exited because the FVM entered an illegal state. """
