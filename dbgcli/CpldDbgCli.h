#pragma once
#include <string>
#include "Cpld.h"
#include "BaseDbgCli.h"
#include "types.h"
#include "BaseClass.h"




class CpldDbgCli:BaseDevCli<uint8,uint8>
{

public:
    CpldDbgCli(shared_dev_addr8_value8_ptr dev, std::string devName):dev(dev),devName(devName),BaseDevCli<uint8,uint8>(dev,devName)
    {}
    ~CpldDbgCli(){}

private:
    shared_dev_addr8_value8_ptr dev;
    std::string devName;
};


#if 0
class CpldDbgCli:public Cpld
{
public:
    CpldDbgCli(BaseBus* devBus):devBus(devBus),
                        Cpld(devBus)
    {
        rootMenu->Insert(
            (devName + ".read"),{"regAddr", "len"},
            [&](std::ostream& out,uint32 regAddr, int len = 1){
                int addStep = (baseBits/32)? 4:1;
                
                for(int i = 0; i < len; i++){
                    out <<  std::hex << "[0x" << std::setfill('0') << std::setw(baseBits/4) <<  unsigned(regAddr + i * addStep) <<"]:0x" \
                     << std::setfill('0') << std::setw(baseBits/4) << unsigned(read(regAddr + i * addStep)) << "\n";
                }
            },
            "read regs"
        );    
        rootMenu->Insert(
            (devName + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint32 regAddr, uint32 value){
                write(regAddr,value);
                out << "[0x" <<  std::setfill('0') << std::setw(baseBits/4) << unsigned(regAddr) <<"]:\t0x" \
                << std::setfill('0') << std::setw(baseBits/4) << unsigned(value) << "\n";
            },
            "write regs"
        );                   
    }
    ~CpldDbgCli(){}
private:
    BaseBus* devBus;
    std::string devName = "cpld";
    int baseBits = 8;
};
#endif