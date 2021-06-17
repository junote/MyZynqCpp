#include "BaseClass.h"

class At24c128:public BaseDev<uint16,uint8>
{
    public:
        At24c128(shared_bus_addr16_value8_ptr devBus, uint8 devAddr):
            devBus(devBus),devAddr(devAddr),
            BaseDev<uint16,uint8>(devBus){}
        ~At24c128() = default;
        uint8 read(uint16 regAddr){return devBus->i2cRead(devAddr, regAddr);}
        void write(uint16 regAddr, uint8 value){devBus->i2cWrite(devAddr, regAddr, value);}
    private:
        shared_bus_addr16_value8_ptr devBus;
        uint8 devAddr;
};