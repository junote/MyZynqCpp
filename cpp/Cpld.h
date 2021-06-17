#pragma once
#include <string>
#include <array>
#include "ZynqSpiDev.h"
#include "BaseClass.h"

class Cpld:public BaseDev<uint8,uint8>
{
    public:
        Cpld(shared_bus_addr8_value8_ptr devBus):devBus(devBus),BaseDev<uint8,uint8>(devBus){}
        ~Cpld(){}
        uint8 read(uint8 regAddr){return devBus->busRead(regAddr);}
        void write(uint8 regAddr, uint8 value){devBus->busWrite(regAddr, value);}

 
    
    private:
        // std::string devName  = "spidev0.0";
        // ZynqSpiDev bus;
        shared_bus_addr8_value8_ptr devBus;

};

template<typename AddrType,typename ValueType>
class CpldGenericI2cBus:public BaseBus<AddrType,ValueType>
{
    public:
        CpldGenericI2cBus(shared_dev_addr8_value8_ptr dev, uint8 baseAddr):dev(dev),
                            baseAddr(baseAddr),BaseBus<AddrType,ValueType>(){}
        ~CpldGenericI2cBus(){}
        ValueType i2cRead(uint8 devAddr, AddrType regAddr);
        void i2cWrite(uint8 devAddr, AddrType regAddr, ValueType value);
        bool checkI2cDone();
    private:
        uint8 readReg(uint8 regAddr){return dev->read((uint8)(baseAddr + regAddr));}
        void writeReg(uint8 regAddr, uint8 value){dev->write((uint8)(baseAddr + regAddr), value);}
        shared_dev_addr8_value8_ptr dev;
        uint8 baseAddr;
        const uint8 REG_CTRL = 0x00;
        const uint8 REG_PTR1 = 0x01;
        const uint8 REG_PTR2 = 0x02;
        const uint8 REG_DEVADDR = 0x03;
        const uint8 REG_WDATA1 = 0x04;
        const uint8 REG_WDATA2 = 0x05;
        const uint8 REG_RDATA1 = 0x06;
        const uint8 REG_RDATA2 = 0x07;    
};


class CpldOpenI2cBus
{
    public:
        CpldOpenI2cBus(shared_dev_addr8_value8_ptr dev,uint8 baseAddr):dev(dev),baseAddr(baseAddr){}
        ~CpldOpenI2cBus(){}
        void startTransfer(uint8 value, bool read);
        template<size_t N>
        void transfer(std::array<uint8, N> dataIn, std::array<uint8, N> dataOut,bool read);
        bool checkI2cDone();

    private:
        uint8 readReg(uint8 regAddr){return dev->read((uint8)(baseAddr + regAddr));}
        void writeReg(uint8 regAddr, uint8 value){dev->write((uint8)(baseAddr + regAddr), value);}
        shared_dev_addr8_value8_ptr dev;
        uint8 baseAddr;

        const uint8 REG_CTRL = 0x00;
        const uint8 REG_TXDATA = 0x01;
        const uint8 REG_RXDATA = 0x01;
        const uint8 REG_CMD = 0x2;
        const uint8 REG_STAT = 0x2;
};

