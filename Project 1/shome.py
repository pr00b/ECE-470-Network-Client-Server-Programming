from enum import Enum
from pickle import TRUE

class SHome(object):
    DSTATE = Enum('DSTATE', {'ON': 'ON', 'OFF': 'OFF', 'LOCKED': 'LOCKED', 'OPEN': 'OPEN', 'ARMED': 'ARMED', 'DISARMED': 'DISARMED'})
    COLORS = Enum('COLORS', {'RED': 'RED', 'GREEN': 'GREEN', 'BLUE': 'BLUE', 'WHITE': 'WHITE', 'DIM': 'DIM', 'BRIGHT': 'BRIGHT'})
    CRLF = '\r\n'

    def __init__(self):
        self._username = 'admin'
        self._password = 'root'
        self._pin = '1234'
        self._alarmPin = '4321'
        self._lights = dict()
        self._lightcolors = dict()
        self._lightbright = dict()
        self._locks = dict()
        self._alarm = dict()
        
    def __str__(self) -> str:
        return (SHome.CRLF.join(self.getLights()), SHome.CRLF.join(self.getLocks()), SHome.CRLF.join(self.getAlarm()))

    def makeDevices(self):
        self.addLight('Living Room Light 1')
        self.addLight('Living Room Light 2')
        self.addLight('Living Room Light 3')
        self.addLight('Bedroom Light 1')
        self.addLight('Bedroom Light 2')
        self.addLock('Front Door Lock')
        self.addLock('Office Lock')
        self.addLock('Bedroom Lock')
        self.addLock('Cabinet Lock')
        self.addAlarm('Home Security Alarm')

    def checkLogin(self, u: str, p: str) -> bool:
        ret = False
        if u == self._username and p == self._password:
            ret = True
        return ret

    def checkPin(self, p: str) -> bool:
        ret = False
        if p == self._pin:
            ret = True
        return ret

    def checkAlarmPin(self, p: str) -> bool:
        ret = False
        if p == self._alarmPin:
            ret = True
        return ret

    def addLight(self, dname: str):
        self._lights[dname] = SHome.DSTATE.OFF
        self._lightcolors[dname] = SHome.COLORS.WHITE
        self._lightbright[dname] = SHome.COLORS.BRIGHT

    def addLock(self, dname: str):
        self._locks[dname] = SHome.DSTATE.LOCKED

    def addAlarm(self, dname: str):
        self._alarm[dname] = SHome.DSTATE.DISARMED

    def setLightState(self, dname: str, state: str):
        if dname in self._lights:
            self._lights[dname] = SHome.DSTATE[state]

    def setLightColor(self, dname: str, state: str):
        if dname in self._lightcolors:
            self._lightcolors[dname] = SHome.COLORS[state]

    def setLightBrightness(self, dname: str, state: str):
        if dname in self._lights:
            self._lightbright[dname] = SHome.COLORS[state]

    def setLockState(self, dname: str, state: str):
        if dname in self._locks:
            self._locks[dname] = SHome.DSTATE[state]

    def setAlarmState(self, dname: str, state: str):
        if dname in self._alarm:
            self._alarm[dname] = SHome.DSTATE[state]

    def toggleLightState(self, dname: str):
        if dname in self._lights:
            if self._lights[dname] == SHome.DSTATE.OFF:
                self._lights[dname] = SHome.DSTATE.ON
            else:
                self._lights[dname] = SHome.DSTATE.OFF

    def toggleLightStateAll(self):
        for light in self._lights:
            if self._lights[light] == SHome.DSTATE.OFF:
                self._lights[light] = SHome.DSTATE.ON
            else:
                self._lights[light] = SHome.DSTATE.OFF

    def toggleLightColorsAll(self):
        for light in self._lightcolors:
            if self._lightcolors[light] == SHome.COLORS.WHITE:
                self._lightcolors[light] = SHome.COLORS.RED
            elif self._lightcolors[light] == SHome.COLORS.RED:
                self._lightcolors[light] = SHome.COLORS.BLUE
            elif self._lightcolors[light] == SHome.COLORS.BLUE:
                self._lightcolors[light] = SHome.COLORS.GREEN
            elif self._lightcolors[light] == SHome.COLORS.GREEN:
                self._lightcolors[light] = SHome.COLORS.WHITE
            else:
                self._lightcolors[light] = SHome.COLORS.WHITE

    def toggleLightBrightnessAll(self):
        for light in self._lightbright:
            if self._lightbright[light] == SHome.COLORS.BRIGHT:
                self._lightbright[light] = SHome.COLORS.DIM
            else:
                self._lightbright[light] = SHome.COLORS.BRIGHT

    def toggleLockState(self, dname: str):
        if dname in self._locks:
            if self._locks[dname] == SHome.DSTATE.LOCKED:
                self._locks[dname] = SHome.DSTATE.OPEN
            else:
                self._locks[dname] = SHome.DSTATE.LOCKED

    def toggleLockStateAll(self):
        for lock in self._locks:
            if self._locks[lock] == SHome.DSTATE.LOCKED:
                self._locks[lock] = SHome.DSTATE.OPEN
            else:
                self._locks[lock] = SHome.DSTATE.LOCKED

    def toggleAlarmState(self, dname: str):
        if dname in self._alarm:
            if self._alarm[dname] == SHome.DSTATE.DISARMED:
                self._alarm[dname] = SHome.DSTATE.ARMED
            else:
                self._alarm[dname] = SHome.DSTATE.DISARMED

    def toggleLightColor(self, dname: str):
        if dname in self._lightcolors:
            if self._lightcolors[dname] == SHome.COLORS.WHITE:
                self._lightcolors[dname] = SHome.COLORS.RED
            elif self._lightcolors[dname] == SHome.COLORS.RED:
                self._lightcolors[dname] = SHome.COLORS.BLUE
            elif self._lightcolors[dname] == SHome.COLORS.BLUE:
                self._lightcolors[dname] = SHome.COLORS.GREEN
            elif self._lightcolors[dname] == SHome.COLORS.GREEN:
                self._lightcolors[dname] = SHome.COLORS.WHITE
            else:
                self._lightcolors[dname] = SHome.COLORS.WHITE

    def toggleLightBrightness(self, dname: str):
        if dname in self._lightbright:
            if self._lightbright[dname] == SHome.COLORS.BRIGHT:
                self._lightbright[dname] = SHome.COLORS.DIM
            else:
                self._lightbright[dname] = SHome.COLORS.BRIGHT

    def getAll(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {} is {}, {}, {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        for lock in self._locks:
            ret.append('{:>3}. {} is {}'.format(i, lock, self._locks[lock].value))
            i += 1
        for alarm in self._alarm:
            ret.append('{:>3}. {} is {}'.format(i, alarm, self._alarm[alarm].value))
            i += 1
        return ret

    def getListOfAll(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        for lock in self._locks:
            ret.append('{:>3}. {}'.format(i, lock, self._locks[lock].value))
            i += 1
        for alarm in self._alarm:
            ret.append('{:>3}. {}'.format(i, alarm, self._alarm[alarm].value))
            i += 1
        return ret

    def getLights(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {} is {}, {}, {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret

    def getLightList(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret

    def getLightLivingRoomList(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret[0:3]

    def getLightBedRoomList(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret[3:5]

    def getCheckLivingRoomLights(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {} is {}, {}, {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret[0:3]

    def getCheckBedRoomLights(self) -> list:
        ret = []
        i = 1
        for light in self._lights:
            ret.append('{:>3}. {} is {}, {}, {}'.format(i,light,self._lights[light].value,self._lightcolors[light].value,self._lightbright[light].value))
            i += 1
        return ret[3:5]

    def getLockList(self) -> list:
        ret = []
        i = 1
        for lock in self._locks:
            ret.append('{:>3}. {}'.format(i, lock, self._locks[lock].value))
            i += 1
        return ret

    def getAlarmList(self) -> list:
        ret = []
        i = 1
        for alarm in self._alarm:
            ret.append('{:>3}. {}'.format(i, alarm, self._alarm[alarm].value))
            i += 1
        return ret

    def getLocks(self) -> list:
        ret = []
        i = 1
        for lock in self._locks:
            ret.append('{:>3}. {} is {}'.format(i, lock, self._locks[lock].value))
            i += 1
        return ret

    def getAlarm(self) -> list:
        ret = []
        i = 1
        for alarm in self._alarm:
            ret.append('{:>3}. {} is {}'.format(i, alarm, self._alarm[alarm].value))
            i += 1
        return ret

    def getDLights(self) -> dict:
        ret = {}
        i = 1
        for light in self._lights:
            ret[str(i)] = light
            i += 1
        return ret

    def getDLocks(self) -> dict:
        ret = {}
        i = 1
        for lock in self._locks:
            ret[str(i)] = lock
            i += 1
        return ret

    def getDAlarm(self) -> dict:
        ret = {}
        i = 1
        for alarm in self._alarm:
            ret[str(i)] = alarm
            i += 1
        return ret
