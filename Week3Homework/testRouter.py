import unittest
from Router import *

class testRouter(unittest.TestCase):
    
    def testAddInterface(self):
        """this case test interface added?"""
        router = Router('Cisco', '3745', 'R1')
        self.assertTrue('GigabitEthernet0/1' in router.addInterface('GigabitEthernet0/1'))

    def testAddDupblicateInterface(self):
        """add interface and data, then add the same name of interface again. Watch out data
        if is lost, Test failed. """
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router2 = Router('Cisco', '2600', 'R2')
        router2.addInterface('GigabitEthernet0/2')
        router.connect('GigabitEthernet0/1', router2, 'GigabitEthernet0/2')
        #test by watching a next interface data of interface 'GigabitEthernet0/1' if it exist will be passed away together.
        router.addInterface('GigabitEthernet0/1')
        self.assertTrue('GigabitEthernet0/2' in router.interfaces['GigabitEthernet0/1']["n_interface"])

    def testRemoveInterface(self):
        """ Test Failed if removed interface is still exist after remove process"""
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router.addInterface('GigabitEthernet0/2')
        router.removeInt('GigabitEthernet0/1') #remove process
        self.assertFalse('GigabitEthernet0/1' in router.interfaces)

    def testDirectlyConnect(self):
        """test connent to neighbor interface of neighbor router"""
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router2 = Router('Cisco', '2600', 'R2')
        router2.addInterface('GigabitEthernet0/2')
        router.connect('GigabitEthernet0/1', router2, 'GigabitEthernet0/2')

        #check the next interface between routers is bonded.
        self.assertTrue('GigabitEthernet0/2' in router.interfaces['GigabitEthernet0/1']["n_interface"])
        self.assertTrue('GigabitEthernet0/1' in router2.interfaces['GigabitEthernet0/2']["n_interface"])

        #check next hostname is exist
        self.assertTrue('R2' in router.interfaces['GigabitEthernet0/1']["n_hostname"])
        self.assertTrue('R1' in router2.interfaces['GigabitEthernet0/2']["n_hostname"])

    def testConnectNotExistInt(self):
        """connection will not occur if next interface doesn't exist"""
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router2 = Router('Cisco', '2600', 'R2')
        router.connect('GigabitEthernet0/1', router2, 'GigabitEthernet0/99')
        self.assertFalse('GigabitEthernet0/99' in router.interfaces['GigabitEthernet0/1']["n_interface"])

    def testDisconnect(self):
        """if link is disconnected, interface will go to down state and able to connect with another interface"""
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router2 = Router('Cisco', '2600', 'R2')
        router2.addInterface('GigabitEthernet0/2')
        router3 = Router('Cisco', '7200', 'R2')
        router3.addInterface('GigabitEthernet0/3')
        router.connect('GigabitEthernet0/1', router2, 'GigabitEthernet0/2')

        #router2 go to UP state, due to have any connection.
        self.assertTrue('Up' == router2.interfaces['GigabitEthernet0/2']["status"])
        router.connect('GigabitEthernet0/1', router3, 'GigabitEthernet0/3') 
        #change connection to router3 then router2 will automatically disconnect
        #router1 will have datail for connection to router3
        self.assertTrue('GigabitEthernet0/3' in router.interfaces['GigabitEthernet0/1']["n_interface"])
        #router2 interface will go to down state, due to not have any connection.
        self.assertTrue('Down' == router2.interfaces['GigabitEthernet0/2']["status"])
        #interface on router2 have no any data about next interface.
        self.assertTrue('' == router2.interfaces['GigabitEthernet0/2']["n_interface"])

    def testIPAssign(self):
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router.addInterface('GigabitEthernet0/2')
        #validate by checking ip into interface that already assign or not.
        #IP currectly assign, will be true
        router.assignIpaddr('GigabitEthernet0/1', '192.168.1.1/24')
        self.assertTrue('192.168.1.1' == router.interfaces['GigabitEthernet0/1']['ip_address'])

    def testAssignIpOverlap(self):
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router.addInterface('GigabitEthernet0/2')
        #validate by checking ip into interface that already assign or not.
        #IP currectly assign, will be true
        router.assignIpaddr('GigabitEthernet0/1', '192.168.1.1/24')
        self.assertTrue('192.168.1.1' == router.interfaces['GigabitEthernet0/1']['ip_address'])
        #IP overlapped to another network, should be False
        router.assignIpaddr('GigabitEthernet0/2', '192.168.37.24/16')
        self.assertFalse('192.168.37.24' == router.interfaces['GigabitEthernet0/2']['ip_address'])

    def testDuplicateIP(self):
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router.addInterface('GigabitEthernet0/3')
        router.assignIpaddr('GigabitEthernet0/1', '192.168.1.1/24')
        #validate by checking ip into interface that already assign or not.
        #Duplicated ip on exist interface, should be False
        router.assignIpaddr('GigabitEthernet0/3', '192.168.1.1/24')
        self.assertFalse('192.168.1.1' == router.interfaces['GigabitEthernet0/3']['ip_address'])
    
    def testFaultAssignIP(self):
        #assign IP Address 888.888.445.134/24 to an interface
        #script will go to error (unable to assign wrong format IP Address).
        router = Router('Cisco', '3745', 'R1')
        router.addInterface('GigabitEthernet0/1')
        router.assignIpaddr('GigabitEthernet0/1', '888.888.445.134/24')
        self.assertTrue('888.888.445.134' != router.interfaces['GigabitEthernet0/1']['ip_address'])



if __name__ == '__main__':
    unittest.main()