import time
import datetime

"""Router"""
class Router:
    
    """create router"""
    def __init__(self, brand, model, hostname):
        self.brand = brand
        self.model = model
        self.hostname = hostname
        self.interfaces = {}
        self.name_interfaces = []
        self.logs = []
    
    """add interface into Router"""
    def addInterface(self, interface):
        #create a dict and use interface as a key for interface data
        self.interfaces[interface] = {
                "n_hostname":'',
                "n_interface":'',
                "n_platform":'',
                "n_object":'',
                "status":'Down'
                }
        self.addLogs('Add interface '+interface+' on device '+self.hostname)
    
    """Logs for showing event that occur in the system"""
    def addLogs(self, event):
        #collect them as a list with datetime and event desc.
        self.logs.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f ')+event)\

    """show all interface and status of interface of current device"""
    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        for i in [*self.interfaces]:
            print(i+' STATUS: '+self.interfaces[i]['status'])
        print("---------------------------------------------------")

    """create connection of devices"""
    def connect(self, srcInt, dstDevice, dstInt):
        #check interface exist on each router
        if not (self.isInterface(srcInt)) or not (dstDevice.isInterface(dstInt)):
            self.addLogs("invalid Interface")
            return False
        
        # check that interface has a connection before?
        # if it connnected will autodisconnect on source interface and (current exist connection of source interface) destination interface
        if self.interfaces[srcInt]['n_hostname'] != '':
            self.interfaces[srcInt]["n_object"].disconnect(self.interfaces[srcInt]["n_interface"])
            self.disconnect(srcInt)

        # check that interface has a connection before?
        # if it connnected will autodisconnect on (destination) source interface and (destination) destination interface
        if dstDevice.interfaces[dstInt]['n_hostname'] != '':
            dstDevice.interfaces[dstInt]["n_object"].disconnect(dstDevice.interfaces[dstInt]["n_interface"])
            dstDevice.disconnect(dstInt)
            
        # set detail of dict of source interface (current)
        self.interfaces[srcInt] = {
            "n_hostname":dstDevice.hostname,
            "n_interface":dstInt,
            "n_platform":dstDevice.brand+" "+dstDevice.model,
            "n_object":dstDevice,
            "status":'Up'
        }
        # set detail of dict of destination interface
        dstDevice.interfaces[dstInt] = {
            "n_hostname":self.hostname,
            "n_interface":srcInt,
            "n_platform":self.brand+" "+self.model,
            "n_object":self,
            "status":'Up'
        }

        #add logs
        self.addLogs('Interface '+srcInt+' is Up')
        dstDevice.addLogs('Interface '+dstInt+' is Up')
        self.addLogs('Connection between '+self.hostname+' to '+dstDevice.hostname+' via '+ srcInt + ' was successfully created')

    """disconnect the connection between interface (unplug)"""
    def disconnect(self, interface):
        self.interfaces[interface]['n_hostname'] = ''
        self.interfaces[interface]['n_interface'] = ''
        self.interfaces[interface]['n_platform'] = ''
        self.interfaces[interface]['n_object'] = ''
        self.interfaces[interface]['status'] = 'Down'

        self.addLogs(interface+" of router "+self.hostname+" is DISCONNECT!!")
        self.addLogs('Interface '+interface+' is Down')

    """ remove the interface in device"""
    def removeInt(self, interface):
        #disconnect the connection of those interface
        if self.interfaces[interface]['n_hostname'] != '': 
            self.interfaces[interface]["n_object"].disconnect(self.interfaces[interface]["n_interface"])
            self.disconnect(interface)

        #remove dict in interfaces dict by key (name of interface)
        self.interfaces.pop(interface, None)
        self.addLogs("Interface "+interface+" on Device "+self.hostname+" was REMOVED!!!.")

    """check interface is exist return true if it exist"""
    def isInterface(self, interface):
        if interface in self.interfaces:
            return True
        else:
            return False

    """show directly connect"""
    def showCDP(self):
        print("List of directly connected of "+self.hostname)
        print("---------------------------------------------------")
        for interface in [*self.interfaces]:
            if self.interfaces[interface]['n_hostname'] != "":
                print("--")
                print("Exit Interface : "+interface)
                print("Next Device ID : "+self.interfaces[interface]['n_hostname'])
                print("Next Interface : "+self.interfaces[interface]['n_interface'])
                print("Platform : "+self.interfaces[interface]['n_platform'])
                print("--")
        print("---------------------------------------------------")

    def showLogs(self):
        print("All event in "+self.hostname)
        print("---------------------------------------------------")
        print(*self.logs, sep='\n')
        print("---------------------------------------------------")

r1 = Router('Cisco', '3745', 'R1')
r1.addInterface('GigabitEthernet0/1')
r1.addInterface('GigabitEthernet0/2')
r1.addInterface('GigabitEthernet0/0')
r1.showInterface()

r2 = Router('Cisco', 'c7200', 'R2')
r2.addInterface('GigabitEthernet0/0')
r2.addInterface('GigabitEthernet0/3')
r2.showInterface()

r3 = Router('Cisco', 'c2600', 'R3')
r3.addInterface('GigabitEthernet0/0')
r3.addInterface('GigabitEthernet0/1')
r3.showInterface()
        
r1.connect('GigabitEthernet0/1', r2, 'GigabitEthernet0/0')
r1.connect('GigabitEthernet0/2', r3, 'GigabitEthernet0/0')
r1.showCDP()
r2.showCDP()
r3.showCDP()

r1.showLogs()
r1.showInterface()
r1.connect('GigabitEthernet0/2', r2, 'GigabitEthernet0/3')
r2.showLogs()
r2.showInterface()
r3.showLogs()
r3.showInterface()
r1.showLogs()
r1.showInterface()
r1.showCDP()
r3.showCDP()

r1.removeInt('GigabitEthernet0/2')
r1.showInterface()
r1.showCDP()
r1.showLogs()

