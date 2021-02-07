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
    
    def addInterface(self, interface):

        self.interfaces[interface] = {
                "n_hostname":'',
                "n_interface":'',
                "n_platform":'',
                "n_object":'',
                "status":'Down'
                }
        self.addLogs('Add interface '+interface+' on device '+self.hostname)

        #self.interfaces['GigabitEthernet0/0']['n_hostname']
    
    def addLogs(self, event):
        self.logs.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f ')+event)
#        print('EVENT: '+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f ')+event)

    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        for i in [*self.interfaces]:
            print(i+' STATUS: '+self.interfaces[i]['status'])
        print("---------------------------------------------------")

    def connect(self, srcInt, dstDevice, dstInt):

        if not (self.isInterface(srcInt)) or not (dstDevice.isInterface(dstInt)):
            self.addLogs("invalid Interface")
            return False
        

        """check current connected interface of src""" 
        # if it connnected will autodisconnect on srcInt and DstInt of current srcInt interface
        if self.interfaces[srcInt]['n_hostname'] != '':
            self.interfaces[srcInt]["n_object"].disconnect(self.interfaces[srcInt]["n_interface"])
            self.disconnect(srcInt)

        """check current connected interface of dst""" 
        # if it connnected will autodisconnect
        if dstDevice.interfaces[dstInt]['n_hostname'] != '':
            dstDevice.interfaces[dstInt]["n_object"].disconnect(dstDevice.interfaces[dstInt]["n_interface"])
            dstDevice.disconnect(dstInt)
        
        self.interfaces[srcInt] = {
            "n_hostname":dstDevice.hostname,
            "n_interface":dstInt,
            "n_platform":dstDevice.brand+" "+dstDevice.model,
            "n_object":dstDevice,
            "status":'Up'
        }

        dstDevice.interfaces[dstInt] = {
            "n_hostname":self.hostname,
            "n_interface":srcInt,
            "n_platform":self.brand+" "+self.model,
            "n_object":self,
            "status":'Up'
        }

        self.addLogs('Interface '+srcInt+' is Up')
        dstDevice.addLogs('Interface '+dstInt+' is Up')
        self.addLogs('Connection between '+self.hostname+' to '+dstDevice.hostname+' via '+ srcInt + ' was successfully created')


    def disconnect(self, interface):
        self.interfaces[interface]['n_hostname'] = ''
        self.interfaces[interface]['n_interface'] = ''
        self.interfaces[interface]['n_platform'] = ''
        self.interfaces[interface]['n_object'] = ''
        self.interfaces[interface]['status'] = 'Down'

        self.addLogs(interface+" of router "+self.hostname+" is DISCONNECT!!")
        self.addLogs('Interface '+interface+' is Down')

    def removeInt(self, interface):
        self.interfaces[interface]["n_object"].disconnect(self.interfaces[interface]["n_interface"])
        self.disconnect(interface)
        self.interfaces.pop(interface, None)
        self.addLogs("Interface "+interface+" on Device "+self.hostname+" was REMOVED!!!.")


    def isInterface(self, interface):
        if interface in self.interfaces:
            return True
        else:
            return False

    # def removeInterface(self):
    
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

