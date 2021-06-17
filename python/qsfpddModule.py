import time
from math import log10
import misc
import baseclass


class Qsfpdd(baseclass.BaseAddr16Value8):

    def __init__(self, bus, dev_addr=0x50):
        """qsfp init

        Args:
            bus (i2c bus instance ): i2c bus instance
            dev_addr (hexadecimal, optional): dev addr. Defaults to 0xa0.
        """
        self.bus = bus
        self.dev_addr = dev_addr
        baseclass.BaseAddr16Value8.__init__(self)
    
    def __del__(self):
        """close laser
        """
        self.module_tx_enable(False)

    def read8(self, addr):
        """reg read

        Args:
            addr (uint8): reg addr

        Returns:
            uint8: reg value
        """
        # write page first
        page = addr>>8
        self.bus.write(self.dev_addr, 0x7f, page)
        return self.bus.read(self.dev_addr, addr)

    def printReg(self, addr, len=1, page=0):
        """print reg value

        Args:
            addr (uint8): start addr
            len (int, optional): len. Defaults to 1.
        """
        # write page first, and only in 1 page
        if (addr + len) > 0xff:
            print("only print in 1 page")
            return
        self.bus.write(self.dev_addr, 0x7f, page)
        for i in range(len):
            print("addr 0x%x" % (addr + i), ": 0x%x" % self.read8(addr, page))

    def dump_page(self, page_no):
        """dump sfp reg page

        Args:
            page_no (uint8): page of sfp
        """
        self.bus.write(self.dev_addr, 0x7f, page_no)
        tmp = []
        for i in range(256):
            tmp.append(self.bus.read(self.dev_addr, i))
        misc.hexdump(0, tmp)

    def write8(self, addr, data):
        """write reg

        Args:
            addr (uint16): reg addr
            data (uint8): reg value
        """
        page = addr>>8
        self.bus.write(self.dev_addr, 0x7f, page)
        self.bus.write(self.dev_addr, addr, data)

    def info(self):
        '''
        Gathers information about a module currently connected to the board.
        :return:
        '''
        # Ensure reading from 0x00 upper page using byte 127 (page select)
        self.write8(addr=127, data=0)

        print("="*60)
        print("Module ID                          :\t0x%2x" %
              self.read8(addr=0))
        print("HOST Lane                          :\t%d" %
              (self.read8(88)>>4))
        print("Media Lane                         :\t%d" %
              (self.read8(88)&0xf))              
        print("Power Class                        :\t%s" %
              self.module_powerclass())
        print("Vendor Name                        :\t%s" %
              self.str_read(addr=129, length=16))
        print("Vendor Part Number                 :\t%s" %
              self.str_read(addr=148, length=16))
        print("Vendor Serial Number               :\t%s" %
              self.str_read(addr=166, length=16))
        print("Vendor Date Code                   :\t%s" %
              self.str_read(addr=182, length=8))
        print("="*60)

    def status(self):
        '''
        Gathers status about a QSFP module connected to the board.
        :return:
        '''
        print("="*60)
        print("Temperature     :\t%3.2f" % self.get_temp())
        print("Supply Voltage  :\t%2.2f" % self.get_volt())

        medialanesrange = (self.read8(88)&0xf) + 1
        # print("TX Power Alarm/Warning:\t%d" %
        #       self.tx_power_alarm_warning_int())
        # print("RX Power Alarm/Warning:\t%d" %
        #       self.rx_power_alarm_warning_int())
        # print("TX Bias Alarm/Warning :\t%d" % self.tx_bias_alarm_warning_int())

        print("-"*50)
        print("%10s%10s%10s%10s" % ("Channel", "TXPWR(dbm)", "LOS","LOL"))
        for ch in range(1, medialanesrange):
            print("%7d" % ch, end=' ')
            print("%10.2f" % (self.ch_tx_power(ch)), end=' ')
            print("%10d" % (self.ch_status_int_tx_los_indicator(ch_no=ch)),end=' ')
            print("%10d" % (self.ch_status_int_tx_lol_indicator(ch_no=ch)))
        print("-"*50)
        print("%10s%10s%10s%10s" % ("Channel", "RXPWR(dbm)", "LOS", "LOL"))
        for ch in range(1, medialanesrange):
            print("%7d" % ch, end=' ')
            print("%10.2f" % (self.ch_rx_power(ch)), end=' ')
            print("%10d" % (self.ch_status_int_rx_los_indicator(ch_no=ch)), end=' ')
            print("%10d" % (self.ch_status_int_rx_lol_indicator(ch_no=ch)))

        # print("-"*50)
        # print("%20s%10s%10s" % ("TX LOS Indicator", "Channel", "State"))
        # for ch in range(1, medialanesrange):
        #     print("%30d%10d" % (ch, self.ch_status_int_tx_los_indicator(ch_no=ch)))
        # print("-"*50)
        # print("%20s%10s%10s" % ("RX LOS Indicator", "Channel", "State"))
        # for ch in range(1, medialanesrange):
        #     print("%30d%10d" % (ch, self.ch_status_int_rx_los_indicator(ch_no=ch)))
        # print("-"*50)
        # print("%20s%10s%10s" % ("TX Loss of Lock Indicator", "Channel", "State"))
        # for ch in range(1, medialanesrange):
        #     print("%30d%10d" % (ch, self.ch_status_int_tx_lol_indicator(ch_no=ch)))
        # print("-"*50)
        # print("%20s%10s%10s" % ("RX Loss of Lock Indicator", "Channel", "State"))
        # for ch in range(1, medialanesrange):
        #     print("%30d%10d" % (ch, self.ch_status_int_rx_lol_indicator(ch_no=ch)))
        # print("-"*50)
        # print("%20s%10s%10s" % ("TX Fault Indicator", "Channel", "State"))
        # for ch in range(1, 8):
        #     print("%30d%10d" %
        #           (ch, self.ch_status_int_tx_adapt_fault_indicator(ch_no=ch)))
        print("="*60)

    def module_state(self):
        module_state = {0: "Reserved", 1: "ModuleLowPwr", 2: "ModulePwrUp",
                        3: "ModuleReady", 4: "ModulePwrDn", 5: "Fault", 6: "Reserved", 7: "Reserved"}
        return module_state[self.read8(3) >> 1]

    def ch_state(self,ch):
        ch_state = {0: "Reserved", 1: "DataPathDeactivated", 2: "DataPathInit", 3: "DataPathDeinit",
                    4: "DataPathActivated", 5: "DataPathTxTurnOn", 6: "DataPathTxTurnOff", 7: "DataPathInitialized"}
        for i in range(8,16):
            ch_state[i] = "Reserved"
        state_reg = self.read8(0x1100 + 128 + (ch-1)>>1)
        state = state_reg & 0x0f if(ch-1)%2 else (state_reg & 0xf0)>>4
        return ch_state[state]
    
    def module_tx_enable(self,enable=True):
        txRegAddr = 0x1000 + 130
        if enable:
            self.write8(txRegAddr,0)
        else:
            self.write8(txRegAddr,0xff)

    def ch_datapathPwrUp(self,  ch_no):
        '''
        Disables the corresponding Optical Tx channel.

        Args:
            ch_no (int): Integer that selects one of the four Tx channels

        Returns:
            None

        Raises:
            Warning if Power Override is disabled

        Notes:
            None
        '''
        rdata = self.read8(addr=0x1080)
        mdata = 2**(ch_no-1)
        self.write8(addr=0x1080, data=rdata & ~(mdata))


    def ch_status_int_tx_los_indicator(self, ch_no):
        '''
        Returns the LOS Indicator interrupt status of the corresponding Tx channel

        Args:
            ch_no (int): Integer that represent one of the four Tx channel number

        Returns:
            True - if the Tx LOS indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        los_ind = self.read8(0x1100+136)
        tx_los_ind = los_ind & 2**(ch_no - 1) != 0

        return tx_los_ind

    def ch_status_int_rx_los_indicator(self,  ch_no):
        '''
        Returns the LOS Indicator interrupt status of the corresponding Rx channel

        Args:
            ch_no (int): Integer that represent one of the four Rx channel number

        Returns:
            True - if the Rx LOS indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        los_ind = self.read8(0x1100+147)
        rx_los_ind = los_ind & 2**(ch_no-1) != 0

        return rx_los_ind

    def ch_status_int_tx_lol_indicator(self,  ch_no):
        '''
        Returns the LOL Indicator interrupt status of the corresponding Tx channel

        Args:
            ch_no (int): Integer that represent one of the four Rx channel number

        Returns:
            True - if the Tx LOL indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        lol_ind = self.read8(0x1100+137)
        tx_lol_ind = lol_ind & 2**(ch_no - 1) != 0

        return tx_lol_ind

    def ch_status_int_rx_lol_indicator(self,  ch_no):
        '''
        Returns the LOL Indicator interrupt status of the corresponding Rx channel

        Args:
            ch_no (int): Integer that represent one of the four Rx channel number

        Returns:
            True - if the Rx LOL indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        lol_ind = self.read8(0x1100+148)
        rx_lol_ind = lol_ind & 2**(ch_no-1) != 0

        return rx_lol_ind

    def ch_status_int_tx_adapt_fault_indicator(self,  ch_no):
        '''
        Returns the Adaptive Eq Fault Indicator interrupt status of the corresponding Tx channel

        Args:
            ch_no (int): Integer that represent one of the four Rx channel number

        Returns:
            True - if the Tx Adaptive Eq Fault indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        adapt_fault_ind = self.read8(0x1100+138)
        tx_adapt_eq_fault_ind = adapt_fault_ind & 2**(ch_no - 1) != 0

        return tx_adapt_eq_fault_ind

    def rx_power_alarm_warning_int(self):
        '''
        Shows the Rx Channel Power related Alarm/Warning Interrupts

        Args:
            None

        Returns:
            True - if any of the Power Alarm/Warning interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        reg_9 = self.read8(addr=9)
        reg_10 = self.read8(addr=10)
        return not(reg_9 == 0x00 and reg_10 == 0x00)

    def tx_power_alarm_warning_int(self):
        '''
        Shows the Tx Channel Power related Alarm/Warning Interrupts

        Args:
            None

        Returns:
            True - if any of the Power Alarm/Warning interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        reg_15 = self.read8(addr=15)
        reg_16 = self.read8(addr=16)
        return not(reg_15 == 0x00 and reg_16 == 0x00)

    def tx_bias_alarm_warning_int(self):
        '''
        Shows the Tx Channel Bias related Alarm/Warning Interrupts

        Args:
            None

        Returns:
            True - if any of the Bias Alarm/Warning interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        reg_13 = self.read8(addr=13)
        reg_14 = self.read8(addr=14)
        return not(reg_13 == 0x00 and reg_14 == 0x00)

    def get_temp(self):
        tmp = (self.read8(14) << 8) + self.read8(15)
        if tmp & 0x8000:
            return (~tmp+1)/256
        else:
            return tmp/256

    def get_volt(self):
        return ((self.read8(16) << 8) + self.read8(17))/10000

    def str_read(self,  addr, length):
        '''
        Performs an I2C read of the QSFP28 module.  Designed to read specific
        registers that provide information in ASCII code which is left aligned
        and padded on the right with ASCII spaces (0x20)

        Args:
            addr (int): register address to read
            length (int): number of registers the information is stored in (size)

        Returns:
            (str) ASCII converted information

        Raises:
            None
        '''
        hex_list = []
        for i in range(length):
            data = self.read8(addr=(addr + i))
            hex_list.append(data)

        new_str = ''
        for item in hex_list:
            if item != 32:
                new_str = new_str+chr(item)

        return new_str

    def ch_tx_power(self, ch):
        reg1 = self.read8(0x1100 + 154 + (ch-1)*2)
        reg2 = self.read8(0x1100 + 155 + (ch-1)*2)
        return ((reg1 << 8) + reg2)*0.0001

    def ch_rx_power(self, ch):
        reg1 = self.read8(0x1100 + 186 + (ch-1)*2)
        reg2 = self.read8(0x1100 + 187 + (ch-1)*2)
        return ((reg1 << 8) + reg2)*0.0001

    def ch_tx_bias(self, ch):
        reg1 = self.read8(0x1100 + 170 + (ch-1)*2)
        reg2 = self.read8(0x1100 + 171 + (ch-1)*2)
        return ((reg1 << 8) + reg2)

    def module_powerclass(self):
        QSFPDD_POWERCLASS = {0: "1.5W", 1: "3.5W", 2: "5W",
                             3: "7W", 4: "10W", 5: "12W", 6: "14W", 7: ">14W"}
        return QSFPDD_POWERCLASS[self.read8(200) >> 5]
