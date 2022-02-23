'''
Created on Feb 19, 2021

@author: nigel
'''

import socket
from shprotocol import SHProtocol
from shclient import SHClient

if __name__ == '__main__':
    # create the socket
    #  defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    commsoc = socket.socket()
    
    # connect to localhost:5000
    commsoc.connect(("localhost",50000))
    
    # run the application protocol
    shp = SHProtocol(commsoc)
    shc = SHClient(shp)
    shc.run()
    
    # close the comm socket
    commsoc.close()