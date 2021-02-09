import time
import datetime
import ipcalc

"""Router"""
class Router:
    
    """create router"""
    def __init__(self, brand, model, hostname):
        self.brand = brand
        self.model = model
        self.hostname = hostname
        self.interfaces = {}
        self.logs = []
    
    """add interface into Router"""
    def addInterface(self, interface):
        #create a dict and use interface as a key for interface data

        #check duplicated interface
        if not self.isInterface(interface):
            self.interfaces[interface] = {
                    "n_hostname":'',
                    "n_interface":'',
                    "n_platform":'',
                    "n_object":'',
                    "ip_address":'None',
                    "ip_pool":'None',
                    "status":'Down'
                    }
            self.addLogs('Add interface '+interface+' on device '+self.hostname)
        else:
            self.addLogs('FAIL to add interface '+interface+' on device '+self.hostname+" DUPLICATE INTERFACE FOUND")

        return self.interfaces
    
    """Logs for showing event that occur in the system"""
    def addLogs(self, event):
        #collect them as a list with datetime and event desc.
        self.logs.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f ')+event)\

    """show all interface and status of interface of current device"""
    def showInterface(self):
        print("---------------------------------------------------")
        print("List of Interface of :" + self.hostname)
        for i in [*self.interfaces]:
            print(i+' | STATUS: '+self.interfaces[i]['status']+' | IP_ADDRESS: '+self.interfaces[i]['ip_address'])
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
        # if it connnected will autodisconnect on (destination) source interface and (destination) destination interface.
        if dstDevice.interfaces[dstInt]['n_hostname'] != '':
            dstDevice.interfaces[dstInt]["n_object"].disconnect(dstDevice.interfaces[dstInt]["n_interface"])
            dstDevice.disconnect(dstInt)
            
        # set detail of dict of source interface (current)
        self.interfaces[srcInt] = {
            "n_hostname":dstDevice.hostname,
            "n_interface":dstInt,
            "n_platform":dstDevice.brand+" "+dstDevice.model,
            "n_object":dstDevice,
            "ip_address":dstDevice.interfaces[dstInt]["ip_address"],
            "ip_pool":dstDevice.interfaces[dstInt]["ip_pool"],
            "status":'Up'
        }
        # set detail of dict of destination interface
        dstDevice.interfaces[dstInt] = {
            "n_hostname":self.hostname,
            "n_interface":srcInt,
            "n_platform":self.brand+" "+self.model,
            "n_object":self,
            "ip_address":self.interfaces[srcInt]["ip_address"],
            "ip_pool":self.interfaces[srcInt]["ip_pool"],
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
        self.interfaces[interface]['ip_address'] = ''
        self.interfaces[interface]['ip_pool'] = ''
        self.interfaces[interface]['status'] = 'Down'

        #add logs
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
                print("IP Address : "+self.interfaces[interface]['ip_address'])
                print("Next Device ID : "+self.interfaces[interface]['n_hostname'])
                print("Next Interface : "+self.interfaces[interface]['n_interface'])
                print("Platform : "+self.interfaces[interface]['n_platform'])
                print("--")
        print("---------------------------------------------------")

    """show all log that get from function addLogs"""
    def showLogs(self):
        print("All event in "+self.hostname)
        print("---------------------------------------------------")
        print(*self.logs, sep='\n')
        print("---------------------------------------------------")

    """bind IP Address to the interfaces"""
    def assignIpaddr(self, interface, ip):
        # The input format is a.a.a.a/x where a.a.a.a is ip address and x is subnet mask

        if not (self.isInterface(interface)): #check interface exist.
            self.addLogs("invalid Interface")
            return False

        #create all possibitliy ip in current interface for prevent dubplication.
        ip_pool = [str(x) for x in ipcalc.Network(ip)] 

        if self.interfaces[interface]['ip_address'] == 'None' and not self.isIpaddrExist(ip, interface) and not self.isDuplicateSubnet(ip_pool):
            # assign ip address to interface
            self.interfaces[interface]['ip_address'] = str(ip.split('/')[0]) 
            self.interfaces[interface]['ip_pool'] = ip_pool
            self.addLogs(ip+" was assigned to "+self.hostname+" on interface "+interface+" gracefully.")
        else:
            self.addLogs(ip+" is OVERLAPPED!! for assign to "+interface)

    """check the existing of IP Address"""
    def isIpaddrExist(self, ip, interface):
        for inf in self.interfaces:
            if str(ip.split('/')[0]) in self.interfaces[inf]['ip_pool']:
                #check on just change ip in same interface not duplicate in another.
                if inf == interface: 
                    return False
                #duplicate in another interface
                return True
        #no have duplicate.
        return False

    """check ip with subnet size, is it overlapping?"""
    def isDuplicateSubnet(self, ip_pool):
        for inf in self.interfaces:
            pool_exist = self.interfaces[inf]['ip_pool']
            if pool_exist != 'None':
                # เทียบ pool ของทุก interface เช็คว่าทับกันกับ pool ที่จะเพิ่มมาหรือเปล่า
                res = [x for x in pool_exist if x not in ip_pool]
                # res จะมีสมาชิกที่ไม่ซ้ำกัน ถ้าซ้ำกันคือ empty list คือแสดงว่า pool ของ interface อื่นเป็น subset อยู่
                if len(res) == 0:
                    return True
        return False
    
    """unassign ip of current interface"""
    def unassignIP(self, interface):
        self.interfaces[interface]['ip_address'] = 'None'
        self.interfaces[interface]['ip_pool'] = 'None'

        self.addLogs("Succesfully unassign IP at interface "+interface)
    

# sample of add router 1
# r1 = Router('Cisco', '3745', 'R1')
# r1.addInterface('GigabitEthernet0/1')
# r1.addInterface('GigabitEthernet0/2')
# r1.addInterface('GigabitEthernet0/0')

# sample of add router 2
# r2 = Router('Cisco', 'c7200', 'R2')
# r2.addInterface('GigabitEthernet0/0')
# r2.addInterface('GigabitEthernet0/3')

# sample of assign ip address
# r1.assignIpaddr('GigabitEthernet0/1', '192.168.1.1/24')
# r1.assignIpaddr('GigabitEthernet0/2', '192.168.2.1/24')
# r1.assignIpaddr('GigabitEthernet0/0', '172.16.10.13/16')
# r2.assignIpaddr('GigabitEthernet0/0', '192.168.1.2/24')
# r2.assignIpaddr('GigabitEthernet0/3', '192.168.2.2/24')

# sample of unassign IP Address
#r1.unassignIP('GigabitEthernet0/2', '192.168.2.1/24')

# sample of show interface
# r1.showInterface()
# r2.showInterface()

# sample of connect to interface
# r1.connect('GigabitEthernet0/1', r2 , 'GigabitEthernet0/0')

# disconnect current interface 
# this function will be run automatically when use the same interface to connect to another interface immediatly.
# r1.disconnect('GigabitEthernet0/1')

# Show directly connected interface
# r1.showCDP()
# r2.showCDP()

# Remove interface
# r1.removeInt('GigabitEthernet0/0')

# show all activities occur in system with datetime
# r1.showLogs()
# r2.showLogs()


# sample output of showInterface()
# ---------------------------------------------------
# List of Interface of :R1
# GigabitEthernet0/1 | STATUS: Down | IP_ADDRESS: 192.168.1.1
# GigabitEthernet0/2 | STATUS: Down | IP_ADDRESS: 192.168.2.1
# GigabitEthernet0/0 | STATUS: Down | IP_ADDRESS: 172.16.10.13
# ---------------------------------------------------

# sample output of showLogs()
# ---------------------------------------------------
# All event in R1
# 2021-02-09 16:45:30:542950 Add interface GigabitEthernet0/1 on device R1
# 2021-02-09 16:45:30:542950 Add interface GigabitEthernet0/2 on device R1
# 2021-02-09 16:45:30:542950 Add interface GigabitEthernet0/0 on device R1
# 2021-02-09 16:45:30:551948 192.168.1.1/24 was assigned to R1 on interface GigabitEthernet0/1 gracefully.
# 2021-02-09 16:45:30:780478 192.168.37.24/16 is OVERLAPPED!! for assign to GigabitEthernet0/2
# ---------------------------------------------------

# sample of showCDP()
# List of directly connected of R1
# ---------------------------------------------------
# --
# Exit Interface : GigabitEthernet0/1
# IP Address : 192.168.1.2
# Next Device ID : R2
# Next Interface : GigabitEthernet0/0
# Platform : Cisco c7200
# --
# ---------------------------------------------------