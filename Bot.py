#TODO: Could make this a class, but never see needing more than one instance

import re

#--------------------------------------------------------------------------------
# Globals
#--------------------------------------------------------------------------------
cmd_seq = re.compile('^!#')

#--------------------------------------------------------------------------------
def take_user_input(line):
    ''' This function parses what users type through proxy.  Enables control of the
        bot without rebuilding code.  
        
        Argument:
            line - line of text to be parsed
    '''
    parseCommand(line)
    
    return result;

#--------------------------------------------------------------------------------
def parseCommand(line):
    ''' Parse command lines 
    '''
    has_cmd = cmd_seq.match(line)
    has_cmd
    print(has_cmd)


#--------------------------------------------------------------------------------
def take_device_input(line):
    ''' This function parses what is received from device.  Actions determine by bot
        state/code.
        
        Argument:
            line - line of text to be parsed
    '''
    print(line)




