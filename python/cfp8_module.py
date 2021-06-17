################################################################################
#   COPYRIGHT (C) 2018 MICROSEMI, INC. ALL RIGHTS RESERVED.
# --------------------------------------------------------------------------
#  This software embodies materials and concepts which are proprietary and
#  confidential to Microsemi, Inc.
################################################################################
'''
This class provides methods to configure, control and obtain status
from CFP8 optical modules plugged in to DIGI boards.
'''

import logging
import time


class Cfp8Module():
    '''
    This class provides methods to configure, control and obtain status
    from CFP8 optical modules plugged in to DIGI boards.

    Attributes:
        read()
        write()
        state()
        identifier()
        info()
        status()
        init()
        reset()
        powerup()
        txon()
    '''
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

    #--------------------------------------------------------------------------#
    def __init__(self, *args, reg, device_idx, **kwargs):
        super().__init__(*args, **kwargs)
        self.reg = reg
        self.device_idx = device_idx
        self.logger = logging.getLogger(__name__)
    #--------------------------------------------------------------------------#

    def read(self, *, addr):
        '''
        Performs an MDIO read of the CFP8 module

        Args:
            addr (int): register address to read

        Returns:
            integer: value read back

        Raises:
            None
        '''
        self.reg.write(
            'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_SELN'.format(self.device_idx), 0)
        self.config_mux(select=self.slvaddr.value[0])
        rd_data = self.mdio.read(phy=self.slvaddr.value[1], addr=addr)
        self.reg.write(
            'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_SELN'.format(self.device_idx), 1)
        return rd_data
    #--------------------------------------------------------------------------#

    def write(self, *, addr, data):
        '''
        Performs an MDIO read of the CFP8 module

        Args:
            addr (int): register address to write
            data (int): value to be written

        Returns:
            integer: value read back

        Raises:
            None
        '''
        self.reg.write(
            'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_SELN'.format(self.device_idx), 0)
        self.config_mux(select=self.slvaddr.value[0])
        rd_data = self.mdio.write(
            phy=self.slvaddr.value[1], addr=addr, data=data)
        self.reg.write(
            'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_SELN'.format(self.device_idx), 1)
    #--------------------------------------------------------------------------#

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
        mod_id = self.read(addr=0x8000)
        if mod_id != 0x15:
            self.logger.wprint("Inserted module is not the CFP8")
        return mod_id
    #--------------------------------------------------------------------------#

    def state(self):
        '''
        Returns the State of the CFP8 module.

        Args:
            None

        Returns:
            CFP8 Module State

        Raises:
            None

        Notes:
        '''
        mod_state = self.read(addr=self.REG_MOD_STATE)
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
        self.logger.lprint("="*60)
        self.logger.lprint(
            "Module ID                       :\t{}".format(self.identifier()))
        self.logger.lprint(
            "Extended ID                     :\t{}".format(self.read(addr=0x8001)))

        # If Application Code registers read 0x00 the documentation specifies that this value is undefined
        eth_app_code = self.read(addr=0x8003)
        if eth_app_code == 0x00:
            self.logger.lprint("Ethernet Application Code      :\tUndefined")
        else:
            self.logger.lprint(
                "Ethernet Appplication Code      :\t{}".format(eth_app_code))
        sonet_sdh_app_code = self.read(addr=0x8006)
        if sonet_sdh_app_code == 0x00:
            self.logger.lprint("SONET/SDH Application Code      :\tUndefined")
        else:
            self.logger.lprint(
                "SONET/SDH Application Code      :\t{}".format(sonet_sdh_app_code))
        otn_app_code = self.read(addr=0x8007)
        if otn_app_code == 0x00:
            self.logger.lprint("OTN Application Code            :\tUndefined")
        else:
            self.logger.lprint(
                "OTN Application Code            :\t{}".format(otn_app_code))

        # Number of network and host lanes are help in the upper and lower 4 bits of the register respectively
        num_lanes = self.read(addr=0x8009)
        num_host_lanes = num_lanes & 0x0f
        if num_host_lanes == 0:
            num_host_lanes = 16
        num_lanes = num_lanes >> 4
        num_network_lanes = num_lanes & 0x0f
        if num_network_lanes == 0:
            num_network_lanes = 16
        self.logger.lprint(
            "Number of Network Supported     :\t{}".format(num_network_lanes))
        self.logger.lprint(
            "Number of Host Supported        :\t{}".format(num_host_lanes))

        # If bit rate registers read 0x00 the documentation specifies that this value is undefined
        max_network_lane_bit_rate = self.read(addr=0x800b)
        if max_network_lane_bit_rate == 0x00:
            self.logger.lprint("Maximum Network Lane Bit Rate   :\tUndefined")
        else:
            self.logger.lprint("Maximum Network Lane Bit Rate   :\t0.2 Gbps x {}".format(
                max_network_lane_bit_rate))
        max_host_lane_bit_rate = self.read(addr=0x800c)
        if max_host_lane_bit_rate == 0x00:
            self.logger.lprint("Maximum Host Lane Bit Rate      :\tUndefined")
        else:
            self.logger.lprint("Maximum Host Lane Bit Rate      :\t0.2 Gbps x {}".format(
                max_host_lane_bit_rate))

        self.logger.lprint("Vendor Name                     :\t{}".format(
            self.str_read(addr=0x8021, length=16)))
        self.logger.lprint("Vendor Part Number              :\t{}".format(
            self.str_read(addr=0x8034, length=16)))
        self.logger.lprint("Vendor Serial Number            :\t{}".format(
            self.str_read(addr=0x8044, length=16)))
        self.logger.lprint("Vendor Date Code                :\t{}".format(
            self.str_read(addr=0x8054, length=8)))

        # Version numbers stored in two registers as x.y where x represents the register at the lower address and y
        # at the higher address
        # [2:] --> slices of the '0x' in the hex numbers returned by the read() functions
        hw_version_num = str(self.read(addr=0x806a))[
            2:]+'.'+str(self.read(addr=0x806b))[2:]
        self.logger.lprint(
            "Module Hardware Version Number  :\t{}".format(hw_version_num))
        fw_version_num = str(self.read(addr=0x806c))[
            2:]+'.'+str(self.read(addr=0x806d))[2:]
        self.logger.lprint(
            "Module Firmware Version Number  :\t{}".format(fw_version_num))
        self.logger.lprint("="*60)

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

        bit_list = {
            'PRG_CNTL1 (Function Select)': self.prg_cntl1(),
            'TX_DIS': self.reg.read('DFPGA_TOP.CFP8_CTRL({}).CFP8_TX_DIS'.format(self.device_idx)),
            'MOD_LOPWR': self.reg.read('DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_LOPWR'.format(self.device_idx)),
            'MOD_RSTn': self.reg.read('DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_RSTN'.format(self.device_idx)),
            'PRG_ALRM1 (Function Select)': self.prg_alrm1(),
            'RX_LOS': self.reg.read('DFPGA_TOP.CFP8_MON({}).CFP8_RX_LOS'.format(self.device_idx)),
            'GLB_ALRMn': self.reg.read('DFPGA_TOP.CFP8_MON({}).CFP8_GLB_ALRMN'.format(self.device_idx))
        }
        self.logger.lprint("="*70)
        for item in bit_list:
            self.logger.lprint("{0:<45}:\t{1}".format(
                item, str(bit_list[item])))
        self.logger.lprint("-"*60)

        # Get number of network lanes
        num_lanes = self.read(addr=0x8009)
        num_host_lanes = num_lanes & 0x0f
        if num_host_lanes == 0:
            num_host_lanes = 16
        num_lanes = num_lanes >> 4
        num_network_lanes = num_lanes & 0x0f
        if num_network_lanes == 0:
            num_network_lanes = 16

        state = self.state()
        for attr in dir(self):
            if attr.find('STATE') != -1 and getattr(self, attr) == state:
                self.logger.lprint(
                    "Module State                                 :\t{}".format(attr))
                break
        self.logger.lprint("Module State Latch                           :\t{}".format(
            self.read(addr=0xB022)))

        self.logger.lprint("Global Alarm Summary                         :\t{}".format(
            self.read(addr=self.REG_MOD_GLB_ALRM)))
        self.logger.lprint("Module General Status                        :\t{}".format(
            self.read(addr=self.REG_MOD_GEN_STATUS)))
        self.logger.lprint("Module General Status Latch                  :\t{}".format(
            self.read(addr=0xB023)))
        self.logger.lprint("Module Fault Status                          :\t{}".format(
            self.read(addr=self.REG_MOD_FAULT_STATUS)))
        self.logger.lprint("Module Fault Status Latch                    :\t{}".format(
            self.read(addr=0xB024)))
        self.logger.lprint("Module Alarms and Warnings 1                 :\t{}".format(
            self.read(addr=0xB01f)))
        self.logger.lprint("Module Alarms and Warnings 1 Latch           :\t{}".format(
            self.read(addr=0xB025)))
        self.logger.lprint("Module Alarms and Warnings 2                 :\t{}".format(
            self.read(addr=0xB020)))
        self.logger.lprint("Module Alarms and Warnings 2 Latch           :\t{}".format(
            self.read(addr=0xB026)))

        self.logger.lprint("-"*60)
        self.logger.lprint(
            "Network Lane Alarm/Warning Summary : {}".format(self.read(addr=0xB019)))
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa200 + i))))
        self.logger.lprint("Network Lane Alarm/Warning Latches")
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa220 + i))))

        self.logger.lprint("-"*60)
        self.logger.lprint(
            "Network Lane Fault/Status Summary : {}".format(self.read(addr=0x0B01a)))
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa210 + i))))
        self.logger.lprint("Network Lane Fault/Status Latches")
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_network_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa230 + i))))

        self.logger.lprint("-"*60)
        self.logger.lprint(
            "Host Lane Fault and Status Summary : {}".format(self.read(addr=0x0B01b)))
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_host_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa400 + i))))
        self.logger.lprint("Host Lane Fault/Status Latches")
        self.logger.lprint("{lane:>41}{state:>15}".format(
            lane="Lane", state="State"))
        for i in range(num_host_lanes):
            self.logger.lprint("{lane:>40}\t\t{state}".format(
                lane=i, state=self.read(addr=(0xa410 + i))))
        self.logger.lprint("="*70)

    #--------------------------------------------------------------------------#

    def init(self):
        '''
        Resets, Powers Up and leaves the device in the Ready State

        Args:
            None

        Returns:
            True - if the initialization is successufl
            False - otherwise

        Raises:
            None
        '''
        self.reset()
        self.powerup()
        self.txon()
        if self.state() == self.READY_STATE:
            init_done = True
        else:
            init_done = False

        return init_done
    #--------------------------------------------------------------------------#

    def reset(self):
        '''
        Resets the CFP8 module and leaves it in Low Power State

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
        mod_abs = self.reg.read(
            'DFPGA_TOP.CFP8_MON({}).CFP8_MOD_ABS'.format(self.device_idx))
        if mod_abs == 1:
            self.logger.lprint("CFP8 module is not present to reset.")
            error_count += 1
        else:
            # 2. Assert and deassert MOD_RSTn, set TX_DIS and MOD_LOPWR to 1
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_TX_DIS'.format(self.device_idx), 1)
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_LOPWR'.format(self.device_idx), 1)
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_RSTN'.format(self.device_idx), 1)
            time.sleep(0.5)
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_RSTN'.format(self.device_idx), 0)
            time.sleep(0.5)
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_RSTN'.format(self.device_idx), 1)

            # 3. CFP8 module goes thru the Reset State and Init State and enters Low Power State.
            #    CFP8 stays in the Low Power State as long as the MOD_LOPWR is asserted.
            # wait for the module to enter Low Power State
            timeout = time.time() + 20
            mod_state = self.state()
            while mod_state != self.LOW_POWER_STATE:
                mod_state = self.state()
                if mod_state == self.FAULT_STATE:
                    self.logger.eprint("CFP8 module entered Fault State")
                    fault_state = True
                    error_count += 1
                    break
                if time.time() > timeout:
                    self.logger.eprint(
                        "Timeout for the CFP8 module to enter Low Power State")
                    error_count += 1
                    raise TimeoutError

        # 4. Return true if the reset is success and the module is not in Fault State.
        if error_count == 0 and (fault_state is False):
            reset_done = True
        else:
            reset_done = False

        return reset_done
    #--------------------------------------------------------------------------#

    def powerup(self):
        '''
        Powers up the CFP8 module and leaves in TX_OFF State

        Args:
            None

        Returns:
            True  - if the power up is successful.
            False - otherwise

        Raises:
            TimeoutError

        Notes:
            CFP8 module cannot be powered up if it is not in Low Power State or in fault state.
        '''
        fault_state = False
        error_count = 0

        # 1. Check if the module is not in Fault State and in Low Power State.
        mod_state = self.state()
        if mod_state == self.TX_OFF_STATE:
            self.logger.eprint("CFP8 is already in TX-OFF State.")
        elif mod_state == self.FAULT_STATE:
            self.logger.eprint("CFP8 is in Fault State. Cannot be powered-up.")
            error_count += 1
        elif mod_state != self.LOW_POWER_STATE:
            self.logger.eprint(
                "CFP8 is not in Low Power State. Cannot be powered-up.")
            error_count += 1
        else:
            self.logger.lprint("Powering up CFP8")

            # 2. Set TX_DIS=1
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_TX_DIS'.format(self.device_idx), 1)
            # 3. Set MOD_LOPWR=0
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_MOD_LOPWR'.format(self.device_idx), 0)

            # 4. CFP8 enters High-Power State, which is a transient state.

            # 5. Upon exiting High-Power State:
            #       - CFP8 asserts HIPWR_ON and enters TX-OFF State, if the power-up is success
            #       - CFP8 enters Fault State and de-asserts HIPWR_ON, if the power-up fails
            timeout = time.time() + 20
            mod_state = self.state()
            while mod_state != self.TX_OFF_STATE:
                mod_state = self.state()
                if mod_state == self.FAULT_STATE:
                    self.logger.eprint(
                        "CFP8 is in Fault State. Power-up Failed.")
                    fault_state = True
                    error_count += 1
                elif mod_state == self.HIGH_POWER_UP_STATE:
                    self.logger.lprint("""CFP8 is in High-Power-up State. \
                                       Waiting for transition to TX-OFF State""")
                if time.time() > timeout:
                    self.logger.eprint(
                        "Timeout for the CFP8 module to enter TX-OFF State")
                    error_count += 1
                    raise TimeoutError

        # 6. Return True if CFP8 enters TX-OFF state successfully without any faults
        if error_count == 0 and fault_state == False:
            powered_up = True
        else:
            powered_up = False

        return powered_up
    #--------------------------------------------------------------------------#

    def txon(self):
        '''
        Turns on the CFP8 module Transmitter ON and leaves it in the Ready State.

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
            CFP8 transmitter cannot be turned on if CFP8 is not powered up or if there is any fault.
        '''
        fault_state = False
        error_count = 0

        # 1. Check the module state
        mod_state = self.state()
        if mod_state == self.READY_STATE:
            self.logger.lprint("CFP8 is already in Ready State...")
            return True
        elif mod_state == self.FAULT_STATE:
            self.logger.eprint(
                "CFP8 is in Fault State. Cannot Turn-On the Transmitter.")
            error_count += 1
        elif mod_state != self.TX_OFF_STATE:
            self.logger.eprint(
                "CFP8 is not in TX-OFF State. See if the CFP8 is powered up.")
            return False
        else:
            self.logger.lprint("Turning ON the CFP8 Transmitters...")

            # 2. Assert Hard TX_DIS.
            self.reg.write(
                'DFPGA_TOP.CFP8_CTRL({}).CFP8_TX_DIS'.format(self.device_idx), 0)

            # 3. CFP8 enters TX-Turn-On state.
            #   In this transient state, CFP module either enables or disables lanes according
            #   to the configuration in individual Network Lane TX_DIS Control CFP register.

            # 4. Upon successfully turning-on the desired transmitters, CFP8 asserts MOD_READY
            #   and enters the Ready State.
            #   If the turning-on the transmitters fail due to any faults, CFP8 enters Fault State
            #   and deasserts MOD_READY.
            timeout = time.time() + 20
            mod_state = self.state()
            while mod_state != self.READY_STATE:
                mod_state = self.state()
                if mod_state == self.FAULT_STATE:
                    self.logger.eprint("CFP8 is in Fault State. TX-ON Failed.")
                    fault_state = True
                elif mod_state == self.TX_TURN_ON_STATE:
                    self.logger.lprint("""CFP8 is in Tx-Turn-on State. \
                                       Waiting for transition to Ready State""")
                if time.time() > timeout:
                    self.logger.eprint(
                        "Timeout for the CFP8 module to enter TX-OFF State")
                    raise TimeoutError

            # 5. Return True if CFP8 enters Ready state successfully without any faults
            return not fault_state
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
        reg = self.read(addr=0xB007)
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
        reg = self.read(addr=0xB00a)
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

    def str_read(self, *, addr, length):
        '''
        Performs an MDIO read of the CFP8 module.  Designed to read specific registers 
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
        hex_list = []
        for i in range(length):
            data = self.read(addr=(addr + i))
            hex_list.append(str(data)[2:])

        new_str = ''
        for item in hex_list:
            if item != '20':
                item = int(item, 16)
                new_str = new_str+chr(item)

        return new_str
    #--------------------------------------------------------------------------#
