#pragma once
#include <iostream>

#include "BaseClass.h"
#include "Cpld.h"

class Si534x:public BaseDev<uint8,uint8>
{
    public:
        Si534x(shared_bus_addr8_value8_ptr devBus, uint8 devAddr):
            devBus(devBus),devAddr(devAddr),
            BaseDev<uint8,uint8>(devBus){}
        ~Si534x() = default;
        uint8 read(uint8 regAddr);
        void write(uint8 regAddr, uint8 value);
        void setPage(uint8 page);
    private:
        shared_bus_addr8_value8_ptr devBus;
        uint8 devAddr;
};