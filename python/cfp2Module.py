import time
import baseclass

class Cfp2(baseclass.BaseAddr16Value16):

    INITIALIZE_STATE = 0x0001
    LOW_POWER_STATE = 0x0002
    HIGH_POWER_UP_STATE = 0x0004
    TX_OFF_STATE = 0x0008
    TX_TURN_ON_STATE = 0x0010
    READY_STATE = 0x0020
    FAULT_STATE = 0x0040
    TX_TURN_OFF_STATE = 0x0080
    HIGH_PWR_DOWN_STATE = 0x0100

    REG_MOD_GEN_CTRL = 0xB010
    REG_MOD_STATE = 0xB016
    REG_MOD_GLB_ALRM = 0xB018
    REG_MOD_GEN_STATUS = 0xB01D
    REG_MOD_FAULT_STATUS = 0xB01E

    
    READY_STATE = 0x20
    FAULT_STATE = 0x40
    TX_OFF_STATE = 0x08
    TX_TURN_ON_STATE = 0x10

    cfpDict = {0x11: "CFP2", 0x12: "CFP4",
               0x14: "CFP2-ACO", 0x15: "CFP8", 0x19: "CFP2-DCO"}

    def __init__(self, bus, phyAddr):
        self.bus = bus
        self.phyAddr = phyAddr
        # PMA/PMD = 1, WIS = 2
        self.devAddr = 1
        baseclass.BaseAddr16Value16.__init__(self)

    def read16(self, regAddr):
        return self.bus.read(self.devAddr, self.phyAddr, regAddr)

    def write16(self, regAddr, value):
        self.bus.write(self.devAddr, self.phyAddr, regAddr, value)

    def printReg(self, regAddr, len=1):
        for i in range(len):
            print("addr 0x%4x" % (regAddr + i), ": %4x" %
                  (self.read16(regAddr + i)))

    def identifier(self):
        """
        Returns the module ID

        Args:
            None

        Returns:
            Module ID 

        Notes:
            None
        """
        mod_id = self.read16(regAddr=0x8000)
        # print("Inserted module is", self.cfpDict[mod_id])
        # print("Inserted module is", mod_id)
        return mod_id

    #--------------------------------------------------------------------------#

    def state(self):
        '''
        Returns the State of the CFP module.

        Args:
            None

        Returns:
            CFP Module State

        Raises:
            None

        Notes:
        '''
        mod_state = self.read16(regAddr=self.REG_MOD_STATE)
        return mod_state
    #--------------------------------------------------------------------------#

    def info(self):
        '''
        Reads CFP module information registers. Note that module registers can not
        be accessed if the module is in reset or initialization state.

        Args:
            None

        Returns:
            Nothing

        Raises:
            Nothing
        '''
        print("="*60)
        print("Module ID                       :\t{}".format(self.identifier()))
        print("Extended ID                     :\t{}".format(self.read16(regAddr=0x8001)))
        power_class_dic = {0:"<=9W",1:"<12W",2:"<=15W",3:">15W"}
        print("Power Class                     :\t{}".format(power_class_dic[self.read16(regAddr=0x8001)>>6]))

       # Number of network and host lanes are help in the upper and lower 4 bits of the register respectively
        num_lanes = self.read16(regAddr=0x8009)
        num_host_lanes = num_lanes & 0x0f
        if num_host_lanes == 0:
            num_host_lanes = 16
        num_lanes = num_lanes >> 4
        num_network_lanes = num_lanes & 0x0f
        if num_network_lanes == 0:
            num_network_lanes = 16
        print("Number of Network Supported     :\t{}".format(num_network_lanes))
        print("Number of Host Supported        :\t{}".format(num_host_lanes))
        print("Vendor Name                     :\t{}".format(
            self.str_read(regAddr=0x8021, length=16)))
        print("Vendor Part Number              :\t{}".format(
            self.str_read(regAddr=0x8034, length=16)))
        print("Vendor Serial Number            :\t{}".format(
            self.str_read(regAddr=0x8044, length=16)))
        print("Vendor Date Code                :\t{}".format(
            self.str_read(regAddr=0x8054, length=8)))

        # Version numbers stored in two registers as x.y where x represents the register at the lower address and y
        # at the higher address
        # [2:] --> slices of the '0x' in the hex numbers returned by the read() functions
        hw_version_num = str(self.read16(regAddr=0x806a))+'.'+str(self.read16(regAddr=0x806b))
        print(
            "Module Hardware Version Number  :\t{}".format(hw_version_num))
        fw_version_num = str(self.read16(regAddr=0x806c))+'.'+str(self.read16(regAddr=0x806d))
        print(
            "Module Firmware Version Number  :\t{}".format(fw_version_num))
        print("="*60)

    #--------------------------------------------------------------------------#

    def status(self):
        '''
        Queries CFP module status pins and status registers. Note that module registers 
        can not be accessed if the module is in reset or initialization state

        Args:
            None

        Returns:
            Nothing

        Raises:
            Nothing
        '''

        # Get number of network lanes
        num_lanes = self.read16(regAddr=0x8009)
        num_host_lanes = num_lanes & 0x0f
        if num_host_lanes == 0:
            num_host_lanes = 16
        num_lanes = num_lanes >> 4
        num_network_lanes = num_lanes & 0x0f
        if num_network_lanes == 0:
            num_network_lanes = 16
        
        # get voltage temperature txpowr, rxpwr
        print("Module voltage                               :\t{:.2f}V".format(self.get_volt()))
        print("Module temperature                           :\t{:.2f}degC".format(self.get_temp()))
        print("Module tx power                              :\t{:.2f}dBm".format(self.get_tx_power()))
        print("Module rx power                              :\t{:.2f}dBm".format(self.get_rx_power()))

        state = self.state()
        for attr in dir(self):
            if attr.find('STATE') != -1 and getattr(self, attr) == state:
                print(
                    "Module State                                 :\t{}".format(attr))
                break
        print("Module State Latch                           :\t{}".format(
            self.read16(regAddr=0xB022)))

        print("Global Alarm Summary                         :\t{}".format(
            self.read16(regAddr=self.REG_MOD_GLB_ALRM)))
        print("Module General Status                        :\t{}".format(
            self.read16(regAddr=self.REG_MOD_GEN_STATUS)))
        print("Module General Status Latch                  :\t{}".format(
            self.read16(regAddr=0xB023)))
        print("Module Fault Status                          :\t{}".format(
            self.read16(regAddr=self.REG_MOD_FAULT_STATUS)))
        print("Module Fault Status Latch                    :\t{}".format(
            self.read16(regAddr=0xB024)))
        print("Module Alarms and Warnings 1                 :\t{}".format(
            self.read16(regAddr=0xB01f)))
        print("Module Alarms and Warnings 1 Latch           :\t{}".format(
            self.read16(regAddr=0xB025)))
        print("Module Alarms and Warnings 2                 :\t{}".format(
            self.read16(regAddr=0xB020)))
        print("Module Alarms and Warnings 2 Latch           :\t{}".format(
            self.read16(regAddr=0xB026)))

        print("-"*60)
        print(
            "Network Lane Alarm/Warning Summary : {}".format(self.read16(regAddr=0xB019)))
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa200 + i))))
        print("Network Lane Alarm/Warning Latches")
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa220 + i))))

        print("-"*60)
        print(
            "Network Lane Fault/Status Summary : {}".format(self.read16(regAddr=0x0B01a)))
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa210 + i))))
        print("Network Lane Fault/Status Latches")
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa230 + i))))

        print("-"*60)
        print(
            "Host Lane Fault and Status Summary : {}".format(self.read16(regAddr=0x0B01b)))
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_host_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa400 + i))))
        print("Host Lane Fault/Status Latches")
        print("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_host_lanes):
            print("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read16(regAddr=(0xa410 + i))))
        print("="*70)

    #--------------------------------------------------------------------------#

    def waitReset(self):
        '''
        Resets the CFP2 module and leaves it in Low Power State

        Args:
            None

        Returns:
            True if the Reset is success and the module doesn't go the Fault State.
            False, otherwise.

        Raises:
            TimeoutError

        Notes:
        '''
        fault_state = False
        error_count = 0

        # 1. Check if the module is present
        # 2. Assert and deassert MOD_RSTn, set TX_DIS and MOD_LOPWR to 1

        # 3. CFP2 module goes thru the Reset State and Init State and enters Low Power State.
        #    CFP2 stays in the Low Power State as long as the MOD_LOPWR is asserted.
        # wait for the module to enter Low Power State

        timeout = time.time() + 20
        mod_state = self.state()
        while mod_state != self.LOW_POWER_STATE:
            mod_state = self.state()
            if mod_state == self.FAULT_STATE:
                print("CFP2 module entered Fault State")
                break
            if time.time() > timeout:
                print("Timeout for the CFP8 module to enter Low Power State")
        else:
            print("enter low power state")

    #--------------------------------------------------------------------------#

    def waitHiPowerup(self):
        '''
        Powers up the CFP2 module and leaves in TX_OFF State

        Args:
            None

        Returns:
            True  - if the power up is successful.
            False - otherwise

        Raises:
            TimeoutError

        Notes:
            CFP2 module cannot be powered up if it is not in Low Power State or in fault state.
        '''
        fault_state = False
        error_count = 0

        # 1. Check if the module is not in Fault State and in Low Power State.

        # 2. Set TX_DIS=1
        # 3. Set MOD_LOPWR=0
        # 4. CFP2 enters High-Power State, which is a transient state.
        # 5. Upon exiting High-Power State:
        #       - CFP2 asserts HIPWR_ON and enters TX-OFF State, if the power-up is success
        #       - CFP2 enters Fault State and de-asserts HIPWR_ON, if the power-up fails
        timeout = time.time() + 20
        mod_state = self.state()
        while mod_state != self.HIGH_POWER_UP_STATE:
            mod_state = self.state()
            if mod_state == self.FAULT_STATE:
                print("CFP2 is in Fault State. Power-up Failed.")
                break
            if time.time() > timeout:
                print("Timeout for the CFP8 module to enter TX-OFF State")
        else:
            print("CFP2 enter hi power state")

    #--------------------------------------------------------------------------#

    def waitTxon(self):
        '''
        Turns on the CFP2 module Transmitter ON and leaves it in the Ready State.

        Args:
            None

        Returns:
            True  - if the module's transmitter turn on is success
            False - otherwise

        Raises:
            TimeoutError

        Notes:
            CFP module either enables or disables lanes according to the configuration in
            individual Network Lane TX_DIS Control CFP register.
            CFP2 transmitter cannot be turned on if CFP2 is not powered up or if there is any fault.
        '''
        # 1. Check the module state

        # 2. Assert Hard TX_DIS.
        # 3. CFP2 enters TX-Turn-On state.
        #   In this transient state, CFP module either enables or disables lanes according
        #   to the configuration in individual Network Lane TX_DIS Control CFP register.
        # 4. Upon successfully turning-on the desired transmitters, CFP2 asserts MOD_READY
        #   and enters the Ready State.
        #   If the turning-on the transmitters fail due to any faults, CFP2 enters Fault State
        #   and deasserts MOD_READY.
        timeout = time.time() + 100
        mod_state = self.state()
        while mod_state != self.READY_STATE:
            mod_state = self.state()
            if mod_state == self.FAULT_STATE:
                print("CFP2 is in Fault State. TX-ON Failed.")
            if time.time() > timeout:
                print("Timeout for the CFP8 module to enter TX-OFF State")
        else:
            print("cfp2 enter ready state")

    #--------------------------------------------------------------------------#

    def prg_cntl1(self):
        '''
        Reads the register 0xB007[7:0] which specifies the function selection for
        PRG_CNTL1. 

        Args:
            None

        Returns:
            A string representing the selected function of PRG_CNTL1

        Raises:
            None
        '''
        reg = self.read16(regAddr=0xB007)
        reg = reg & 0x0f
        func = "No Active"
        if reg == 0x01:
            func = "TRXIC_RSTn"
        elif reg == 0x0a:
            func = "TX_DIS"
        return func
    #--------------------------------------------------------------------------#

    def prg_alrm1(self):
        '''
        Reads the register 0xB00A[7:0] which specifies the function selection for
        PRG_ALRM1. 

        Args:
            None

        Returns:
            A string representing the selected function of PRG_CNTL1

        Raises:
            None
        '''
        reg = self.read16(regAddr=0xB00a)
        reg = reg & 0x0f
        func = "Not Active"
        if reg == 0x01:
            func = "HIPWR_ON"
        elif reg == 0x02:
            func = "Ready State"
        elif reg == 0x03:
            func = "Fault State"
        elif reg == 0x04:
            func = "RX_ALRM"
        elif reg == 0x05:
            func = "TX_ALRM"
        elif reg == 0x06:
            func = "RX_NETWORK_LOL"
        elif reg == 0x07:
            func = "TX_LOSF"
        elif reg == 0x08:
            func = "TX_HOST_LOL"
        elif reg == 0x09:
            func = "Out of Alignment"
        elif reg == 0x0a:
            func = "RX_LOS"
        return func
    #--------------------------------------------------------------------------#

    def str_read(self, regAddr, length):
        '''
        Performs an MDIO read of the CFP2 module.  Designed to read specific registers 
        that provide vendor information in ASCII code which is left aligned and padded
        on the right with ASCII spaces (0x20)

        Args:
            addr (int): register address to read
            length (int): number of registers the information is stored in (size)

        Returns:
            (str) ASCII converted information

        Raises:
            None
        '''
        new_str = ''
        for i in range(length):
            data = self.read16(regAddr + i)
            new_str = new_str + chr(data)


        return new_str
    #--------------------------------------------------------------------------#

    def get_temp(self):
        """get temperaturer

        Returns:
            double: temperatue
        """
        tmp = self.read16(0xb02f)
        if tmp & 0x8000:
            return (~tmp+1)/256
        else:
            return tmp/256
    
    def get_volt(self):
        """get supply voltage

        Returns:
            [double]: voltage of cfp2
        """
        return self.read16(0xb030)/1000
    
    def get_tx_power(self):
        """get tx power

        Returns:
            float: tx power in dBm
        """
        return (self.read16(0x8120)<<16+self.read16(0x8121))*0.01

    def get_rx_power(self):
        """get rx power

        Returns:
            float: rx power in dBm
        """
        return (self.read16(0x8100)<<16+self.read16(0x8101))*0.01