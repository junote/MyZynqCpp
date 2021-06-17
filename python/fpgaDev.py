import os
import mmap
import time
import threading
import baseclass
import Mmap64

class Fpga(baseclass.BaseAddr32Value32):
    """fpga interface

    Args:
        MmapDevice (class): basic mmap device
    """

    def __init__(self, baseAddr=0xa0000000, size=0x40000):
        self.baseAddr = baseAddr
        self.size = size
        self.master = Mmap64.Mmap64("mem", self.baseAddr, self.size)
        baseclass.BaseAddr32Value32.__init__(self)

    def read32(self, regAddr):
        """fpga read

        Args:
            regAddr (uint32): reg addr

        Returns:
            uint32: reg value
        """
        return self.master.read32(regAddr)

    def write32(self, regAddr, value):
        """fpga write

        Args:
            regAddr (uint32): reg addr
        """
        self.master.write32(regAddr, value)

    def setBitHigh(self, regAddr, bitAddr, High=True):
        """set fpga bit high

        Args:
            regAddr (uint32): regaddr
            bitAddr (uint8): 0-31
            High (bool, optional): False to clear, Defaults to True.
        """
        tmp = self.read32(regAddr)
        if High:
            tmp = tmp | (1 << bitAddr)
            self.write32(regAddr, tmp)
        else:
            tmp = tmp & (~(1 << bitAddr))
            self.write32(regAddr, tmp)

    def getBitHigh(self, regAddr, bitAddr):
        """get bit value

        Args:
            regAddr (uint32): reg addr
            bitAddr (uint8): 0-31 bit addr

        Returns:
            bool: if high return True else False
        """
        tmp = self.read32(regAddr)
        ret = True if tmp & (1 << bitAddr) else False
        return ret

    def printReg(self, regAddr, len=1):
        """print reg value

        Args:
            regAddr (uint32): reg addr
            len (int, optional): reg num. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr + 4 * i):04x}]:0x{self.read(regAddr+i*4):08x}")
    
    def upgrade(self, filename="pl.bin"):
        os.system("mkdir /lib/firmware")
        cmdline = "scp lab@10.13.11.104:/home/share/CHM1R/" + filename +  " /lib/firmware/ "
        os.system(cmdline)
        # os.system("i2cset -f -y 1 0x71 0xa1 0x55")
        # os.system("i2cget -f -y 1 0x71 0xa1")
        os.system("echo 0xFFD80004 3 2 > /sys/firmware/zynqmp/config_reg")
        os.system("echo 0 > /sys/class/fpga_manager/fpga0/flags")
        cmdline = "echo " + filename +  " > /sys/class/fpga_manager/fpga0/firmware"
        os.system(cmdline)
        os.system("echo $?")
        os.system("echo 0xFFD80004 3 1 > /sys/firmware/zynqmp/config_reg")
        # os.system("i2cset -f -y 1 0x71 0xa1 0xaa")
        # os.system("i2cget -f -y 1 0x71 0xa1")


class FpgaInstance:
    """fpga interface base class
    """
    TIMEOUT = 0.1

    def __init__(self, master, baseAddr):
        self.master = master
        self.baseAddr = baseAddr

    def readReg(self, regAddr):
        """fpga intance read reg

        Args:
            regAddr (uint32): reg

        Returns:
            [uint32]: [reg value]
        """
        return self.master.read32(self.baseAddr+regAddr)

    def writeReg(self, regAddr, value):
        """fpga interface write reg

        Args:
            regAddr (uint32): reg addr
            value (uint32): reg value to write
        """
        self.master.write32(self.baseAddr + regAddr, value)

    def printconfig(self, len=1):
        """print reg

        Args:
            regAddr (uint32): reg addr
            len (uint32): len of reg
        """
        for i in range(len):
            print(f"{(self.baseAddr+i*4):08x}:{self.readReg(i*4):08x}")

    def done(self, regAddr, mask):
        """wait for operation to complete

        Args:
            regAddr (uint8): offset of base addr
            mask (uint32): mask to check if some bit is 1

        Returns:
            bool: True if tranfer done else False
        """
        now = time.time()
        status = self.readReg(regAddr)
        # self.writeReg(regAddr, mask | status)
        # status = self.readReg(regAddr)
        # print(f"before while status={status:04x}")
        while status & mask == 0 and time.time() < now + self.TIMEOUT:
            status = self.readReg(regAddr)
            # self.writeReg(regAddr, mask | status)
            # status = self.readReg(regAddr)
            time.sleep(0.0001)
            # print(f"before while status={status:04x}")

        if status & mask == 0:
            return False
        else:
            self.writeReg(regAddr, mask)
            return True


class FpgaI2c(FpgaInstance):
    """fpga i2c interface

    Args:
        MmapDevice (class): base mmap device
    """
    CTRL = 0
    PTR = 4
    DATA = 8
    DATA_CTRL = 0x0c
    TRIG = 0x10
    STATUS = 0x10

    def __init__(self, master, baseAddr):
        FpgaInstance.__init__(self, master, baseAddr)

    def read(self, devAddr, regAddr):
        """fpga i2c read byte at dev addr 8 bit

        Args:
            devAddr (uint7): device addr
            regAddr (uint8): device register addr
        """
        ctrl = (0xf7 << 8) | (devAddr << 1) | 0x1
        self.writeReg(self.CTRL, ctrl)
        ptr = regAddr
        self.writeReg(self.PTR, ptr)
        data_ctrl = (1 << 19) | (1 << 3)
        self.writeReg(self.DATA_CTRL, data_ctrl)
        myLock = threading.Lock()
        data = 0
        with myLock:
            self.writeReg(self.TRIG, 0x8000ffff)
            time.sleep(0.001)
            # status = self.readReg(self.STATUS)
            if self.done(self.STATUS, 0x100) == False:
                print("time out i2cdone = 0")
                return -1
            else:
                self.writeReg(self.STATUS, 0x10)
                status = self.readReg(self.STATUS)
                if (status & 0xffff) != 0:
                    print(
                        f"i2c read error at fpga baseAddr 0x{self.baseAddr:04x} devAddr 0x{devAddr:02x} regAddr 0x{regAddr:02x} status 0x{status:04x}")
                    return -1
                else:
                    data = self.readReg(self.DATA) & 0xff
        return data

    def write(self, devAddr, regAddr, value):
        """write i2c value with regaddr8 and value8

        Args:
            devAddr (uint7): device addr
            regAddr (uint8): register addr
            value (uint8): value
        """
        ctrl = (0xc7 << 8) | (devAddr << 1) | 0
        self.writeReg(self.CTRL, ctrl)
        ptr = regAddr
        self.writeReg(self.PTR, ptr)
        self.writeReg(self.DATA, value)
        data_ctrl = (1 << 11) | (1 << 3)
        self.writeReg(self.DATA_CTRL, data_ctrl)
        myLock = threading.Lock()
        data = 0
        with myLock:
            self.writeReg(self.TRIG, 0x8000ffff)
            time.sleep(0.001)
            if self.done(self.STATUS, 0x100) == False:
                print("time out i2cdone = 0")
                return False
            else:
                status = self.readReg(self.STATUS)
                self.writeReg(self.STATUS, 0x100)
                if (status & 0xffff) != 0:
                    print(
                        f"i2c write error at fpga baseAddr {self.baseAddr:04x} devAddr{devAddr:02x} regAddr {regAddr:02x} value {value:02x} status {status:04x}")
                    return False
                else:
                    return True

    def readAddr16(self, devAddr, regAddr):
        """fpga i2c read byte at reg addr 16 bit

        Args:
            devAddr (uint7): device addr
            regAddr (uint16): device register addr 16 bit
        """
        ctrl = (0xf7 << 8) | (devAddr << 1) | 0x1
        self.writeReg(self.CTRL, ctrl)
        # ptr = (regAddr >> 8) | ((regAddr & 0xff) << 8)
        ptr = regAddr
        self.writeReg(self.PTR, ptr)
        data_ctrl = (1 << 19) | (1 << 3) | 1
        self.writeReg(self.DATA_CTRL, data_ctrl)
        myLock = threading.Lock()
        data = 0
        with myLock:
            self.writeReg(self.TRIG, 0x8000ffff)
            time.sleep(0.001)
            # self.writeReg(self.STATUS, 0x10)
            status = self.readReg(self.STATUS)
            if (status & 0x100) == 0:
                print("time out i2cdone = 0")
                return -1
            else:
                self.writeReg(self.STATUS, 0x100)
                status = self.readReg(self.STATUS)
                if (status & 0xffff) != 0:
                    print(
                        f"i2c read error at fpga baseAddr {self.baseAddr:04x} devAddr{devAddr:02x} regAddr {regAddr:02x} status {status:04x}")
                    return -1
                else:
                    data = self.readReg(self.DATA) & 0xff
        return data

    def writeAddr16(self, devAddr, regAddr, value):
        """write i2c value with regaddr16 and value8

        Args:
            devAddr (uint7): device addr
            regAddr (uint16): register addr
            value (uint8): value
        """
        ctrl = (0xc7 << 8) | (devAddr << 1) | 0
        self.writeReg(self.CTRL, ctrl)
        # ptr = (regAddr >> 8) | ((regAddr & 0xff) << 8)
        ptr = regAddr
        self.writeReg(self.PTR, ptr)
        self.writeReg(self.DATA, value)
        data_ctrl = (1 << 11) | (1 << 3) | 1
        self.writeReg(self.DATA_CTRL, data_ctrl)
        myLock = threading.Lock()
        data = 0
        with myLock:
            self.writeReg(self.TRIG, 0x8000ffff)
            time.sleep(0.001)
            # self.writeReg(self.STATUS, 0x10)
            status = self.readReg(self.STATUS)
            if (status & 0x100) == 0:
                print("time out i2cdone = 0")
                return False
            else:
                self.writeReg(self.STATUS, 0x100)
                status = self.readReg(self.STATUS)
                if (status & 0xffff) != 0:
                    print(
                        f"i2c read error at fpga baseAddr {self.baseAddr:04x} devAddr{devAddr:02x} regAddr {regAddr:02x} status {status:04x}")
                    return False
                else:
                    return True


class FpgaMdio(FpgaInstance):
    """base fpga mdio interface

    Args:
        FpgaInstance (class): base class for instance
    """
    MDIO_CMD = 0
    MDIO_RDATA = 4
    TIMEOUT = 0.1

    def __init__(self, master, baseAddr):
        FpgaInstance.__init__(self, master, baseAddr)

    def read(self, devAddr, phyAddr, regAddr):
        """fpga mdio module read default 45

        Args:
            devAddr (uint5): clause45: device addr, clause22:register addr
            phyAddr (uint5): clause45: port addr, clause22:phy addr
            regAddr ([uint16]): reg addr
        """
        # send addr first
        data = 00 << 26 | phyAddr << 21 | devAddr << 16 | regAddr
        myLock = threading.Lock()
        with myLock:
            self.writeReg(self.MDIO_CMD, data | 0x80000000)
            time.sleep(0.01)
            if(self.readReg(self.MDIO_CMD)&0x80000000):
                print("timeout when send addr")
                return -1
            else:
                # send op read
                data = 3 << 26 | phyAddr << 21 | devAddr << 16 | regAddr
                self.writeReg(self.MDIO_CMD, data | 0x80000000)
                time.sleep(0.01)
                if(self.readReg(self.MDIO_CMD)&0x80000000):
                    print("timeout when read data")
                    return -1
                else:            
                    time.sleep(0.01)
                    data = self.readReg(self.MDIO_RDATA)
                    if (data & 0x10000):
                        return data & 0xffff
                    else:
                        print("mdio read data not ready")
                        return -1

    def write(self, devAddr, phyAddr, regAddr, value):
        """fpga mdio write

        Args:
            devAddr (uint5): dev addr
            phyAddr (uint5): phy addr
            regAddr (uint16): reg addr
            value (uint16): reg vaule
        """
        # send addr first
        data = 00 << 26 | phyAddr << 21 | devAddr << 16 | regAddr
        myLock = threading.Lock()
        with myLock:
            self.writeReg(self.MDIO_CMD, data | 0x80000000)
            # send op write
            time.sleep(0.01)
            if(self.readReg(self.MDIO_CMD)&0x80000000):
                print("timeout when send addr")
                return -1
            else:
                data = 1 << 26 | phyAddr << 21 | devAddr << 16 | value
                self.writeReg(self.MDIO_CMD, data | 0x80000000)
                time.sleep(0.01)
                if(self.readReg(self.MDIO_CMD)&0x80000000):
                    print("timeout when write data")
                    return -1



class FpgaSpi(FpgaInstance):
    """base fpga spi interface

    Args:
        FpgaInstance (class): base class for instance
    """
    SPI_CTRL0 = 0x4
    SPI_CTRL1 = 0x8
    SPI_EVENT = 0xc
    SPI_TXD = 0x10
    SPI_RXD = 0x14

    def __init__(self, master, baseAddr):
        FpgaInstance.__init__(self, master, baseAddr)

    def xfer(self, bitLen, outBuf):
        """basic read function

        Args:
            bitLen (uint8): bit len of buf bitlen ,support 16 and 32
            outBuf (uint8 list): buf list 
        """
        if bitLen == 16:
            self.writeReg(self.SPI_CTRL1, 0xf0 | 1 << 14)
            self.writeReg(self.SPI_TXD, outBuf[0] << 8 | outBuf[1])
        elif bitLen == 32:
            self.writeReg(self.SPI_CTRL1, 1 << 14)
            self.writeReg(
                self.SPI_TXD, outBuf[0] << 24 | outBuf[1] << 16 | outBuf[2] << 8 | outBuf[3])
        else:
            print("now only support 16bit and 32 bit")
            return -1

        myLock = threading.Lock()
        with myLock:
            self.writeReg(self.SPI_CTRL0, 1)
            time.sleep(0.001)
            if self.done(self.SPI_EVENT, 0x40):
                data = self.readReg(self.SPI_RXD)
                self.writeReg(self.SPI_CTRL0, 0x80)
                if bitLen == 16:
                    return (data & 0xff)
                else:
                    return [(data & 0xff), (data & 0xff00) >> 8, (data & 0xff0000) >> 16]
            else:
                self.writeReg(self.SPI_CTRL0, 0x80)
                print(
                    f"time out when tranfer status = {self.readReg(self.SPI_EVENT)}")
                return -1

    def read(self, regAddr):
        """fpga read 8 bit reg

        Args:
            regAddr (uint8): register addr
        """
        return self.xfer(16, [regAddr, 0xff])

    def write(self, regAddr, value):
        """write addr8 with value8

        Args:
            regAddr (uint8): reg addr
            value (uint8): value to write 
        """
        self.xfer(16, [regAddr, value])


class FpgaQspi(FpgaInstance):
    """fpga qspi interface 

    support 32 bit only
    wait = 2

    Args:
        FpgaInstance (class): base interface
    """
    QSPI_CTRL = 0
    QSPI_ADDR = 4
    QSPI_DATA = 8
    QSPI_WAIT_CYCLE = 2

    def __init__(self, master, baseAddr):
        FpgaInstance.__init__(self, master, baseAddr)

    def read(self, regAddr):
        """read regiseter 

        Args:
            regAddr (uint32): reg addr
        Return:
            value (uint32): reg value if succeed else -1
        """
        self.writeReg(self.QSPI_ADDR, regAddr)
        myLock = threading.Lock()
        with myLock:
            self.writeReg(self.QSPI_CTRL, 0x20)
            time.sleep(0.1)
            self.writeReg(self.QSPI_CTRL, 0xd0)
            time.sleep(0.1)
            self.writeReg(self.QSPI_CTRL, 0x8)
            time.sleep(0.1)
        return self.readReg(self.QSPI_DATA)

    def write(self, regAddr, value):
        """qspi write

        Args:
            regAddr (uint32): reg addr
            value (uint32): reg value to write
        """
        self.writeReg(self.QSPI_ADDR, regAddr)
        self.writeReg(self.QSPI_DATA, value)
        myLock = threading.Lock()
        with myLock:
            self.writeReg(self.QSPI_CTRL, 0x80)
            time.sleep(0.1)
            self.writeReg(self.QSPI_CTRL, 0xd0)
            time.sleep(0.1)
