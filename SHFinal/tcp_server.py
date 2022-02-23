'''
Created on Feb 19, 2021

@author: nigel
'''

import socket
from shprotocol import SHProtocol
from shserver import SHServer

if __name__ == '__main__':
    # create the server socket
    #  defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    serversoc = socket.socket()
    
    # bind to local host:5000
    serversoc.bind(("localhost",50000))
                   
    # make passive with backlog=5
    serversoc.listen(5)
    
    # wait for incoming connections
    while True:
        print("Listening on ", 50000)
        
        # accept the connection
        commsoc, raddr = serversoc.accept()
        
        # run the application protocol
        shp = SHProtocol(commsoc)
        shs = SHServer(shp)
        shs.run()
        
        # close the comm socket
        commsoc.close()
    
    # close the server socket
    serversoc.close()