import time
import baseclass


class Zl3064x(baseclass.BaseAddr16Value8):
    """clock zl3064x support spi now 
    """

    def __init__(self, bus):
        """init

        Args:
            bus (spi instance): spi instance
        """
        self.bus = bus
        baseclass.BaseAddr16Value8.__init__(self)

    def read8(self, regAddr):
        """read reg

        Args:
            regAddr (uint16): reg addr

        Returns:
            uint8: reg value
        """
        self.bus.write(0x7f, regAddr >> 8)
        return self.bus.read(0x80 | (regAddr & 0xff))

    def write8(self, regAddr, value):
        """write reg 

        Args:
            regAddr (uint16): reg addr
            value (uint8): value
        """
        self.bus.write(0x7f, regAddr >> 8)
        self.bus.write((regAddr & 0xff), value)

    def printReg(self, regAddr, len=1):
        """print reg value

        Args:
            regAddr (uint16): reg addr
            len (int, optional): reg num. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):04x}]:0x{self.read8(regAddr+i):02x}")

    def readSticky(self, regAddr):
        """read sticky register

        Args:
            regAddr (uint16): reg addr

        Returns:
            uint8: reg value
        """
        self.write8(0x180, 0x1)
        self.write8(regAddr, 0x00)
        self.write8(0x180, 0x0)
        time.sleep(0.025)
        return self.read8(regAddr)

    def writeFile(self, filePath):
        pass
