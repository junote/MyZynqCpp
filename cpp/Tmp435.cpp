#include "Tmp435.h"

Tmp435::Tmp435(shared_bus_addr8_value8_ptr devBus, uint8 devAddr):
            devBus(devBus),devAddr(devAddr),
            BaseDev(devBus)
{
    init();
}

uint8 Tmp435::read(uint8 regAddr)
{
    return devBus->i2cRead(devAddr, regAddr);
}
void Tmp435::write(uint8 regAddr, uint8 value)
{
    devBus->i2cWrite(devAddr, regAddr, value);
}

void Tmp435::init()
{
    using namespace std::chrono_literals;

    //soft reset
    write(0xfc, 1);
    //set extend range mode
    write(0x03, (read(0x03)|0x04));
    //set rate 1Hz
    write(0x0a, 4);
    std::this_thread::sleep_for(1s);

}
float32 Tmp435::getLocalTemperature()
{
    float32 tmp = (read(0) - EXTENDED_OFFSET) + (read(0x15) >> 4)*TEMPERATURE_RESOLUTION;
    return tmp;
}
float32 Tmp435::getRemoteTemperature()
{
    float32 tmp = (read(1) - EXTENDED_OFFSET) + (read(0x10) >> 4)*TEMPERATURE_RESOLUTION;
    return tmp;    
}