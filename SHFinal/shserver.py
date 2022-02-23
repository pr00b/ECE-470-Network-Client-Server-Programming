'''
Created on Feb 19, 2021

@author: nigel
'''

from message import Message
from shprotocol import SHProtocol
from shome import SHome

class SHServer(object):
    '''
    classdocs
    '''


    def __init__(self, s: SHProtocol):
        '''
        Constructor
        '''
        self._shp = s
        self._login = False
        self._mLevel = 'main'
        self._home = SHome()
        self._home.mkDummy()
        self._debug = True
        
    def _debugPrint(self, m: str):
        if self._debug:
            print(m)
            
    def _doLogin(self):
        count = 0
        try:
            while not self._login:
                ms = Message()
                ms.setType('USER')
                ms.addParam('pnum','1')
                ms.addParam('1','user')
                ms.addLine('Enter your username:')
            
                self._shp.putMessage(ms)
            
                mr = self._shp.getMessage()
                user = mr.getParam('user')
            
                ms.reset()
                ms.setType('PASS')
                ms.addParam('pnum','1')
                ms.addParam('1','pass')
                ms.addLine('Enter your password:')
            
                self._shp.putMessage(ms)
            
                mr = self._shp.getMessage()
                passw = mr.getParam('pass')
                
                self._login = self._home.checkLogin(user, passw)
                count = count + 1
                if count > 2:
                    raise Exception('Too many login tries')
                self._mLevel = 'main'
                
        except Exception as e:
            print('doLogin:',e)
            self.shutdown()
        else:
            return
    
    def _doMainMenu(self):
        try:
            menu = ['1. Display States','2. Change States', '99. Logout']
            choices = {'1': 'display', '2': 'change', '99': 'logout'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum','1')
            ms.addParam('1','choice')
            ms.addLines(menu)
            
            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in choices:
                self._mLevel = choices[choice]
            else:
                self._mLevel = 'main'
            
        except Exception:
            self.shutdown()
        else:
            return
    
    def _doDisplay(self):
        try:
            menu = self._home.getLights()
            menu.append('99. Return to Main')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum','1')
            ms.addParam('1','choice')
            ms.addLines(menu)
            
            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            
            # always go back to main
            self._mLevel = 'main'
                
        except Exception:
            self.shutdown()
        else:
            return
    
    def _doChange(self):
        try:
            menu = self._home.getLights()
            menu.append('99. Return to Main')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum','1')
            ms.addParam('1','choice')
            ms.addLines(menu)
            
            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightState(choices[choice])
                self._mLevel = 'change'
            else:
                self._mLevel = 'main'
            
        except Exception:
            self.shutdown()
        else:
            return
    
    def shutdown(self):
        self._login = False
        self._shp.close()  
        return    
        
    def test(self):
        mr = self._shp.getMessage()
        print(mr)
        
        ms = Message()
        ms.setType('USER')
        ms.addParam('user', 'none')
        ms.addLine('Enter your username:')
        
        self._shp.putMessage(ms)
        
        mr = self._shp.getMessage()
        print(mr)
        
        ms.reset()
        ms.setType('PASS')
        ms.addParam('pass', 'none')
        ms.addLine('Enter your password:')
        
        self._shp.putMessage(ms)
        
        mr = self._shp.getMessage()
        print(mr)

        self._shp.close()
        
    def run(self):
        try:
            # recv start
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            
            # do login
            self._doLogin()
            self._debugPrint('logged in')
            
            # run the menus
            # a dict with the menu names and the corresponding methods
            menus = {'main': self._doMainMenu,
                     'display': self._doDisplay,
                     'change': self._doChange,
                     'logout': self.shutdown}
            while self._login:
                self._debugPrint('menu level='+self._mLevel)
                m = menus[self._mLevel]
                m()
            
        except Exception as e:
            print('run: shutdown')
            print(e)
            self.shutdown()
        else:
            return
        