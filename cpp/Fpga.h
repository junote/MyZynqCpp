#pragma once
#include <string>
#include "types.h"
#include "Mmap32.h"
#include "BaseClass.h"

class Fpga:public BaseDev<uint32,uint32>
{
    public:
        Fpga(shared_bus_addr32_value32_ptr devBus):devBus(devBus),BaseDev<uint32,uint32>(devBus){}
        ~Fpga(){}
        uint32 read(uint32 regAddr){return devBus->busRead(regAddr);}
        void write(uint32 regAddr, uint32 value){devBus->busWrite(regAddr, value);}
    
    private:
        // std::string devName  = "mem";
        // uint32 offset = 0x43c00000;
        // uint32  size=0x10000;
        shared_bus_addr32_value32_ptr devBus;
};


// class FpgaInstance
// {
//     public:
//         FpgaInstance(BaseBus* devBus, uint32 baseAddr):devBus(devBus),baseAddr(baseAddr){}
//         ~FpgaInstance(){}
//         uint32 readReg(uint32 regAddr){return devBus->read32(baseAddr + regAddr);}
//         void writeReg(uint32 regAddr, uint32 value){devBus->write32((baseAddr + regAddr), value);}
    
//     private:
//         BaseBus* devBus;
//         uint32 baseAddr;
// };

// class FpgaGenericI2c:public FpgaInstance, BaseBus
// {
// public:
//     public:
//         FpgaGenericI2c(BaseBus* devBus, uint32 baseAddr, uint8 devAddr):devBus(devBus),baseAddr(baseAddr),devAddr(devAddr),
//             FpgaInstance(devBus,baseAddr),BaseBus(){}
//         ~FpgaGenericI2c(){}
//         uint8 read8(uint8 regAddr);
//         void write8(uint8 regAddr, uint8 value);
    
//     private:
//         BaseBus* devBus;
//         uint32 baseAddr;
//         uint8 devAddr;
//         const uint8 I2cIrqCtl =  0x00;
//         const uint8 I2cIrqEn = 0x04;
//         const uint8 I2cCtl = 0x08;
//         const uint8 I2cAddr = 0x0c;
//         const uint8 I2cWData = 0x10;
//         const uint8 I2cRData = 0x14;
// };