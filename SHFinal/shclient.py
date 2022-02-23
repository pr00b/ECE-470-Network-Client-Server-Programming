'''
Created on Feb 19, 2021

@author: nigel
'''

from message import Message
from shprotocol import SHProtocol

class SHClient(object):
    '''
    classdocs
    '''


    def __init__(self, s: SHProtocol):
        '''
        Constructor
        '''
        self._shp = s
        
    def test(self):
        ms = Message()
        ms.setType('START')
        
        self._shp.putMessage(ms)
        
        mr = self._shp.getMessage()
        print(mr.getBody())
        
        choice = input('-->')
        ms.reset()
        ms.setType('CHOICE')
        ms.addParam('user', choice)
         
        self._shp.putMessage(ms)
        
        mr = self._shp.getMessage()
        print(mr.getBody())
        
        choice = input('-->')
        ms.reset()
        ms.setType('CHOICE')
        ms.addParam('pass', choice)
         
        self._shp.putMessage(ms)
        
        self._shp.close()
        
    def run(self):
        # send START
        ms = Message()
        ms.setType('START')
        ms.addParam('pnum','0')
        
        self._shp.putMessage(ms)
        
        try:
            while True:
                mr = self._shp.getMessage()
                print(mr.getBody())
                
                user = input('-->')
                ms.reset()
                ms.setType('CHOICE')
                ms.addParam('pnum','1')
                ms.addParam(mr.getParam('1'), user)
                self._shp.putMessage(ms)
        except Exception:
            self._shp.close()
            
            