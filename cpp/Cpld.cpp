#include <iostream>
#include <thread>
#include <chrono>
#include "Cpld.h"

template<typename AddrType,typename ValueType> 
bool  CpldGenericI2cBus<AddrType,ValueType>::checkI2cDone()
{
    using namespace std::chrono_literals;
    uint8 status;
    int i = 0;
    std::this_thread::sleep_for(200ns);

    for(i = 0; i < 200; i++)
    {
        status = readReg(REG_CTRL);
        if (status & 0x80) break;
        std::this_thread::sleep_for(10ns);
    }
    if(i == 200)
    {
        devWarnLog("cpld i2c tranfer timeout status=0x{0:2x}",status);
        return false;
    }
    if(status & 0x40)
    {
        devWarnLog("cpld I2C access failure status=0x{0:2x}",status);
        return false;
    }

    return true;
}

template<typename AddrType,typename ValueType> 
ValueType CpldGenericI2cBus<AddrType,ValueType>::i2cRead(uint8 devAddr, AddrType regAddr)
{
    ValueType ret;
    //write regAdd
    if(sizeof(AddrType) == 1){
        writeReg(REG_PTR1,regAddr & 0xff);
    }else if(sizeof(regAddr) == 2){
        writeReg(REG_PTR1,regAddr >> 8);
        writeReg(REG_PTR2,regAddr & 0xff);
    }else{
        devErrLog("cpld generic i2c only support 8/16 regAddr");
    }
    //write devAddr and read
    writeReg(REG_DEVADDR,(devAddr<<1)|0x1);
    //go
    uint8 go  = 1;
    go = (sizeof(AddrType) == 1)?go:(go|(1 << 2));
    go = (sizeof(ValueType) == 1)?go:(go|(1 << 1));
    writeReg(REG_CTRL, go);
    //check done and return;
    if (checkI2cDone()){
        if(sizeof(ValueType) == 1){
            ret = readReg(REG_RDATA1);
        }else if(sizeof(ValueType) == 2){
            ret = (readReg(REG_RDATA2) << 8) | readReg(REG_RDATA1);
        }else{
            devErrLog("cpld generic i2c only support 8/16 Value");
            ret = 0;
        }
    }
    else{
        devErrLog("cpld generic i2c trasfor not done");
        ret = 0;
    }
    return ret;    
}

template<typename AddrType,typename ValueType>
void CpldGenericI2cBus<AddrType,ValueType>::i2cWrite(uint8 devAddr, AddrType regAddr, ValueType value)
{
    //write regAddr
    if(sizeof(AddrType) == 1){
        writeReg(REG_PTR1,regAddr & 0xff);
    }else if(sizeof(regAddr) == 2){
        writeReg(REG_PTR1,regAddr >> 8);
        writeReg(REG_PTR2,regAddr & 0xff);
    }else{
        devErrLog("cpld generic i2c only support 8/16 regAddr");
    }
    //write devAddr and read
    writeReg(REG_DEVADDR,(devAddr<<1)|0x0);
    //write value
    if(sizeof(ValueType) == 1){
        writeReg(REG_WDATA1,value & 0xff);
    }else if(sizeof(ValueType) == 2){
        writeReg(REG_WDATA1,value >> 8);
        writeReg(REG_WDATA2,value & 0xff);
    }else{
        devErrLog("cpld generic i2c only support 8/16 value");
    }
    uint8 go  = 1;
    go = (sizeof(AddrType) == 1)?go:(go|(1 << 2));
    go = (sizeof(ValueType) == 1)?go:(go|(1 << 1));
    writeReg(REG_CTRL, go);
    //check done and return;
    checkI2cDone();
}

template class CpldGenericI2cBus<uint8,uint8>;
template class CpldGenericI2cBus<uint16,uint8>;
template class CpldGenericI2cBus<uint8,uint16>;


void CpldOpenI2cBus::startTransfer(uint8 value, bool read)
{   
    //enable core
    writeReg(REG_CTRL, 0x80);
    //write value and set read|write
    uint8 tmp = read? (value << 1 |1): (value << 1);
    writeReg(REG_TXDATA, tmp);
    //set go, read|write, 
    tmp = read?(1<<5):(1<<4);
    tmp |= (1<<7);
    writeReg(REG_CMD, tmp);
    checkI2cDone();
    //disable core
    writeReg(REG_CTRL, 0x00);

}

bool CpldOpenI2cBus::checkI2cDone()
{
    using namespace std::chrono_literals;
    uint8 status;
    int i = 0;
    std::this_thread::sleep_for(200ns);

    for(i = 0; i < 100; i++)
    {
        status = readReg(REG_STAT);
        if (status & 0x02) break;
        std::this_thread::sleep_for(10ns);
    }
    if(i == 100)
    {
        devWarnLog("cpld open i2c tranfer timeout");
        //stop i2c tranfer
        writeReg(REG_CMD, 0x40);
        return false;
    }
    if(status & 0x80)
    {
        devWarnLog("cpld I2C NACK");
        writeReg(REG_CMD, 0x40);
        return false;
    }

    return true;  
}


template<size_t N>
void CpldOpenI2cBus::transfer(std::array<uint8, N> dataOut, std::array<uint8, N> dataIn,bool read)
{
    std::array<uint8, N> readRet;
    //enable core
    writeReg(REG_CTRL, 0x80);
    //set go, read|write, 
    uint8 tmp = read?(1<<5):(1<<4);
    for(size_t i = 0 ; i < N; i++)
    {
        tmp = (i == (N - 1))? tmp|(1<<6):tmp;
        if(read)
        {  
            writeReg(REG_CMD, tmp);
            if(checkI2cDone())
                dataIn[i] = readReg(REG_RXDATA);
            else
                devWarnLog("i2c open read error status = {:x}",readReg(REG_STAT));
        }else{
            writeReg(REG_TXDATA, dataOut[i]);
            writeReg(REG_CMD, tmp);
            if(!checkI2cDone())
                devWarnLog("i2c open write error status = {:x}",readReg(REG_STAT));
        }   
    }
    //disable core
    writeReg(REG_CTRL, 0x00);
}

template void CpldOpenI2cBus::transfer(std::array<uint8, 5> dataOut, std::array<uint8, 5> dataIn,bool read);
template void CpldOpenI2cBus::transfer(std::array<uint8, 3> dataOut, std::array<uint8, 3> dataIn,bool read);
template void CpldOpenI2cBus::transfer(std::array<uint8, 1> dataOut, std::array<uint8, 1> dataIn,bool read);