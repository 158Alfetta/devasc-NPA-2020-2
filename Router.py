"""Router"""
class Router:
    
    """create router"""
    def __init__(self, brand, model, hostname):
        self.brand = brand
        self.model = model
        self.hostname = hostname
        self.interfaces = {}
        self.name_interfaces = []
    
    def addInterface(self, interface):

        self.interfaces[interface] = {
                "n_hostname":'',
                "n_interface":'',
                "n_platform":'',
                "n_object":''
                }
        
        #self.interfaces['GigabitEthernet0/0']['n_hostname']

    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        print(*self.interfaces, sep='\n')
        print("---------------------------------------------------")

    def connect(self, srcInt, dstDevice, dstInt):

        if not (self.isInterface(srcInt)) or not (dstDevice.isInterface(dstInt)):
            print("Invalid Interface")
            return False
        
        if self.interfaces[srcInt]['n_hostname'] != '':
            dstDevice.disconnect(self.interfaces[srcInt]["n_interface"])
            self.disconnect(srcInt)
        
        self.interfaces[srcInt] = {
            "n_hostname":dstDevice.hostname,
            "n_interface":dstInt,
            "n_platform":dstDevice.brand+" "+dstDevice.model,
            "n_object":dstDevice
        }

        dstDevice.interfaces[dstInt] = {
            "n_hostname":self.hostname,
            "n_interface":srcInt,
            "n_platform":self.brand+" "+self.model,
            "n_object":self  
        }



    def disconnect(self, interface):
        self.interfaces[interface]['n_hostname'] = ''
        self.interfaces[interface]['n_interface'] = ''
        self.interfaces[interface]['n_platform'] = ''
        self.interfaces[interface]['n_object'] = ''

        print("!!!!! "+interface+" of router "+self.hostname+" is DISCONNECTED !!!!!")

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
r1.connect('GigabitEthernet0/2', r3, 'GigabitEthernet0/1')
r1.connect('GigabitEthernet0/9', r3, 'GigabitEthernet0/0')
r1.showCDP()
r2.showCDP()
r3.showCDP()
