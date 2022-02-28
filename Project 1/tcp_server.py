import socket
from shprotocol import SHProtocol
from shserver import SHServer

if __name__ == '__main__':
    serversoc = socket.socket()

    serversoc.bind(("localhost",50000))

    serversoc.listen(5)

    while True:
        print("Listening on ", 50000)

        commsoc, raddr = serversoc.accept()

        shp = SHProtocol(commsoc)
        shs = SHServer(shp)
        shs.run()

        commsoc.close()

    serversoc.close()
