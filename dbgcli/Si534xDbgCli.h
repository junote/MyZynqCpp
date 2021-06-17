#pragma once
#include <string>
#include <iomanip>
#include "cli/cli.h"
#include "types.h"

#include "BaseDbgCli.h"
#include "Si534x.h"


class Si534xDbgCli:public BaseDevCli<uint8,uint8>
{

public:
    Si534xDbgCli(shared_dev_addr8_value8_ptr dev, std::string devName):dev(dev),devName(devName),
                                    BaseDevCli<uint8,uint8>(dev,devName)
    {}
    ~Si534xDbgCli(){}

private:
    shared_dev_addr8_value8_ptr dev;
    std::string devName;
};


#if 0
class Si534xDbgCli
{

public:
    Si534xDbgCli(std::shared_ptr<Si534x> dev, std::string devName):dev(dev),devName(devName)
    {
        rootMenu->Insert(
            (devName + ".read"),{"regAddr"},
            [&](std::ostream& out,uint16 regAddr){
                    readOne(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (devName + ".read"),{"regAddr len"},
            [&](std::ostream& out,uint16 regAddr, int len){
                    readMore(out,regAddr,len);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (devName + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint16 regAddr, uint8 value){
                writeOne(out, regAddr, value);
            },
            "write regs"
        );         
    }
    ~Si534xDbgCli(){}
    void readOne(std::ostream& out,uint16 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(4) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(2) << unsigned(dev->read(regAddr)) << "\n";       
    }

    void readMore(std::ostream& out, uint16 regAddr, int len){
        for(int i = 0; i < len; i++){
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(4) <<  unsigned(regAddr + i) <<"]:0x" \
                     << std::setfill('0') << std::setw(2) << unsigned(dev->read(uint16(regAddr + i ))) << "\n";
        }
    }
    
    void writeOne(std::ostream& out,uint16 regAddr, uint8 value){
        dev->write(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(4) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(2) << unsigned(value) << "\n";        
    }

private:
    std::shared_ptr<Si534x> dev;
    std::string devName;
};
#endif
