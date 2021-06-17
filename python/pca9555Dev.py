import baseclass


class Pca9555(baseclass.BaseAddr8Value8):
    """i2c io mux
    """

    def __init__(self, bus, devAddr):
        self.bus = bus
        self.devAddr = devAddr
        baseclass.BaseAddr8Value8.__init__(self)

    def read8(self, regAddr):
        """read reg

        Args:
            regAddr (uint8): reg addr

        Returns:
            uint8: reg value
        """
        return self.bus.read(self.devAddr, regAddr)

    def write8(self, regAddr, value):
        """write reg

        Args:
            regAddr (uint8): reg addr
            value (uint8): value
        """
        self.bus.write(self.devAddr, regAddr, value)

    def printReg(self, regAddr, len=1):
        """print reg

        Args:
            regAddr (uint16): reg addr
            len (int, optional): len of reg. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):02x}]:0x{self.read8(regAddr+i):02x}")

    def configPortOut(self, port, out=True):
        """set port input

        Args:
            port (uint8): 0-17 same as sch
            input (bool): True = input or False = output
        """
        regAddr = 7 if port >= 10 else 6
        port = port - 10 if port >= 10 else port
        tmp = self.read8(regAddr)
        if out:
            value = tmp & ~(1 << port)
            self.write8(regAddr, value)
        else:
            value = tmp | (1 << port)
            self.write8(regAddr, value)

    def setOutPortHigh(self, port, high=True):
        regAddr = 3 if port >= 10 else 2
        port = port - 10 if port >= 10 else port
        tmp = self.read8(regAddr)
        if high:
            value = tmp | (1 << port)
            self.write8(regAddr, value)
        else:
            value = tmp & ~(1 << port)
            self.write8(regAddr, value)
