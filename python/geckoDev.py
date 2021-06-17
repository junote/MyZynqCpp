from smbus2 import SMBusWrapper, i2c_msg
import baseclass


class Gecko(baseclass.BaseAddr8Value8):
    """12v current sensor
    """

    def __init__(self, busId, devAddr):
        self.busId = busId
        self.devAddr = devAddr
        baseclass.BaseAddr8Value8.__init__(self)

    def read8(self, regAddr):
        """read reg

        Args:
            regAddr (uint8): reg adr

        Returns:
            uint16: reg value
        """
        write_buf = i2c_msg.write(self.devAddr, [regAddr])
        read_buf = i2c_msg.read(self.devAddr, 1)
        with SMBusWrapper(self.busId) as bus:
            bus.i2c_rdwr(write_buf, read_buf)
        return ord(read_buf.buf[0])

    def write8(self, regAddr, value):
        """write reg value

        Args:
            regAddr (uint8): reg addr
            value (uint8): reg value
        """
        write_buf = i2c_msg.write(self.devAddr, [regAddr, value & 0xff])
        with SMBusWrapper(self.busId) as bus:
            bus.i2c_rdwr(write_buf)


