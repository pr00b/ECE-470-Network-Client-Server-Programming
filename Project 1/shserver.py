from message import Message
from shprotocol import SHProtocol
from shome import SHome

class SHServer(object):

    def __init__(self, s: SHProtocol):

        self._shp = s
        self._login = False
        self._mLevel = 'main'
        self._home = SHome()
        self._home.makeDevices()
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
                ms.addLine('Username:')
            
                self._shp.putMessage(ms)
            
                mr = self._shp.getMessage()
                user = mr.getParam('user')
            
                ms.reset()
                ms.setType('PASS')
                ms.addParam('pnum','1')
                ms.addParam('1','pass')
                ms.addLine('Password:')
            
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
            menu = ['1. List Devices', '2. Check Device Status','3. Change Devices Status', '99. Logout']
            choices = {'1': 'listMenu', '2': 'checkMenu', '3': 'changeMenu', '99': 'logout'}

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

    def _doListMenu(self):
        try:
            listMenu = ['1. List All Devices', '2. List Lights', '3. List Locks', '4. List Alarms', '5. List Group']
            listChoice = {'1': 'listAll', '2': 'listLights', '3': 'listLocks', '4': 'listAlarm', '5': 'listGroup'}
            listMenu.append('99. Return to Main Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(listMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in listChoice:
                self._mLevel = listChoice[choice]
            else:
                self._mLevel = 'main'

        except Exception:
            self.shutdown()
        else:
            return

    def _doGroupListMenu(self):
        try:
            listGroupMenu = ['1. Living Room', '2. Bedroom']
            listChoice = {'1': 'LRList', '2': 'BRList'}
            listGroupMenu.append('99. Return to List Devices Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(listGroupMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in listChoice:
                self._mLevel = listChoice[choice]
            else:
                self._mLevel = 'main'

        except Exception:
            self.shutdown()
        else:
            return

    def _doLRList(self):
        try:
            menu = self._home.getLightLivingRoomList()
            menu.append('99. Return to List Group Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doBRList(self):
        try:
            menu = self._home.getLightBedRoomList()
            menu.append('99. Return to List Group Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doCheckMenu(self):
        try:
            checkMenu = ['1. Check All Devices', '2. Check Light Status', '3. Check Lock Status', '4. Check Alarm Status', '5. Check Group Status']
            checkChoice = {'1': 'checkAll', '2': 'displayLights', '3': 'displayLocks', '4': 'displayAlarm', '5': 'checkGroup'}
            checkMenu.append('99. Return to Main Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(checkMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in checkChoice:
                self._mLevel = checkChoice[choice]
            else:
                self._mLevel = 'main'

        except Exception:
            self.shutdown()
        else:
            return

    def _doCheckGroup(self):
        try:
            checkGroup = ['1. Living Room', '2. Bedroom']
            checkChoice = {'1': 'LRCheck', '2': 'BRCheck'}
            checkGroup.append('99. Return to Check Device Status Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(checkGroup)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in checkChoice:
                self._mLevel = checkChoice[choice]
            else:
                self._mLevel = 'checkMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doLRCheck(self):
        try:
            menu = self._home.getCheckLivingRoomLights()
            menu.append('99. Return to Check Group Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doBRCheck(self):
        try:
            menu = self._home.getCheckBedRoomLights()
            menu.append('99. Return to Check Group Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeMenu(self):
        try:
            changeMenu = ['1. Change Light Status', '2. Change Lock Status', '3. Change Alarm Status', '4. Change Group Status']
            changeChoice = {'1': 'changeLightMenu', '2': 'changeLockMenu', '3': 'changeAlarm', '4': 'changeGroup'}
            changeMenu.append('99. Return to Main Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(changeMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in changeChoice:
                self._mLevel = changeChoice[choice]
            else:
                self._mLevel = 'main'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLockMenu(self):
        try:
            changeMenu = ['1. Lock/Open Locks', '2. Lock/Open All Locks']
            changeChoice = {'1': 'changeLocks', '2': 'changeAllLocks'}
            changeMenu.append('99. Return to Main Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(changeMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in changeChoice:
                self._mLevel = changeChoice[choice]
            else:
                self._mLevel = 'changeMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeGroup(self):
        try:
            checkGroup = ['1. Living Room', '2. Bedroom']
            checkChoice = {'1': 'changeLightMenuGroupLR', '2': 'changeLightMenuGroupBR'}
            checkGroup.append('99. Return to Check Device Status Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(checkGroup)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in checkChoice:
                self._mLevel = checkChoice[choice]
            else:
                self._mLevel = 'changeMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doLRChange(self):
        try:
            menu = self._home.getCheckLivingRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightState(choices[choice])
                self._mLevel = 'LRChange'
            else:
                self._mLevel = 'changeLightMenuGroupLR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightColorLR(self):
        try:
            menu = self._home.getCheckLivingRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightColor(choices[choice])
                self._mLevel = 'changeLightColorLR'
            else:
                self._mLevel = 'changeLightMenuGroupLR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightBrightLR(self):
        try:
            menu = self._home.getCheckLivingRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightBrightness(choices[choice])
                self._mLevel = 'changeLightBrightLR'
            else:
                self._mLevel = 'changeLightMenuGroupLR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doBRChange(self):
        try:
            menu = self._home.getCheckBedRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightState(choices[choice])
                self._mLevel = 'BRChange'
            else:
                self._mLevel = 'changeLightMenuGroupBR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightColorBR(self):
        try:
            menu = self._home.getCheckBedRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightColor(choices[choice])
                self._mLevel = 'changeLightColorBR'
            else:
                self._mLevel = 'changeLightMenuGroupBR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightBrightBR(self):
        try:
            menu = self._home.getCheckBedRoomLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightBrightness(choices[choice])
                self._mLevel = 'changeLightBrightBR'
            else:
                self._mLevel = 'changeLightMenuGroupBR'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightMenu(self):
        try:
            changeLightMenu = ['1. Turn On/Off', '2. Change Color', '3. Change Brightness', '4. Turn All On/Off', '5. Change All Colors', '6. Change All Brightness']
            changeLMChoice = {'1': 'changeLights', '2': 'changeLightColors', '3': 'changeLightBrightness', '4': 'changeAllLights','5': 'changeAllColors', '6': 'changeAllBrightness'}
            changeLightMenu.append('99. Return to Change Device Status Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(changeLightMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in changeLMChoice:
                self._mLevel = changeLMChoice[choice]
            else:
                self._mLevel = 'changeMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightMenuGroupLR(self):
        try:
            changeLightMenu = ['1. Turn On/Off', '2. Change Color', '3. Change Brightness']
            changeLMChoice = {'1': 'LRChange', '2': 'changeLightColorLR', '3': 'changeLightBrightLR'}
            changeLightMenu.append('99. Return to Change Device Status Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(changeLightMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in changeLMChoice:
                self._mLevel = changeLMChoice[choice]
            else:
                self._mLevel = 'changeGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightMenuGroupBR(self):
        try:
            changeLightMenu = ['1. Turn On/Off', '2. Change Color', '3. Change Brightness']
            changeLMChoice = {'1': 'BRChange', '2': 'changeLightColorBR', '3': 'changeLightBrightBR'}
            changeLightMenu.append('99. Return to Change Device Status Menu')

            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(changeLightMenu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            self._debugPrint(mr)
            choice = mr.getParam('choice')
            if choice in changeLMChoice:
                self._mLevel = changeLMChoice[choice]
            else:
                self._mLevel = 'changeGroup'

        except Exception:
            self.shutdown()
        else:
            return

    def _doListAll(self):
        try:
            menu = self._home.getListOfAll()
            menu.append('99. Return to List Devices Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doCheckAll(self):
        try:
            menu = self._home.getAll()
            menu.append('99. Return to Check Device Status Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doDisplayLights(self):
        try:
            menu = self._home.getLights()
            menu.append('99. Return to Check Device Status Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum','1')
            ms.addParam('1','choice')
            ms.addLines(menu)
            
            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkMenu'
                
        except Exception:
            self.shutdown()
        else:
            return

    def _doDisplayLocks(self):
        try:
            menu = self._home.getLocks()
            menu.append('99. Return to Check Device Status Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doDisplayAlarm(self):
        try:
            menu = self._home.getAlarm()
            menu.append('99. Return to Check Device Status Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'checkMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doLightsList(self):
        try:
            menu = self._home.getLightList()
            menu.append('99. Return to List Devices Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doLocksList(self):
        try:
            menu = self._home.getLockList()
            menu.append('99. Return to List Devices Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doAlarmList(self):
        try:
            menu = self._home.getAlarmList()
            menu.append('99. Return to List Devices Menu')
            choices = {'99': 'main'}
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()

            self._mLevel = 'listMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLights(self):
        try:
            menu = self._home.getLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightState(choices[choice])
                self._mLevel = 'changeLights'
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeAllLights(self):
        try:
            menu = self._home.getLights()
            menu.append('1. Turn all On/Off\n'
                        '99. Return to Change Light Status Menu')
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice == '1':
                self._home.toggleLightStateAll()
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeAllColors(self):
        try:
            menu = self._home.getLights()
            menu.append('1. Cycle through colors for all\n'
                        '99. Return to Change Light Status Menu')
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice == '1':
                self._home.toggleLightColorsAll()
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeAllBrightness(self):
        try:
            menu = self._home.getLights()
            menu.append('1. Change all brightness\n'
                        '99. Return to Change Light Status Menu')
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice == '1':
                self._home.toggleLightBrightnessAll()
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightColors(self):
        try:
            menu = self._home.getLights()
            menu.append('NOTE: Cycle through colors for each by entering their corresponding number multiple times\n'
                        '99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightColor(choices[choice])
                self._mLevel = 'changeLightColors'
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLightBright(self):
        try:
            menu = self._home.getLights()
            menu.append('99. Return to Change Light Status Menu')
            choices = self._home.getDLights()
            ms = Message()
            ms.setType('MENU')
            ms.addParam('pnum', '1')
            ms.addParam('1', 'choice')
            ms.addLines(menu)

            self._shp.putMessage(ms)
            mr = self._shp.getMessage()
            choice = mr.getParam('choice')
            if choice in choices:
                self._home.toggleLightBrightness(choices[choice])
                self._mLevel = 'changeLightBrightness'
            else:
                self._mLevel = 'changeLightMenu'

        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeLocks(self):
        try:
            self._doPin()
            while self._pin:
                menu = self._home.getLocks()
                menu.append('99. Return to Change Lock Status Menu')
                choices = self._home.getDLocks()
                ms = Message()
                ms.setType('MENU')
                ms.addParam('pnum', '1')
                ms.addParam('1', 'choice')
                ms.addLines(menu)

                self._shp.putMessage(ms)
                mr = self._shp.getMessage()
                choice = mr.getParam('choice')
                if choice in choices:
                    self._home.toggleLockState(choices[choice])
                    self._mLevel = 'changeLockMenu'
                else:
                    break

            self._mLevel = 'changeLockMenu'
        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeAllLocks(self):
        try:
            self._doPin()
            while self._pin:
                menu = self._home.getLocks()
                menu.append('1. Lock/Open all\n'
                            '99. Return to Change Lock Status Menu')
                ms = Message()
                ms.setType('MENU')
                ms.addParam('pnum', '1')
                ms.addParam('1', 'choice')
                ms.addLines(menu)

                self._shp.putMessage(ms)
                mr = self._shp.getMessage()
                choice = mr.getParam('choice')
                if choice == '1':
                    self._home.toggleLockStateAll()
                else:
                    break

            self._mLevel = 'changeLockMenu'
        except Exception:
            self.shutdown()
        else:
            return

    def _doChangeAlarm(self):
        try:
            self._doAlarmPin()
            while self._alarmPin:
                menu = self._home.getAlarm()
                menu.append('99. Return to Change Device Status Menu')
                choices = self._home.getDAlarm()
                ms = Message()
                ms.setType('MENU')
                ms.addParam('pnum', '1')
                ms.addParam('1', 'choice')
                ms.addLines(menu)

                self._shp.putMessage(ms)
                mr = self._shp.getMessage()
                choice = mr.getParam('choice')
                if choice in choices:
                    self._home.toggleAlarmState(choices[choice])
                    self._mLevel = 'changeMenu'
                else:
                    break

            self._mLevel = 'changeMenu'
        except Exception:
            self.shutdown()
        else:
            return

    def _doPin(self):
        self._pin = False
        count = 0
        try:
            while not self._pin:
                ms = Message()
                ms.setType('PIN')
                ms.addParam('pnum', '1')
                ms.addParam('1', 'pin')
                ms.addLine('Enter lock pin:')
                self._shp.putMessage(ms)
                mr = self._shp.getMessage()
                pin = mr.getParam('pin')

                self._pin = self._home.checkPin(pin)
                count = count + 1
                if count > 2:
                    raise Exception('Too many pin tries')
                self._mLevel = 'changeLocks'
        except Exception as e:
            print('doPin:', e)
            self.shutdown()

    def _doAlarmPin(self):
        self._alarmPin = False
        count = 0
        try:
            while not self._alarmPin:
                ms = Message()
                ms.setType('PIN')
                ms.addParam('pnum', '1')
                ms.addParam('1', 'pin')
                ms.addLine('Enter alarm pin:')
                self._shp.putMessage(ms)
                mr = self._shp.getMessage()
                alarmPin = mr.getParam('pin')

                self._alarmPin = self._home.checkAlarmPin(alarmPin)
                count = count + 1
                if count > 2:
                    raise Exception('Too many alarm pin tries')
                self._mLevel = 'changeAlarm'
        except Exception as e:
            print('doAlarmPin:', e)
            self.shutdown()

    def shutdown(self):
        self._login = False
        self._shp.close()  
        return

    def msgTest(self):
        mr = self._shp.getMessage()
        print(mr)

        ms = Message()
        ms.setType('USER')
        ms.addParam('user', 'none')
        ms.addLine('Username:')

        self._shp.putMessage(ms)

        mr = self._shp.getMessage()
        print(mr)

        ms.reset()
        ms.setType('PASS')
        ms.addParam('pass', 'none')
        ms.addLine('Password:')

        self._shp.putMessage(ms)

        mr = self._shp.getMessage()
        print(mr)

        self._shp.close()

    def run(self):
        try:
            mr = self._shp.getMessage()
            self._debugPrint(mr)

            self._doLogin()
            self._debugPrint('logged in')

            menus = {'main': self._doMainMenu,
                     'displayLights': self._doDisplayLights,
                     'displayLocks': self._doDisplayLocks,
                     'displayAlarm': self._doDisplayAlarm,
                     'changeLights': self._doChangeLights,
                     'changeLocks': self._doChangeLocks,
                     'changeAlarm': self._doChangeAlarm,
                     'changeLightBrightness': self._doChangeLightBright,
                     'changeLightColors': self._doChangeLightColors,
                     'listMenu': self._doListMenu,
                     'listAll': self._doListAll,
                     'listLights': self._doLightsList,
                     'listLocks': self._doLocksList,
                     'listAlarm': self._doAlarmList,
                     'listGroup': self._doGroupListMenu,
                     'LRList': self._doLRList,
                     'BRList': self._doBRList,
                     'LRCheck': self._doLRCheck,
                     'BRCheck': self._doBRCheck,
                     'LRChange': self._doLRChange,
                     'BRChange': self._doBRChange,
                     'checkMenu': self._doCheckMenu,
                     'checkAll': self._doCheckAll,
                     'checkGroup': self._doCheckGroup,
                     'changeMenu': self._doChangeMenu,
                     'changeLightMenu': self._doChangeLightMenu,
                     'changeAllLights': self._doChangeAllLights,
                     'changeAllColors': self._doChangeAllColors,
                     'changeAllBrightness': self._doChangeAllBrightness,
                     'changeLockMenu': self._doChangeLockMenu,
                     'changeAllLocks': self._doChangeAllLocks,
                     'changeLightMenuGroupLR': self._doChangeLightMenuGroupLR,
                     'changeLightColorLR': self._doChangeLightColorLR,
                     'changeLightBrightLR': self._doChangeLightBrightLR,
                     'changeLightMenuGroupBR': self._doChangeLightMenuGroupBR,
                     'changeLightColorBR': self._doChangeLightColorBR,
                     'changeLightBrightBR': self._doChangeLightBrightBR,
                     'changeGroup': self._doChangeGroup,
                     'logout': self.shutdown
                     }
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
