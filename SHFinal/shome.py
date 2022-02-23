'''
Created on Feb 23, 2021

@author: nigel
'''
from enum import Enum
from pickle import TRUE

class SHome(object):
    '''
    classdocs
    '''
    DSTATE = Enum('DSTATE', {'ON': 'ON', 'OFF': 'OFF' })
    CRLF = '\r\n'

    def __init__(self):
        '''
        Constructor
        '''
        self._username = 'admin'
        self._password = 'welcome'
        self._lights = dict()
        
    def __str__(self) -> str:
        return (SHome.CRLF.join(self.getLights()))
    
    def mkDummy(self):
        self.addLight('Light 1')
        self.addLight('Light 2')
        self.addLight('Light 3')
        self.addLight('Light 4')
        self.addLight('Light 5')
        
    def checkLogin(self, u: str, p: str) -> bool:
        ret = False
        if u == self._username and p == self._password:
            ret = True
        return ret
        
    def addLight(self, lname: str):
        self._lights[lname] = SHome.DSTATE.OFF
    
    def setLightState(self, lname: str, state: str):
        if lname in self._lights:
            self._lights[lname] = SHome.DSTATE[state]
    
    def toggleLightState(self, lname: str):
        if lname in self._lights:
            if self._lights[lname] == SHome.DSTATE.OFF:
                self._lights[lname] = SHome.DSTATE.ON
            else:
                self._lights[lname] = SHome.DSTATE.OFF
    
    def getLights(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {} is {}'.format(i,light,self._lights[light].value))
            i += 1
        return ret
    
    def getDLights(self) -> dict:
        ret = {}
        i = 1
        for light in self._lights:
            ret[str(i)] = light
            i += 1
        return ret
    