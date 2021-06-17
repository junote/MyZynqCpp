#pragma once
#include <memory>

#include "types.h"




template<typename AddrType,typename ValueType>
class BaseBus
{
    public:
        ~BaseBus()=default;
        virtual ValueType busRead(AddrType regAddr){return 0;}
        virtual void busWrite(AddrType regAddr, ValueType value){}

        virtual ValueType i2cRead(uint8 devAddr, AddrType regAddr){return 0;}
        virtual void i2cWrite(uint8 devAddr, AddrType regAddr, ValueType value){}
};

using shared_bus_addr8_value8_ptr = std::shared_ptr<BaseBus<uint8,uint8>>;
using shared_bus_addr8_value16_ptr = std::shared_ptr<BaseBus<uint8,uint16>>;
using shared_bus_addr16_value8_ptr = std::shared_ptr<BaseBus<uint16,uint8>>;
using shared_bus_addr32_value32_ptr = std::shared_ptr<BaseBus<uint32,uint32>>;

template<typename AddrType,typename ValueType>
class BaseDev
{
    public:
        BaseDev(std::shared_ptr<BaseBus<AddrType,ValueType>> devBus):devBus(devBus){}
        ~BaseDev()=default;

        virtual ValueType read(AddrType regAddr){return 0;};
        virtual void write(AddrType regAddr, ValueType value){};

    private:
        std::shared_ptr<BaseBus<AddrType,ValueType>> devBus;
};
using shared_dev_addr8_value8_ptr = std::shared_ptr<BaseDev<uint8,uint8>>;
using shared_dev_addr32_value32_ptr = std::shared_ptr<BaseDev<uint32,uint32>>;







// class PmbusDev
// {
// public:
//     PmbusDev(shared_basebus_ptr devBus, uint8 devAddr):devBus(devBus),devAddr(devAddr){}
//     ~PmbusDev()=default;
    
//     virtual uint8 readByte(uint8 regAddr){return 0xde;}
//     virtual void writeByte(uint8 regAddr, uint8 value){}

//     virtual uint16 readWord(uint8 regAddr){return 0xdead;}
//     virtual void writeWord(uint8 regAddr, uint16 value){}   

//     float32 getChannelVoltage(uint8 ch){
//         writeByte(0x00,ch);
//         double voutN = getVoutN();
//         return readWord(0x8b)*(exp2(voutN));
//     }
//     float32 getVolageIn(){
//         return decodePmbus(readWord(0x88));
//     }
//     float32 getTemperature(){
//         return decodePmbus(readWord(0x8d));
//     }

//     inline uint16 twosComp(uint16 value, uint8 bits){
//         if( (value & (1 << (bits - 1)) )!= 0)
//             return (value - (1 << bits));
//         else 
//             return value;
//     }
//     uint16 getVoutN(){
//         uint16 tmp = readByte(0x20) & 0x1f;
//         return twosComp(tmp,5);
//     }
//     float32 decodePmbus(uint16 value){
//         uint16 tmp1 = (value >> 11); 
//         uint16 tmp2 = value & 0x7ff;
//         return tmp2*( std::exp2(twosComp(tmp1,5)));
         
//     }
//     uint16 encodePmbus(float value){
//         float32 YMAX = 1023.0;
//         uint32 NVal = uint32(log2(value/YMAX));
//         uint32 YVal = uint32(value * (exp2(0-NVal)));
//         return ((NVal & 0x1f) << 11)|YVal;
//     }

// private:
//     shared_basebus_ptr devBus;
//     uint8 devAddr;
// };
// using shared_PmbusDev_ptr = std::shared_ptr<PmbusDev>;