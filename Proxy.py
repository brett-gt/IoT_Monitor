import queue
import os
import socket
import sys
import threading

from select import select

#TODO: Pull the transmit/receive threads inside this class.  

class proxy(object):
    ''' Crates a proxy that acts as a TCP server.  Connected clients are serviced
        by two seperate threads (threads created external to this) which handle
        receiving and transmitting data.  Data is passed to/from proxy via pipes.
    '''

    #----------------------------------------------------------------------------
    def __init__(self, bindAddr, listenPort, pipeProxyOutput, pipeToSocketR, stop):
        ''' Proxy initialization, sets up listener socket and pipes for reading/writing
        '''
        self.pipeToSocketBuffer = []  # Hold data to be sent to the socket
        self.clientSocket = None      # Placeholder for connections we receive

        self.pipeProxyOutput = pipeProxyOutput
        #self.pipeToSocketR = pipeToSocketR
        self.stop = stop

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Socket server listens to
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((bindAddr, listenPort))
        self.sock.listen(5)


    #----------------------------------------------------------------------------
    def transmit(self, data):
        ''' Thread function to transmit data to the client (either bot to client or device to client)
            This data is received via a pipe which is written to by the bot or telnet connection.
        '''
        if self.clientSocket:
            self.clientSocket.sendall(data)  

        else: #Not currently connected, queue it up
            self.pipeToSocketBuffer.append(data)

    #----------------------------------------------------------------------------
    def receive(self):
        ''' Thread function to transmit data to the device (either bot to device or proxy to device)
            This data is received via a pipe which is written to by the bot or proxy connection.
        '''
        print("Proxy receive thread starting...")
        self.pipeProxyOutput = os.fdopen(self.pipeProxyOutput, 'wb')
        addr = None
        clients = []

        while not self.stop.is_set():
            fds, _, _ = select([self.sock] + clients, [], [])
            for fd in fds:
                #Only allow one connection at a time
                if fd == self.sock:   # New connection
                    print("Proxy.serve: new client")

                    if self.clientSocket:
                        print("Proxy.serve:  booting old client")
                        self.clientSocket.sendall(b"Superseded. Bye!")
                        self.clientSocket.close()

                    self.clientSocket, addr = self.sock.accept()
                    clients = [self.clientSocket]

                    #Send over que data to catch it up
                    for item in self.pipeToSocketBuffer:
                        self.clientSocket.sendall(item)

                    self.pipeToSocketBuffer = []

                elif fd == self.clientSocket:  #Already connected
                    data = fd.recv(4096)
                    if not data:  # disconnect
                        self.clientSocket.close()
                        self.clientSocket = None
                        print("socket disconnected")
                    else:
                        self.pipeProxyOutput.write(data)  # TODO: partial writes?
                        self.pipeProxyOutput.flush()
        print("Gracefully shutting down in serve")

