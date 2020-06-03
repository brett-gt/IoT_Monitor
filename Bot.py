import re

class Bot(object):

    #--------------------------------------------------------------------------------
    # Globals
    #--------------------------------------------------------------------------------
    self.cmd_seq = re.compile('^!#')

    #----------------------------------------------------------------------------
    def __init__(self):
        self.enabled = True;

    #--------------------------------------------------------------------------------
    def take_user_input(self, line):
        ''' This function parses what users type through proxy.  Enables control of the
            bot without rebuilding code.  
        
            Argument:
                line - line of text to be parsed
        '''
        was_cmd = parseCommand(line)

        if(self.enabled and was_cmd == False):
            parseNonCommand(line)
            
        return was_cmd;  #TODO: May want to return if Bot Handled or not so don't forward to end point if Bot did

    #--------------------------------------------------------------------------------
    def parseCommand(self, line):
        ''' Parse command lines 
        '''
        has_cmd = cmd_seq.match(line)
        has_cmd
        print(has_cmd)

        return True;  #TODO: Return based on it being a command or not

    #--------------------------------------------------------------------------------
    def parseNonCommand(self, line):
        print("parseLine")


    #--------------------------------------------------------------------------------
    def take_device_input(self, line):
        ''' This function parses what is received from device.  Actions determine by bot
            state/code.
        
            Argument:
                line - line of text to be parsed
        '''
        print(line)




