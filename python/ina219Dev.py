from smbus2 import SMBusWrapper, i2c_msg
import math
import time
import baseclass


class Ina219(baseclass.BaseAddr8Value16):
    """12v current sensor
    """

    def __init__(self, busId, devAddr, calc=0x1120):
        self.busId = busId
        self.devAddr = devAddr
        self.calc = calc
        self.init()
        baseclass.BaseAddr8Value16.__init__(self)

    def read8(self, regAddr):
        """read reg

        Args:
            regAddr (uint8): reg adr

        Returns:
            uint16: reg value
        """
        write_buf = i2c_msg.write(self.devAddr, [regAddr])
        read_buf = i2c_msg.read(self.devAddr, 2)
        with SMBusWrapper(self.busId) as bus:
            bus.i2c_rdwr(write_buf, read_buf)
        return (ord(read_buf.buf[0]) << 8) + ord(read_buf.buf[1])

    def printReg(self, regAddr, len=1):
        """print reg

        Args:
            Reg (uint8): reg addr
            len (int, optional): len. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):02x}]:0x{self.read8(regAddr+i):04x}")

    def write8(self, regAddr, value):
        """write reg value

        Args:
            regAddr (uint8): reg addr
            value (uint16): reg value
        """
        write_buf = i2c_msg.write(
            self.devAddr, [regAddr, (value >> 8), (value & 0xff)])
        with SMBusWrapper(self.busId) as bus:
            bus.i2c_rdwr(write_buf)

    def init(self):
        """init config register
        """
        # reset
        self.write8(0x0, 0x8000)
        time.sleep(0.01)
        # write config
        self.write8(0x0, 0x199f)
        # write cal current lsb=0.001
        self.write8(0x5, self.calc << 1)

    def status(self):
        """print device voltage,current,power
        """
        print("INA status:")
        time.sleep(0.01)

        voltage = (self.read8(0x2) >> 3) * 4/1000
        print(f"volate: {voltage:.4f}V")
        current = self.read8(0x4)*0.001
        print(f"current: {current:.4f} A")
        power = self.read8(0x3)*0.001*20
        print(f"power:{power:.4f}W")
