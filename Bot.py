import re

class Bot(object):
    #--------------------------------------------------------------------------------
    # Globals
    #--------------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    def __init__(self):
        self.version = "1.0"
        self.cmd_seq = re.compile('^!#(\w+)')

        self.enabled = True;
        self.msgs_sent = 0;

    #--------------------------------------------------------------------------------
    def take_proxy_input(self, line):
        ''' This function parses what users type through proxy.  Enables control of the
            bot without rebuilding code.  
        
            Argument:
                line - line of text to be parsed
        '''
        response = self.parseCommand(line)

        if(self.enabled and not response):
            self.parseNonCommand(line)
            
        return response;  

    #--------------------------------------------------------------------------------
    def parseCommand(self, line):
        ''' Check and see if this is a command sequence, if so handle it.
        '''
        cmds = re.findall(self.cmd_seq, line)
        print(cmds)

        data = self.version.encode()

        if(len(cmds) == 0):
            return []

        else:
            response = []
            if(cmds[0] == 'ENABLE'):
                msg = "Enabling bot."
                response.append(msg)
                print(msg)
                self.enabled = True

            elif(cmds[0] == 'DISABLE'):
                msg = "Disabling bot."
                response.append(msg)
                print(msg)
                self.enabled = False

            elif(cmds[0] == 'STATUS'):
                response = self.print_status()

            else:
                msg = "Bot::parseCommand:  Invalid command argumnet " + cmds[0]
                print(msg)
                response.append(msg)

            return response  #TODO: Return based on it being a command or not

    #--------------------------------------------------------------------------------
    def parseNonCommand(self, line):
        ''' Place holder.  Don't think I will need this because don't have a use case
            to process non-command lines from the user. Instead these are just passed
            through (which is handled at a higher level).
        '''
        return False

    #--------------------------------------------------------------------------------
    def take_device_input(self, line):
        ''' This function parses what is received from device.  Actions determine by bot
            state/code.
        '''
        print(line)


    #--------------------------------------------------------------------------------
    def handle_disconnect(self):
        ''' Place holder with function to handle get disconnected (may try reconnect,
            may send message, etc)
        '''


    #--------------------------------------------------------------------------------
    def print_status(self):
        ''' Print Bot status.  
            TODO: Needs to be updated with major bot changes.
            TODO: Other ideas: count how many text messages have been sent, 
        '''
        status_lines = []
        status_lines.append("\n\n------------------------------------------------------------------------\n")
        status_lines.append("                         BOT Version " +  self.version + "\n\n")
        status_lines.append(" Enabled: " + str(self.enabled) + "\n")
        status_lines.append(" Messages Sent: " + str(self.msgs_sent) + "\n")
        status_lines.append("\n------------------------------------------------------------------------\n")

        for lines in status_lines:
            print(lines)

        return status_lines









