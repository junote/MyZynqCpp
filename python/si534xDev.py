import time
import misc
import baseclass


class Si534x(baseclass.BaseAddr16Value8):
    def __init__(self, bus, devAddr):
        """Si534x

        Args:
            bus (instancd): i2c bus instance
            devAddr (uint7): dev addr
        """
        self.bus = bus
        self.devAddr = devAddr
        # print("grade:", self.read8(4))
        # print("rev:", self.read8(5))
        baseclass.BaseAddr16Value8.__init__(self)

    def read8(self, regAddr):
        """read

        Args:
            regAddr (uint16): dev addr

        Returns:
            uint8: reg value
        """
        # write page first
        self.bus.write(self.devAddr, 1, int(regAddr/0x100))
        return self.bus.read(self.devAddr, (regAddr % 0x100))

    def printReg(self, regAddr, len=1):
        """print reg

        Args:
            regAddr (uint16): reg addr
            len (int, optional): len of reg. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):04x}]:0x{self.read8(regAddr+i):02x}")

    def write8(self, regAddr, value):
        """write reg

        Args:
            regAddr (uint16): reg addr
            value (uint8): reg value
        """
        self.bus.write(self.devAddr, 1, int(regAddr/0x100))
        self.bus.write(self.devAddr, (regAddr % 0x100), value)

    def write_file(self, file):
        """config clock from file

        Args:
            file (string): file path + name
        """
        with open(file, "r") as f:
            lines = f.readlines()
        pre = {}
        mid = {}
        post = {}
        index = 0
        for i, line in enumerate(lines):
            if "0x" in line:
                pre[int(line[:6], base=16)] = int(line[7:], base=16)
            if "End configuration preamble" in line:
                index = i
                break
        for i, line in enumerate(lines[(index+1):]):
            if "0x" in line:
                mid[int(line[:6], base=16)] = int(line[7:], base=16)
            if "End configuration registers" in line:
                index = i
                break
        for line in enumerate(lines[(index+1):]):
            if "0x" in line:
                post[int(line[:6], base=16)] = int(line[7:], base=16)
        for addr in pre.keys():
            self.write8(addr, pre[addr])
        time.sleep(1)
        for addr in  mid.keys():
            self.write8(addr, mid[addr])
        for addr in post.keys():
            self.write8(addr, post[addr])

    def dump_page(self, page_no):
        self.write8(1, page_no)
        tmp = []
        for i in range(256):
            tmp.append(self.bus.read(self.devAddr, i))
        misc.hexdump(0, tmp)

    def status(self):
        pass
