#include "BaseClass.h"

class Tmp435:public BaseDev<uint8,uint8>
{
    public:
        Tmp435(shared_bus_addr8_value8_ptr devBus, uint8 devAddr);
        ~Tmp435() = default;
        uint8 read(uint8 regAddr);
        void write(uint8 regAddr, uint8 value);
        void init();
        float32 getLocalTemperature();
        float32 getRemoteTemperature();
    private:
        shared_bus_addr8_value8_ptr devBus;
        uint8 devAddr;
        const uint8 EXTENDED_OFFSET = 64;
        const float32 TEMPERATURE_RESOLUTION = 0.065;
};