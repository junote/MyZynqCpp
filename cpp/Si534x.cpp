#include "Si534x.h"

uint8 Si534x::read(uint8 regAddr)
{   
    return devBus->i2cRead(devAddr, (regAddr & 0xff));
}

void Si534x::write(uint8 regAddr, uint8 value)
{
    devBus->i2cWrite(devAddr, (regAddr & 0xff), value);
}

void Si534x::setPage(uint8 page)
{
    devBus->i2cWrite(devAddr, 1, page);

}