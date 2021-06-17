#pragma once
#include <string>
#include "Fpga.h"
#include "BaseDbgCli.h"
#include "types.h"
#include "BaseClass.h"

#include "stdio.h"


class FpgaDbgCli:BaseDevCli<uint32,uint32>
{

public:
    FpgaDbgCli(shared_dev_addr32_value32_ptr dev, std::string devName):dev(dev),devName(devName),BaseDevCli<uint32,uint32>(dev,devName)
    {}
    ~FpgaDbgCli(){}

private:
    shared_dev_addr32_value32_ptr  dev;
    std::string devName;
};

#if 0
class FpgaDbgCli:public Fpga
{
public:
    FpgaDbgCli(BaseBus* devBus):devBus(devBus),
                        Fpga(devBus)
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
    ~FpgaDbgCli(){}
    // uint32 read(uint32 regAddr){return devBus->read32(regAddr);}
    // void write(uint32 regAddr, uint32 value){devBus->write32(regAddr,value);}
private:
    BaseBus* devBus;
    std::string devName = "fpga";
    int baseBits = 32;
};
#endif