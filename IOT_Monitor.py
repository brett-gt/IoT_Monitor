#TODO List: 
#   Handle disconnects
#
#   Transmitting seems kind of slow, either stick proxy TX in a thread or buffer 
#       data better before transmit.
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
def device_handler():
    ''' Receives data from the devices and parses it with the bot.
        Bot output and device data are passed through to the proxy and 
        the bot output (if any) is sent back to the device. 
    '''
    print("device_handler starting...")
    while not stop.is_set():
        data = os.read(pipeDeviceOutputRead, 4096)
        if not data:
            print("EOF from pipe")
            break
        else:
            text = data.decode(proxy_encode)
            dataBot.take_device_input(text)
            proxy.transmit(data)

    print("\n\n*** Receive_handler, stop set.")

#---------------------------------------------------------------------------------
def proxy_handler():
    ''' Thread function to transmit data from the bot/proxy to the device.
        This data is received via a pipe which is written to by the bot or proxy connection.
    '''
    print("proxy_handler starting...")
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
 
                print(line)
                if line[-1] == '\r':
                    line = line[:-1]

                was_cmd = dataBot.take_proxy_input(line)
                if(not was_cmd): #No response, so pass this through to session
                    telnetSess.handle_output_line(line)
            
        except EOFError:
            telnetSess.log("EOF in pipe")
            print("\n\n*** ERROR:  EOF in transmit_handler pipe.")
            stop.set()


#---------------------------------------------------------------------------------
# Main Code 
#---------------------------------------------------------------------------------
print("--------------------------------------------------------------------------")
print("   Running Bot")
print("--------------------------------------------------------------------------")

proxy_encode = 'UTF-8'

# Create pipes for moving the data
# The way these definitions work is to define a reader and a writer side.  These pairs
# are used to read and write through the pipe.
pipeProxyOutputRead, pipeProxyOutputWrite = os.pipe()  
pipeDeviceOutputRead, pipeDeviceOutputWrite = os.pipe()

stop = threading.Event()                        # Stop event for killing threads

# Start the proxy server so can connect an external client
print("Starting proxy server...")

proxy = proxy('127.0.0.1', Secrets.proxy_port, pipeProxyOutputWrite, pipeDeviceOutputRead, stop)
print("***     Proxy initialized.")
       
pipeDeviceOutputWrite = os.fdopen(pipeDeviceOutputWrite, 'wb')
proxyRxThread = threading.Thread(target=proxy.receive)
proxyRxThread.start()
print("***     Proxy read thread started.")

deviceRxThread = threading.Thread(target=device_handler)
deviceRxThread.start()
print("***     Device read thread started.")

print("Proxy server complete.\n\n")

# Connect via telent
print("Starting telnet session...")

print("***     Starting device...")
telnetSess = Session(pipeDeviceOutputWrite, stop)

print("***     Starting thread to write to device...")
handlePipeThread = threading.Thread(target=proxy_handler)
handlePipeThread.start()

print("***     Starting bot...")
dataBot = Bot(proxy, telnetSess)

print("***     Logging in...")
telnetSess.login()

print("Telnet init complete.\n\n")
telnetSess.run()    #Handles receiving data from Telnet
#receive_handler()




