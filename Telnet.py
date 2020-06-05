from select import select
import importlib
import json
import os
import pprint
import re
import sys
import telnetlib
import threading
import traceback
import Secrets

class Session(object):
    #----------------------------------------------------------------------------
    def __init__(self, pipeDeviceOutputWrite, socketToPipeR, stop):
        self.endpoint_encoding = 'iso-8859-1'
        self.client_encoding = 'utf-8'
        #self.gmcp = {}

        self.pipeDeviceOutputWrite = pipeDeviceOutputWrite
        #self.socketToPipeR = socketToPipeR
        self.stop = stop

        self.host = Secrets.host
        self.port = Secrets.port
       
    #----------------------------------------------------------------------------
    def login(self):
        self.log("Connecting")
        self.telnet = self.connect(self.host, self.port)
        self.log("Connected")
        #TODO: Exception handling

    #----------------------------------------------------------------------------
    def join(self):
        self.thr.join()

    #----------------------------------------------------------------------------
    def log(self, *args, **kwargs):
        if len(args) == 1 and type(args[0]) == str:
            line = args[0]
        else:
            line = pprint.pformat(args)

        print("---------\n")
        print(line)
        print("\n")
        self.pipeDeviceOutputWrite.write("---------\n".encode(self.client_encoding))
        self.pipeDeviceOutputWrite.write(line.encode(self.client_encoding))
        self.pipeDeviceOutputWrite.write(b"\n")
        self.pipeDeviceOutputWrite.flush()

    #----------------------------------------------------------------------------
    def strip_ansi(self, line):
        return re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', line)
  
    #----------------------------------------------------------------------------
    def connect(self, host, port):
        t = telnetlib.Telnet()
        # t.set_debuglevel(1)
        t.open(host, int(port))
        return t

    #----------------------------------------------------------------------------
    def close(self):
        self.log("Telnet: Closing")
        self.telnet.close()

    #----------------------------------------------------------------------------
    def send(self, line):
        print("> ", line)
        self.telnet.write((line + '\n').encode(self.endpoint_encoding))

    #----------------------------------------------------------------------------
    def handle_from_telnet(self):
        try:
            data = self.telnet.read_very_eager()
        except:
            self.log("EOF on telnet")
            self.stopFlag.set()
            raise
        try:
            data = data.decode(self.endpoint_encoding)
        except UnicodeError as e:
            print("Unicode error:", e)
            print("Data was:", data)
            data = ''

        if not data:
            _ = self.telnet.read_sb_data()

        if data != '':
            prn = []
            for line in data.split('\n'):
                prn.append(line)
            self.pipeDeviceOutputWrite.write('\n'.join(prn).encode(self.endpoint_encoding))
            self.pipeDeviceOutputWrite.flush()
    
            #TODO: Test output of received data...
            print('\n'.join(prn))

    #----------------------------------------------------------------------------
    def show(self, line):
        self.pipeDeviceOutputWrite.write(line.encode(self.client_encoding))
        self.pipeDeviceOutputWrite.flush()

    #----------------------------------------------------------------------------
    def handle_from_pipe(self, data):
        lines = data.split(b'\n')
        if lines[-1] != '':  # received partial line, don't process
            data = lines[-1]
        else:
            data = b''
        lines = lines[:-1]  # chop off either the last empty line, or the partial line

        for line in lines:
            line = line.decode(self.client_encoding)
            if line[-1] == '\r':
                line = line[:-1]
            self.handle_output_line(line)

    #----------------------------------------------------------------------------
    def handle_output_line(self, data):
        pprint.pprint(data)
        self.send(data)

    #----------------------------------------------------------------------------
    def run(self):
        ''' Function to continually parse the telnet data
        '''
        try:
            while True:
                self.handle_from_telnet()

        except Exception as e:
            self.log("Exception in run():", e)
        finally:
            self.stop.set()
            self.log("Closing")
            self.telnet.close()

#---------------------------------------------------------------------------------
# UNIT TEST
#---------------------------------------------------------------------------------
def main():
    test = 1

if __name__ == '__main__':
    main()


