'''
Created on Feb 19, 2021

@author: nigel
'''

import socket
from message import Message

class SHProtocol(object):
    '''
    classdocs
    '''
    CRLF = '\r\n'
    BUFSIZE = 8196


    def __init__(self, s: socket):
        '''
        Constructor
        '''
        self._sock = s
        self._rfile = self._sock.makefile(mode='r',encoding='utf-8',newline=SHProtocol.CRLF)
        
    def _recvLine(self) -> str:
        s = self._rfile.readline()
        if len(s) == 0:
            raise Exception('EOF on _recvLine')
        return s
        
    def putMessage(self, m: Message):
        data = m.marshal()
        self._sock.sendall(data.encode('utf-8'))
    
    def getMessage(self) -> Message:
        try:
            lines = []
            lines.append(self._recvLine())
            lines.append(self._recvLine())
            m = Message()
            m.unmarshal(''.join(lines))
            count = int(m.getParam('lines'))
            for i in range(count):
                m.addLine(self._recvLine())
                
        except Exception:
            raise Exception('bad getMessage')
        else:
            return m
    
    def close(self):
        self._rfile.close()
        self._sock.close()