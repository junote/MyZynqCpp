class BaseAddr32Value32():
    """base class for addr 32 bit, value 32 bit
    """

    def __init__(self):
        pass

    def read32(self, regAddr):
        pass

    def write32(self, regAddr, value):
        pass

    def read(self, regAddr, len=1):
        if (regAddr % 4 != 0):
            print("reg addr must 4x")
        else:
            print("read:")
            for i in range(len):
                print(
                    f"[0x{(regAddr + 4 * i):08x}]:0x{self.read32(regAddr+i*4):08x}")

    def write(self, regAddr, value):
        if (regAddr % 4 != 0):
            print("reg addr must 4x")
        else:
            self.write32(regAddr, value)
            print(f"write [0x{(regAddr):08x}]:0x{value:08x}")


class BaseAddr16Value16():
    """base class for addr 16 bit, value 16 bit
    """

    def __init__(self):
        pass

    def read16(self, regAddr):
        pass

    def write16(self, regAddr, value):
        pass

    def read(self, regAddr, len=1):
        print("read:")
        for i in range(len):
            print(f"[0x{(regAddr + i):04x}]:0x{self.read16(regAddr + i):04x}")

    def write(self, regAddr, value):
        self.write16(regAddr, value)
        print(f"write [0x{(regAddr):04x}]:0x{value:04x}")


class BaseAddr16Value8():
    """base class for addr 16 bit, value 8 bit
    """

    def __init__(self):
        pass

    def read8(self, regAddr):
        pass

    def write8(self, regAddr, value):
        pass

    def read(self, regAddr, len=1):
        print("read:")
        for i in range(len):
            print(f"[0x{(regAddr + i):04x}]:0x{self.read8(regAddr + i):02x}")

    def write(self, regAddr, value):
        self.write8(regAddr, value)
        print(f"write [0x{(regAddr):04x}]:0x{value:02x}")


class BaseAddr8Value8():
    """base class for addr 32 bit, value 32 bit
    """

    def __init__(self):
        pass

    def read8(self, regAddr):
        pass

    def write8(self, regAddr, value):
        pass

    def read(self, regAddr, len=1):
        print("read:")
        for i in range(len):
            print(f"[0x{(regAddr + i):02x}]:0x{self.read8(regAddr + i):02x}")

    def write(self, regAddr, value):
        self.write8(regAddr, value)
        print(f"write [0x{(regAddr):02x}]:0x{value:02x}")


class BaseAddr8Value16():
    """base class for addr 32 bit, value 32 bit
    """

    def __init__(self):
        pass

    def read8(self, regAddr):
        pass

    def write8(self, regAddr, value):
        pass

    def read(self, regAddr, len=1):
        print("read:")
        for i in range(len):
            print(f"[0x{(regAddr + i):02x}]:0x{self.read8(regAddr + i):04x}")

    def write(self, regAddr, value):
        self.write8(regAddr, value)
        print(f"write [0x{(regAddr):02x}]:0x{value:04x}")
