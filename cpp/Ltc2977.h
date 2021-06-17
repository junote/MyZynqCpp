#pragma once
#include "BaseClass.h"



class Ltc2977
{
    public:
        Ltc2977(shared_bus_addr8_value8_ptr devBus8, shared_bus_addr8_value16_ptr devBus16, uint8 devAddr):
            devBus8(devBus8),devBus16(devBus16),devAddr(devAddr){}
        ~Ltc2977() = default;
        
        uint8 readByte(uint8 regAddr);
        void writeByte(uint8 regAddr, uint8 value);
        uint16 readWord(uint8 regAddr);
        void writeWord(uint8 regAddr, uint16 value);

        float32 getChannelVoltage(uint8 ch);
        float32 getVolageIn();
        float32 getTemperature();

        int twosComp(uint16 value, uint8 bits);
        int getVoutN();
        float32 decodePmbus(uint16 value);
        uint16 encodePmbus(float32 value);
    private:
        shared_bus_addr8_value8_ptr devBus8;
        shared_bus_addr8_value16_ptr devBus16;
        uint8 devAddr;    
};

