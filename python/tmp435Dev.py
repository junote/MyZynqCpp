import baseclass
import time

class Tmp435(baseclass.BaseAddr8Value8):
    """tmp435 temperature sensor

    """
    TEMPERATURE_RESOLUTION = 0.065
    EXTENDED_OFFSET = 64

    def __init__(self, bus, devAddr):
        """tmp 435 init

        Args:
            bus (i2c bus instance): i2c bus
            devAddr (uint7): dev addr
        """
        self.devAddr = devAddr
        self.bus = bus
        self.init()
        baseclass.BaseAddr8Value8.__init__(self)

    def read8(self, regAddr):
        """read register

        Args:
            regAddr (uint8): reg addr

        Returns:
            uint8: reg value
        """
        return self.bus.read(self.devAddr, regAddr)

    def write8(self, regAddr, value):
        """reg write

        Args:
            regAddr (uint8): reg addr
            value (uint8): reg addr
        """
        self.bus.write(self.devAddr, regAddr, value)

    def printReg(self, regAddr, len=1):
        """print reg

        Args:
            regAddr (uint16): reg addr
            len (int, optional): len of reg. Defaults to 1.
        """
        for i in range(len):
            print(f"[0x{(regAddr +  i):04x}]:0x{self.read8(regAddr+i):02x}")

    def init(self):
        """dev init and normal config
        """
        # soft reset
        self.write8(0xfc, 1)
        # set extend range mode
        self.write8(0x03, (self.read8(0x3) | 0x4))
        # set conversion rate 1 Hz
        self.write8(0x0a, 4)
        time.sleep(1)

    def dispTemp(self):
        """display temperature
        """
        print("TMP435 STATUS:")
        local_temp = self.read8(0) - self.EXTENDED_OFFSET
        local_temp += (self.read8(0x15) >> 4) * self.TEMPERATURE_RESOLUTION
        remote_temp = self.read8(1) - self.EXTENDED_OFFSET
        remote_temp += (self.read8(0x10) >> 4) * self.TEMPERATURE_RESOLUTION
        print("local temperature: ",  "%3.2f" % local_temp, "degC")
        print("remote temperature: ",  "%3.2f" % remote_temp, "degC")
    
    def localTemp(self):
        """get local temperature

        Returns:
            double: local temperatue
        """
        local_temp = self.read8(0) - self.EXTENDED_OFFSET
        local_temp += (self.read8(0x15) >> 4) * self.TEMPERATURE_RESOLUTION   
        return local_temp
    
    def remoteTemp(self):
        """remote temperature

        Returns:
            double: remote temperatue
        """
        remote_temp = self.read8(1) - self.EXTENDED_OFFSET
        remote_temp += (self.read8(0x10) >> 4) * self.TEMPERATURE_RESOLUTION        
        return remote_temp

    def dump(self):
        """dump register
        """
        print("TMP435 readable registers:")
        print("Local Temp High Byte               [00h]: ", "0x%02x" % (
            self.read8(0x00)))
        print("Remote Temp High Byte              [01h]: ", "0x%02x" % (
            self.read8(0x01)))
        print("Status Register                    [02h]: ", "0x%02x" % (
            self.read8(0x02)))
        print("Configuration 1                    [03h]: ", "0x%02x" % (
            self.read8(0x03)))
        print("Conversion Rate                    [05h]: ", "0x%02x" % (
            self.read8(0x05)))
        print("Local Temp Hight Limit High Byte   [05h]: ", "0x%02x" % (
            self.read8(0x05)))
        print("Local Temp Low Limit High Byte     [06h]: ", "0x%02x" % (
            self.read8(0x06)))
        print("Remote Temp Hight Limit High Byte  [07h]: ", "0x%02x" % (
            self.read8(0x07)))
        print("Remote Temp Low Limit High Byte    [08h]: ", "0x%02x" % (
            self.read8(0x08)))
        print("Remote Temp Low Byte               [10h]: ", "0x%02x" % (
            self.read8(0x10)))
        print("Remote Temp Hight Limit Low Byte   [13h]: ", "0x%02x" % (
            self.read8(0x13)))
        print("Remote Temp Low Limit Low Byte     [14h]: ", "0x%02x" % (
            self.read8(0x14)))
        print("Local Temp Low Byte                [15h]: ", "0x%02x" % (
            self.read8(0x15)))
        print("Local Temp Hight Limit Low Byte    [16h]: ", "0x%02x" % (
            self.read8(0x16)))
        print("Local Temp Low Limit Low Byte      [17h]: ", "0x%02x" % (
            self.read8(0x17)))
        print(
            "N-Correction                         [18h]: ", "0x%02x" % (self.read8(0x18)))
        print("Remote Therm Limit                 [19h]: ", "0x%02x" % (
            self.read8(0x19)))
        print("Configuration 2                    [0Ah]: ", "0x%02x" % (
            self.read8(0x0A)))
        print("Channel Mask                       [1Fh]: ", "0x%02x" % (
            self.read8(0x1F)))
        print("Local Therm Limit                  [20h]: ", "0x%02x" % (
            self.read8(0x20)))
        print("Therm Hysteresis                   [21h]: ", "0x%02x" % (
            self.read8(0x21)))
        print("Consecutive Alert                  [22h]: ", "0x%02x" % (
            self.read8(0x22)))
        print("Beta Compensation                  [25h]: ", "0x%02x" % (
            self.read8(0x25)))
        print("Device ID                          [FDh]: ", "0x%02x" % (
            self.read8(0xFD)))
        print("Manufacturer ID                    [FEh]: ", "0x%02x" % (
            self.read8(0xFE)))
