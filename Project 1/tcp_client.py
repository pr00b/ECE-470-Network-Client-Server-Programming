import socket
from shprotocol import SHProtocol
from shclient import SHClient

if __name__ == '__main__':
    commsoc = socket.socket()
    
    # connect to localhost:5000
    commsoc.connect(("localhost",50000))

    shp = SHProtocol(commsoc)
    shc = SHClient(shp)
    shc.run()

    commsoc.close()
