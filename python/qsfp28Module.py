import time
from math import log10
import misc
import baseclass


class Qsfp28(baseclass.BaseAddr16Value8):
    def __init__(self, bus, dev_addr=0x50):
        """qsfp init

        Args:
            bus (i2c bus instance ): i2c bus instance
            dev_addr (hexadecimal, optional): dev addr. Defaults to 0xa0.
        """
        self.bus = bus
        self.dev_addr = dev_addr
        baseclass.BaseAddr16Value8.__init__(self)

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
        print("Extended ID                        :\t0x%2x" %
              self.read8(addr=129))
        print("Encoding value                     :\t%s" %
              self.encoding_mechanism())
        print("Vendor Name                        :\t%s" %
              self.str_read(addr=148, length=16))
        print("Vendor Part Number                 :\t%s" %
              self.str_read(addr=168, length=16))
        print("Vendor Serial Number               :\t%s" %
              self.str_read(addr=196, length=16))
        print("Vendor Date Code                   :\t%s" %
              self.str_read(addr=212, length=8))
        print("="*60)

    def status(self):
        '''
        Gathers status about a QSFP module connected to the board.
        :return:
        '''
        print("="*60)
        print("Temperature     :\t%3.2f" % self.get_temp())
        print("Supply Voltage  :\t%2.2f" % self.get_volt())
        print("TX Power Alarm/Warning:\t%d" %
              self.tx_power_alarm_warning_int())
        print("RX Power Alarm/Warning:\t%d" %
              self.rx_power_alarm_warning_int())
        print("TX Bias Alarm/Warning :\t%d" % self.tx_bias_alarm_warning_int())

        print("-"*50)
        print("%20s%20s%20s" % ("Channel", "TX Power", "Power(dbm)"))
        for ch in range(1, 5):
            print("%15d" % ch, end=' ')
            print("%20.2f" % (self.ch_tx_power(ch)), end=' ')
            tmp = (10*log10(self.ch_tx_power(ch))
                   ) if (self.ch_tx_power(ch)) != 0 else 0
            print("%20.2f" % tmp)
        print("-"*50)
        print("%20s%20s%20s" % ("Channel", "RX Power", "Power(dbm)"))
        for ch in range(1, 5):
            print("%15d" % ch, end=' ')
            print("%20.2f" % (self.ch_rx_power(ch)), end=' ')
            tmp = (10*log10(self.ch_rx_power(ch))
                   ) if (self.ch_rx_power(ch)) != 0 else 0
            print("%20.2f" % tmp)
        print("-"*50)
        print("%20s%10s%10s" % ("TX LOS Indicator", "Channel", "State"))
        for ch in range(1, 5):
            print("%30d%10d" % (ch, self.ch_status_int_tx_los_indicator(ch_no=ch)))
        print("-"*50)
        print("%20s%10s%10s" % ("RX LOS Indicator", "Channel", "State"))
        for ch in range(1, 5):
            print("%30d%10d" % (ch, self.ch_status_int_rx_los_indicator(ch_no=ch)))
        print("-"*50)
        print("%20s%10s%10s" % ("TX Loss of Lock Indicator", "Channel", "State"))
        for ch in range(1, 5):
            print("%30d%10d" % (ch, self.ch_status_int_tx_lol_indicator(ch_no=ch)))
        print("-"*50)
        print("%20s%10s%10s" % ("RX Loss of Lock Indicator", "Channel", "State"))
        for ch in range(1, 5):
            print("%30d%10d" % (ch, self.ch_status_int_rx_lol_indicator(ch_no=ch)))
        print("-"*50)
        ##################
        # Changed due to Address 0x01 reading 0x00 - Undefined revision compliance
        # Fault indicator addressing slightly different in older versions
        #
        # for ch in range(1,5):
        #    print "Ch. {0} TX Adaptive EQ Fault Indicator   :\t{1}".format(ch, self.ch_status_int_tx_adapt_eq_fault_indicator(ch_no=ch)))
        # Changed from RX Adaptive EQ Fault Indicator to TX Fault Indicator (older version)
        print("%20s%10s%10s" % ("TX Fault Indicator", "Channel", "State"))
        for ch in range(1, 5):
            print("%30d%10d" %
                  (ch, self.ch_status_int_rx_adapt_eq_fault_indicator(ch_no=ch)))
        print("="*60)

    def encoding_mechanism(self):
        '''
        Indicates if the encoding algorithm based on Table 4-2 in SFF-8024

        Args:
            None

        Returns:
            (str) - Encoding mechanism

        Raises:
            None

        Notes:
        '''
        enc = self.read8(addr=139)
        mec = "Undefined"
        if enc == 0x01:
            mec = "8B/10B"
        elif enc == 0x02:
            mec = "4B/5B"
        elif enc == 0x03:
            mec = "NRZ"
        elif enc == 0x04:
            mec = "SONET Scrambled"
        elif enc == 0x05:
            mec = "64B/66B"
        elif enc == 0x06:
            mec = "Manchester"
        elif enc == 0x07:
            mec = "256B/257B"
        elif enc == 0x08:
            mec = "PAM4"

        return mec

    def rate_sel_support(self):
        '''
        Shows the availability of Rate Selection support feature

        Args:
            None

        Returns:
            True - if the Rate Selection support feature is available
            False - otherwise

        Raises:
            None

        Notes:
        '''
        return (self.read8(addr=221) & 0x0C == 0) and (self.read8(addr=195) & 0x20 == 0)

    def ext_rate_sel_support(self):
        '''
        Shows the availability of Extended Rate Selection support feature

        Args:
            None

        Returns:
            True - if the Extended Rate Selection support feature is available
            False - otherwise

        Raises:
            None

        Notes:
        '''
        return (self.read8(addr=221) & 0x08 == 0x08) and (self.read8(addr=141) != 0)

    def rate_sel_rx(self, val):
        '''
        Software Rate Select for the Rx Channels in the format:
        (Rx4-MSB, Rx4-LSB, Rx3-MSB, Rx3-LSB, Rx2-MSB, Rx2-LSB, Rx1-MSB, Rx1-LSB)

        Args:
            val (int): Integer that represents the value to be set for the Rate Select

        Returns:
            None

        Raises:
            None

        Notes:
            (MSB, LSB) = (0, 0) for the bit rates less than 2.2 Gbps
                       = (0, 1) for the bit rates from 2.2 to 6.6 Gbps
                       = (1, 0) for the bit rates from 6.6 Gbps and above
                       = (1, 1) Reserved. No effect.
        '''
        self.write8(addr=87, data=val)

    def rate_sel_tx(self,  val):
        '''
        Software Rate Select for the Rx Channels in the integer converted format:
        (Tx4-MSB, Tx4-LSB, Tx3-MSB, Tx3-LSB, Tx2-MSB, Tx2-LSB, Tx1-MSB, Tx1-LSB)

        Args:
            val (int): Integer that represents the value to be set for the Rate Select

        Returns:
            None

        Raises:
            None

        Notes:
            (MSB, LSB) = (0, 0) for the bit rates less than 2.2 Gbps
                       = (0, 1) for the bit rates from 2.2 to 6.6 Gbps
                       = (1, 0) for the bit rates from 6.6 Gbps and above
                       = (1, 1) Reserved. No effect.
        '''
        self.write8(addr=88, data=val)

    def tx_ch_disable(self,  ch_no):
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
        rdata = self.read8(addr=86)
        mdata = 2**(ch_no-1)
        self.write8(addr=86, data=rdata | mdata)

    def set_low_power_mode(self):
        '''
        Configures the QSFP28 in Low Power Mode, if Power Override is not disabled.

        Args:
            None

        Returns:
            None

        Raises:
            Warning if Power Override is disabled

        Notes:
            None
        '''
        rdata = self.read8(addr=93)
        if rdata & 0x01 != 0:
            wdata = rdata | 0x02
            self.write8(addr=93, data=wdata)
        else:
            print("Power Override is disabled.")

    def ch_status_int_los_indicator(self):
        '''
        Returns the LOS Indicator interrupt status register bits

        Args:
            None

        Returns:
            LOS Indicator interrupt status register

        Raises:
            None

        Notes:
        '''
        return self.read8(addr=3)

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
        los_ind = self.ch_status_int_los_indicator()
        if los_ind & 0xF0 == 0:
            tx_los_ind = False
        else:
            tx_los_ind = los_ind & 2**(ch_no+3) != 0

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
        los_ind = self.ch_status_int_los_indicator()
        if los_ind & 0x0F == 0:
            rx_los_ind = False
        else:
            rx_los_ind = los_ind & 2**(ch_no-1) != 0

        return rx_los_ind

    def ch_status_int_lol_indicator(self):
        '''
        Returns the LOL Indicator interrupt status register bits

        Args:
            None

        Returns:
            LOL Indicator interrupt status register

        Raises:
            None

        Notes:
        '''
        return self.read8(addr=5)

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
        lol_ind = self.ch_status_int_lol_indicator()
        if lol_ind & 0xF0 == 0:
            tx_lol_ind = False
        else:
            tx_lol_ind = lol_ind & 2**(ch_no+3) != 0

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
        lol_ind = self.ch_status_int_lol_indicator()
        if lol_ind & 0x0F == 0:
            rx_lol_ind = False
        else:
            rx_lol_ind = lol_ind & 2**(ch_no-1) != 0

        return rx_lol_ind

    def ch_status_int_adapt_eq_fault_indicator(self):
        '''
        Returns the Adaptive Eq Fault Indicator interrupt status register bits

        Args:
            None

        Returns:
            Adaptive Eq Fault Indicator interrupt status register

        Raises:
            None

        Notes:
        '''
        return self.read8(addr=4)

    def ch_status_int_tx_adapt_eq_fault_indicator(self,  ch_no):
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
        adapt_eq_fault_ind = self.ch_status_int_adapt_eq_fault_indicator()
        if adapt_eq_fault_ind & 0xF0 == 0:
            tx_adapt_eq_fault_ind = False
        else:
            tx_adapt_eq_fault_ind = adapt_eq_fault_ind & 2**(ch_no+3) != 0

        return tx_adapt_eq_fault_ind

    def ch_status_int_rx_adapt_eq_fault_indicator(self,  ch_no):
        '''
        Returns the Adaptive Eq Fault Indicator interrupt status of the corresponding Rx channel

        Args:
            ch_no (int): Integer that represent one of the four Rx channel number

        Returns:
            True - if the Rx Adaptive Eq Fault indicator interrupt field is high
            False - otherwise

        Raises:
            None

        Notes:
        '''
        adapt_eq_fault_ind = self.ch_status_int_adapt_eq_fault_indicator()
        if adapt_eq_fault_ind & 0x0F == 0:
            rx_adapt_eq_fault_ind = False
        else:
            rx_adapt_eq_fault_ind = adapt_eq_fault_ind & 2**(ch_no-1) != 0

        return rx_adapt_eq_fault_ind

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
        reg_13 = self.read8(addr=13)
        reg_14 = self.read8(addr=14)
        return not(reg_13 == 0x00 and reg_14 == 0x00)

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
        reg_11 = self.read8(addr=11)
        reg_12 = self.read8(addr=12)
        return not(reg_11 == 0x00 and reg_12 == 0x00)

    def get_temp(self):
        tmp = (self.read8(22) << 8) + self.read8(23)
        if tmp & 0x8000:
            return (~tmp+1)/256
        else:
            return tmp/256

    def get_volt(self):
        return ((self.read8(26) << 8) + self.read8(27))/10000

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
        reg1 = self.read8(50 + (ch-1)*2)
        reg2 = self.read8(51 + (ch-1)*2)
        return ((reg1 << 8) + reg2)*0.0001

    def ch_rx_power(self, ch):
        reg1 = self.read8(34 + (ch-1)*2)
        reg2 = self.read8(35 + (ch-1)*2)
        return ((reg1 << 8) + reg2)*0.0001

    def ch_tx_bias(self, ch):
        reg1 = self.read8(42 + (ch-1)*2)
        reg2 = self.read8(43 + (ch-1)*2)
        return ((reg1 << 8) + reg2)*2
