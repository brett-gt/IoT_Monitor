import re
from BotActions import parse_device_input
from datetime import datetime
import Secrets
from SNS import SNS

class Bot(object):  
    #----------------------------------------------------------------------------
    def __init__(self, proxy, device):
        ''' 
        '''
        self.version = "1.0"
        self.cmd_seq = re.compile('^!#(\w+)')

        self.proxy = proxy
        self.device = device

        self.enabled = True;

        self.messanger = SNS([Secrets.phone_num])


    #--------------------------------------------------------------------------------
    def take_proxy_input(self, line):
        ''' This function parses what users type through proxy.  Enables control of the
            bot without rebuilding code.  
        
            Argument:
                line - line of text to be parsed
        '''
        was_cmd = self.parse_command(line)

        if(self.enabled and not was_cmd):
            self.parse_non_command(line)
            
        return was_cmd;  

    #--------------------------------------------------------------------------------
    def parse_command(self, line):
        ''' Check and see if this is a command sequence, if so handle it.
        '''
        cmds = re.findall(self.cmd_seq, line)
        print(cmds)

        was_cmd = False

        if(len(cmds) != 0):
            was_cmd = True
            msg = []
            if(cmds[0] == 'ENABLE'):
                msg.append("Enabling bot.")
                self.enabled = True

            elif(cmds[0] == 'DISABLE'):
                msg.append("Disabling bot.")
                self.enabled = False

            elif(cmds[0] == 'STATUS'):
                self.print_status()

            else:
               msg.append("Bot::parseCommand:  Invalid command argumnet " + cmds[0])

            self.proxy_print(msg)

        return was_cmd  #TODO: Return based on it being a command or not

    #--------------------------------------------------------------------------------
    def parse_non_command(self, line):
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
        results = parse_device_input(line)

        if(results):
            for line in results:
                self.messanger.send_text(line)
     

    #--------------------------------------------------------------------------------
    def handle_disconnect(self):
        ''' TODO: Place holder with function to handle get disconnected (may try reconnect,
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

        self.proxy_print(status_lines)  


    #--------------------------------------------------------------------------------
    def proxy_print(self, buffer):
        for line in buffer:
            print(line)
            self.proxy.transmit(line.encode())
            










