import json
import os
import at24c128
import time
import tlv
from zlib import crc32


class MfgEprom(at24c128.At24c128):
    """write and dump eprom
    """
    def __init__(self, bus, devAddr, file):

        self.file = os.path.join(os.getenv('PYTHONPATH'), file)
        self.binFile = self.file.replace(".json", ".bin")
        self.EepromRW = os.path.join(os.getenv('PYTHONPATH'), 'EepromRW')
        at24c128.At24c128.__init__(self, bus, devAddr)

    def getBinFile(self):
        os.system("%s -i %s -o %s" % (self.EepromRW, self.file, self.binFile))

    def dumpBinFile(self):
        os.system("%s -r %s" % (self.EepromRW, self.binFile))

    def writeBinfile(self):
        with open(self.binFile, "rb") as f:
            data = f.read()
            for i in range(len(data)):
                self.write8(i, data[i])
                time.sleep(0.002)

    def getTagValue(self, *tag):
        tags = (len(tag))
        with open(self.file, "r", encoding='utf-8') as f:
            tlv = json.load(f)
            if (tags == 1):
                print(tlv[tag[0]])
            elif (tags == 2):
                print(tlv[tag[0]][tag[1]])
            elif (tags == 3):
                print(tlv[tag[0]][tag[1]][tag[2]])
            elif (tags == 4):
                print(tlv[tag[0]][tag[1]][tag[2]][tag[3]])
            else:
                print("Please input tag for query!")

    def setTagValue(self, *tag):
        tags = (len(tag)) - 1
        with open(self.file, "r", encoding='utf-8') as fr:
            tlv = json.load(fr)
            if (tags == 1):
                tlv[tag[0]] = tag[1]
            elif (tags == 2):
                tlv[tag[0]][tag[1]] = tag[2]
            elif (tags == 3):
                tlv[tag[0]][tag[1]][tag[2]] = tag[3]
            elif (tags == 4):
                tlv[tag[0]][tag[1]][tag[2]][tag[3]] = tag[4]
            else:
                print("Please input tag for write!")

        with open(self.file, "w", encoding='utf-8') as fw:
            json.dump(tlv, fw, indent='\t')

    def showTlv(self, show_names: bool = True):
        config = {
            0x11: {
                'type': 'str',
                'name': 'Pon'
            },
            0x12: {
                'type': 'bytes',
                'name': 'MacList'
            },
            0x13: {
                'type': 'int',
                'name': 'DramSize'
            },
            0x14: {
                'type': 'int',
                'name': 'BootFlashSize'
            },
            0x15: {
                'type': 'int',
                'name': 'FdrFlashSize'
            },
            0x16: {
                'type': 'int',
                'name': 'FcpFwClass'
            },
            0x17: {
                'type': 'int',
                'name': 'FruWidth'
            },
            0x18: {
                'type': 'bytes',
                'name': 'CalibData'
            },
            0x19: {
                'type': 'str',
                'name': 'CleiCode'
            },
            0x1a: {
                'type': 'str',
                'name': 'FinalAssPartNo'
            },
            0x1b: {
                'type': 'int',
                'name': 'MfgProcessStatus'
            },
            0x1c: {
                'type': 'str',
                'name': 'MfgFinalAssRev'
            },
            0x1d: {
                'type': 'int',
                'name': 'TestStatus'
            },
            0x1e: {
                'type': 'str',
                'name': 'FinalAssSerNo'
            },
            0x1f: {
                'type': 'int',
                'name': 'SoftwareSupVers'
            },
            0x20: {
                'type': 'bytes',
                'name': 'ECI'
            },
            0x21: {
                'type': 'str',
                'name': 'ProductName'
            },
            0x22: {
                'type': 'str',
                'name': 'PartNo'
            },
            0x23: {
                'type': 'str',
                'name': 'SerialNo'
            },
            0x24: {
                'type': 'bytes',
                'name': 'MacBase'
            },
            0x25: {
                'type': 'str',
                'name': 'MfgDate'
            },
            0x26: {
                'type': 'int',
                'name': 'DeviceVers'
            },
            0x27: {
                'type': 'str',
                'name': 'LabelVer'
            },
            0x28: {
                'type': 'str',
                'name': 'PlatformName'
            },
            0x29: {
                'type': 'str',
                'name': 'OnieVers'
            },
            0x2a: {
                'type': 'int',
                'name': 'MacNum'
            },
            0x2b: {
                'type': 'str',
                'name': 'Manufacture'
            },
            0x2c: {
                'type': 'str',
                'name': 'CountryCode'
            },
            0x2d: {
                'type': 'str',
                'name': 'Vendor'
            },
            0x2e: {
                'type': 'str',
                'name': 'DiagVers'
            },
            0x2f: {
                'type': 'str',
                'name': 'Servicetag'
            },
            0x30: {
                'type': 'int',
                'name': 'DtrBoardCount'
            },
            0x31: {
                'type': 'str',
                'name': 'DtrBoardSnList'
            },
            0x32: {
                'type': 'str',
                'name': 'DtrBoardPnList'
            },
            0x33: {
                'type': 'int',
                'name': 'SubType'
            },
            0xfd: {
                'type': 'str',
                'name': 'VendorExt'
            }
        }

        t = tlv.TLV()
        t.set_tag_map(config)

        buf = []
        for i in range(512):
            buf.append(self.read8(i))

        data = bytes(buf)
        s = int.from_bytes(data[16:18], byteorder='big')
        e = int.from_bytes(data[18:20], byteorder='big')
        print("TLV start at %d and end at %d" % (s, e))

        calc_crc32 = crc32(data[:508])
        read_crc32 = int.from_bytes(data[508:512], byteorder='big')
        if (calc_crc32 != read_crc32):
            print(
                f"Checksum verify failed! invalid eeprom content! calc_crc32:{hex(calc_crc32)}"
            )
            return

        new = data[s:e]
        t.parse_array(new)
        print(t.tree(offset=4, use_names=show_names))

    def showHeader(self):
        vendor = ""
        for i in range(8):
            vendor = vendor + chr(self.read8(i))
        version = self.read8(8)
        total_size = (self.read8(9) << 8) + self.read8(10)
        device_type = (self.read8(11) << 8) + self.read8(12)
        device_model = (self.read8(13) << 8) + self.read8(14)
        hwver = self.read8(15)
        tlv_start = (self.read8(16) << 8) + self.read8(17)
        tlv_end = (self.read8(18) << 8) + self.read8(19)
        bsa = ""
        for i in range(20, 44):
            bsa = bsa + chr(self.read8(i))
        print(f"Vendor-Info      : {vendor}")
        print(f"Version          : {version}")
        print(f"Total-size       : {total_size}")
        print(f"Device-Type      : {device_type}")
        print(f"Device-Model     : {device_model}")
        print(f"Hardware Revision: {hwver}")
        print(f"TLV-StartOffset  : {tlv_start}")
        print(f"TLV-EndOffset    : {tlv_end}")
        print(f"BSA              : {bsa}")

    def showAll(self):
        self.showHeader()
        print("="*40)
        self.showTlv()

    def setSn(self, sn='BQ0180228'):
        self.setTagValue('EepromTlvArea', 'FinalAssSerNoTlv', 'FinalAssSerNo',
                         sn)

    def setMacAddr(self, macaddr='b22a9fe30d27'):
        maclist = []
        for i in range(6):
            maclist.append(macaddr[i * 2:i * 2 + 2])

        self.setTagValue('EepromTlvArea', 'MacBaseTlv', 'BaseMac', maclist)
