#TODO List: 
#   Handle mud disconnects
#
#---------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------
from Proxy import proxy
from Telnet import Session

import Secrets
import os
import threading

#---------------------------------------------------------------------------------
# Globals
#---------------------------------------------------------------------------------
def bot_C2(data):
    '''Command and control for the bot functions.
    '''



#---------------------------------------------------------------------------------
def receive_handler():
    ''' Receives data from the end-point.  It then parses it with the bot.
        Bot output and end-point data are passed through to the proxy and 
        the bot output (if any) is sent back to the end-point. 
    '''
    print("Proxy transmit thread starting...")
    while not stop.is_set():
        data = os.read(pipeToSocketR, 4096)
        if not data:
            print("EOF from pipe")
            break
        else:
            bot_C2(data)
            proxy.transmit(data)

#---------------------------------------------------------------------------------
def transmit_handler():
    ''' Thread function to transmit data from the bot/proxy to the client.
        This data is received via a pipe which is written to by the bot or telnet connection.
    '''
    data = b''  # to handle partial lines
    while not stop.is_set():
        try:
            data += os.read(socketToPipeR, 4096)
            telnetSess.handle_from_pipe(data)

        except EOFError:
            telnetSess.log("EOF in pipe")
            stop.set()


#---------------------------------------------------------------------------------
# Main Code 
#---------------------------------------------------------------------------------
print("--------------------------------------------------------------------------")
print("Running Bot")
print("--------------------------------------------------------------------------")

# Create pipes for moving the data
socketToPipeR, socketToPipeW = os.pipe()  
pipeToSocketR, pipeToSocketW = os.pipe()

stop = threading.Event()                        # Stop event for killing threads

# Start the proxy server so can connect an external client
print("***Starting proxy server...")

proxy = proxy('127.0.0.1', Secrets.proxy_port, socketToPipeW, pipeToSocketR, stop)
print("***     Proxy started.")
       
pipeToSocketW = os.fdopen(pipeToSocketW, 'wb')
proxyRxThread = threading.Thread(target=proxy.receive)
proxyRxThread.start()
print("***     Received thread started.")

RxThread = threading.Thread(target=receive_handler)
RxThread.start()
print("***     Received thread started.")

print("***Proxy server complete.")

# Connect via telent
print("***Starting telnet session...")
telnetSess = Session(pipeToSocketW, socketToPipeR, stop)
handlePipeThread = threading.Thread(target=transmit_handler)
handlePipeThread.start()

print("***     Logging in...")
telnetSess.login()



print("***Telnet init complete.")
telnetSess.run()
#receive_handler()




