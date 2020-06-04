import re

class Bot(object):
    #--------------------------------------------------------------------------------
    # Globals
    #--------------------------------------------------------------------------------
    

    #----------------------------------------------------------------------------
    def __init__(self):
        self.enabled = True;

        self.cmd_seq = re.compile('^!#(\w+)')

    #--------------------------------------------------------------------------------
    def take_user_input(self, line):
        ''' This function parses what users type through proxy.  Enables control of the
            bot without rebuilding code.  
        
            Argument:
                line - line of text to be parsed
        '''
        was_cmd = self.parseCommand(line)

        if(self.enabled and was_cmd == False):
            self.parseNonCommand(line)
            
        return was_cmd;  #TODO: May want to return if Bot Handled or not so don't forward to end point if Bot did

    #--------------------------------------------------------------------------------
    def parseCommand(self, line):
        ''' Parse command lines 
        '''
        cmds = re.findall(self.cmd_seq, line)
        print(cmds)

        if(len(cmds) == 0):
            return False
        else:
            if(cmds[0] == 'ENABLE'):
                print("Enabling bot.")
                self.enabled = True

            elif(cmds[0] == 'DISABLE'):
                print("Disabling bot.")
                self.enabled = False

            else:
                print("Bot::parseCommand:  Invalid command argumnet " + cmds[0])

        
            return True  #TODO: Return based on it being a command or not

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




