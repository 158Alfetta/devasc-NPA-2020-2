"""Router"""
class Router:
    
    """create router"""
    def __init__(self, brand, model, hostname):
        self.brand = brand
        self.model = model
        self.hostname = hostname
        self.interfaces = []
    
    def addInterface(self, interface):
        self.interfaces.append(
            {
                "interface":interface,
                "n_hostname":'',
                "n_interface":'',
                "n_platform":'',
                "n_object":''
            }
        )

    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        for i in self.interfaces:
            print("Interface :"+i['interface'])
        print("---------------------------------------------------")

    def connect(self, srcInt, dstDevice, dstInt):
        flag = 0
        for i in self.interfaces:
            if i['interface'] == srcInt:
                if i['n_hostname'] != '':
                    self.disconnect(i['interface'])
                    print("!!!!! "+srcInt+" is Disconnected !!!!!")
                i['n_hostname'] = dstDevice.hostname
                i['n_interface'] = dstInt
                i['n_platform'] = dstDevice.brand+" "+dstDevice.model
                i['n_object'] = dstDevice
                flag = 1
        for j in dstDevice.interfaces:
            if j['interface'] == dstInt and flag == 1:
                j['n_hostname'] = self.hostname
                j['n_interface'] = srcInt
                j['n_platform'] = self.brand+" "+self.model
                i['n_object'] = self

    def disconnect(self, interface):
        for i in self.interfaces:
            if i['interface'] == interface:
                next_int = i['n_interface']
                next_dev = i['n_object']
                for j in next_dev.interfaces:
                    if j['interface'] == next_int:
                        j['n_hostname'] = ''
                        j['n_interface'] = ''
                        j['n_platform'] = ''
                        j['n_object'] = ''

    def showCDP(self):
        print("List of directly connected of "+self.hostname)
        print("---------------------------------------------------")
        for i in self.interfaces:
            if i['n_hostname'] != "":
                print("--")
                print("Exit Interface : "+i['interface'])
                print("Next Device ID : "+i['n_hostname'])
                print("Next Interface : "+i['n_interface'])
                print("Platform : "+i['n_platform'])
                print("--")
        print("---------------------------------------------------")

r1 = Router('Cisco', '3745', 'R1')
r1.addInterface('GigabitEthernet0/1')
r1.addInterface('GigabitEthernet0/2')
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
r1.connect('GigabitEthernet0/9', r3, 'GigabitEthernet0/1')
r1.showCDP()
r2.showCDP()
r3.showCDP()
        