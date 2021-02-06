"""Router"""
class Router:
    
    """create router"""
    def __init__(self, brand, model, hostname):
        self.brand = brand
        self.model = model
        self.hostname = hostname
        self.interfaces = []
        self.name_interfaces = []
    
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
        
        self.name_interfaces.append(interface)

    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        print(*self.name_interfaces, sep='\n')
        print("---------------------------------------------------")

    def connect(self, srcInt, dstDevice, dstInt):
        pos_srcInt = self.isOrderInterface(srcInt)
        pos_dstInt = dstDevice.isOrderInterface(dstInt)

        if pos_dstInt == 'wrong' or pos_dstInt == 'wrong':
            print("Invalid Interface")
            return

        src_interface = self.interfaces[pos_srcInt]
        dst_interface = dstDevice.interfaces[pos_dstInt]

        print(src_interface)
        print(dst_interface)

        if src_interface['n_hostname'] != '':
            self.disconnect(pos_srcInt)
            print("!!!!! "+srcInt+" is Disconnected !!!!!")

        src_interface['n_hostname'] = dst_interface['hostname']
        src_interface['n_interface'] = dst_interface['interface']
        src_interface['n_platform'] = dst_interface['brand']+" "+dstDevice['model']
        # src_interface['n_object'] = dstDevice

        # for i in self.interfaces:
        #     if i['interface'] == srcInt:
        #         if i['n_hostname'] != '':
        #             self.disconnect(i['interface'])
        #             print("!!!!! "+srcInt+" is Disconnected !!!!!")

        #         flag = 1
        # for j in dstDevice.interfaces:
        #     if j['interface'] == dstInt and flag == 1:

        dst_interface['n_hostname'] = src_interface['hostname']
        dst_interface['n_interface'] = src_interface['interface']
        dst_interface['n_platform'] = src_interface['brand']+" "+src_interface['model']
        # dst_interface['n_object'] = self

        # self.interfaces[pos_srcInt] = src_interface
        # dstDevice.interfaces[pos_dstInt] = dst_interface

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

    def isOrderInterface(self, interface):
        if interface in self.name_interfaces:
            return self.name_interfaces.index(interface)
        else:
            return 'wrong'

    # def removeInterface(self):
    
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
