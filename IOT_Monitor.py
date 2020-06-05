#TODO List: 
#   Handle disconnects
#
#---------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------
from Proxy import proxy
from Telnet import Session

import Secrets 
from Bot import Bot
import os
import threading


#---------------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
def receive_handler():
    ''' Receives data from the devices and parses it with the bot.
        Bot output and device data are passed through to the proxy and 
        the bot output (if any) is sent back to the device. 
    '''
    print("receive_handler starting...")
    while not stop.is_set():
        data = os.read(pipeDeviceOutputRead, 4096)
        if not data:
            print("EOF from pipe")
            break
        else:
            dataBot.take_device_input(data)
            proxy.transmit(data)

    print("\n\n*** Receive_handler, stop set.")

#---------------------------------------------------------------------------------
def transmit_handler():
    ''' Thread function to transmit data from the bot/proxy to the device.
        This data is received via a pipe which is written to by the bot or proxy connection.
    '''
    data = b''  # to handle partial lines
    while not stop.is_set():
        try:
            data += os.read(pipeProxyOutputRead, 4096)

            lines = data.split(b'\n')
            if lines[-1] != '':  # received partial line, don't process
                data = lines[-1]
            else:
                data = b''
            lines = lines[:-1]  # chop off either the last empty line, or the partial line

            for line in lines:
                line = line.decode('utf-8')
                if line[-1] == '\r':
                    line = line[:-1]

                response = dataBot.take_proxy_input(line)
                if(not response): #No response, so pass this through to session
                    telnetSess.handle_output_line(line)
                else:
                    for line in response:
                        proxy.transmit(line.encode())

            
        except EOFError:
            telnetSess.log("EOF in pipe")
            print("\n\n*** ERROR:  EOF in transmit_handler pipe.")
            stop.set()


#---------------------------------------------------------------------------------
# Main Code 
#---------------------------------------------------------------------------------
print("--------------------------------------------------------------------------")
print("Running Bot")
print("--------------------------------------------------------------------------")

# Create pipes for moving the data
# The way these definitions work is to define a reader and a writer side.  These pairs
# are used to read and write through the pipe.
pipeProxyOutputRead, pipeProxyOutputWrite = os.pipe()  
pipeDeviceOutputRead, pipeDeviceOutputWrite = os.pipe()

stop = threading.Event()                        # Stop event for killing threads

# Start the proxy server so can connect an external client
print("***Starting proxy server...")

proxy = proxy('127.0.0.1', Secrets.proxy_port, pipeProxyOutputWrite, pipeDeviceOutputRead, stop)
print("***     Proxy started.")
       
pipeDeviceOutputWrite = os.fdopen(pipeDeviceOutputWrite, 'wb')
proxyRxThread = threading.Thread(target=proxy.receive)
proxyRxThread.start()
print("***     Received thread started.")

RxThread = threading.Thread(target=receive_handler)
RxThread.start()
print("***     Received thread started.")

print("***Proxy server complete.")

# Connect via telent
print("***Starting telnet session...")
telnetSess = Session(pipeDeviceOutputWrite, pipeProxyOutputRead, stop)
handlePipeThread = threading.Thread(target=transmit_handler)
handlePipeThread.start()

dataBot = Bot()

print("***     Logging in...")
telnetSess.login()

print("***Telnet init complete.")
telnetSess.run()
#receive_handler()




