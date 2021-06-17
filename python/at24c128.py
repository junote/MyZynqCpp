import misc
import time
import baseclass


class At24c128(baseclass.BaseAddr16Value8):
    """EEPROM addr16
    """

    def __init__(self, bus, devAddr):
        """init

        Args:
            bus (i2c bus ): i2c bus instance
            devAddr (uint7): dev addr
        """
        self.bus = bus
        self.devAddr = devAddr
        baseclass.BaseAddr16Value8.__init__(self)

    def read8(self, regAddr):
        """read reg

        Args:
            regAddr (uint16): reg addr

        Returns:
            uint8: reg value
        """
        return self.bus.readAddr16(self.devAddr, regAddr)

    def write8(self, regAddr, value):
        """write reg

        Args:
            regAddr (uint8): reg addr
            value (uint8): reg value
        """
        self.bus.writeAddr16(self.devAddr, regAddr, value)

    def printReg(self, regAddr, len=1):
        """print reg

        Args:
            regAddr (uint16): reg addr
            len (int, optional): len of reg. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):04x}]:0x{self.read8(regAddr+i*4):02x}")

    def dump(self):
        """dump 512 bytes
        """
        tmp = []
        for i in range(512):
            tmp.append(self.read8(i))
        misc.hexdump(0, tmp)
