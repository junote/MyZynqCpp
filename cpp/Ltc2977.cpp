#include "Ltc2977.h"
#include <cmath>

uint8 Ltc2977::readByte(uint8 regAddr)
{
    return devBus8->i2cRead(devAddr, regAddr);
}

void Ltc2977::writeByte(uint8 regAddr, uint8 value)
{
    devBus8->i2cWrite(devAddr, regAddr, value);
}

uint16 Ltc2977::readWord(uint8 regAddr)
{
    return devBus16->i2cRead(devAddr, regAddr);
}

void Ltc2977::writeWord(uint8 regAddr, uint16 value)
{
    devBus16->i2cWrite(devAddr, regAddr, value);
}

int Ltc2977::getVoutN()
{
        uint16 tmp = readByte(0x20) & 0x1f;
        return twosComp(tmp,5);
}

int  Ltc2977::twosComp(uint16 value, uint8 bits)
{
    if( (value & (1 << (bits - 1)) )!= 0)
        return (value - (1 << bits));
    else 
        return value;
}

float32 Ltc2977::decodePmbus(uint16 value)
{
    uint16 tmp1 = (value >> 11); 
    uint16 tmp2 = value & 0x7ff;
    return tmp2*( std::exp2(twosComp(tmp1,5)));
     
}
uint16 Ltc2977::encodePmbus(float32 value)
{
    float32 YMAX = 1023.0;
    int NVal = int(log2(value/YMAX));
    int YVal = int(value * (exp2(0-NVal)));
    return ((NVal & 0x1f) << 11)|YVal;
}

float32 Ltc2977::getChannelVoltage(uint8 ch){
    writeByte(0x00,ch);
    int voutN = getVoutN();
    return readWord(0x8b)*(exp2(voutN));
}
float32 Ltc2977::getVolageIn(){
    return decodePmbus(readWord(0x88));
}
float32 Ltc2977::getTemperature(){
    return decodePmbus(readWord(0x8d));
}