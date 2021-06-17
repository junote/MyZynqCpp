#pragma once
#include <string>
#include <iomanip>
#include "cli/cli.h"
#include "types.h"

#include "BaseClass.h"
#include "BaseDbgCli.h"

#include "spdlog/spdlog.h"
#include "spdlog/fmt/fmt.h"


class Ltc2977DbgCli:public Ltc2977
{

public:
    Ltc2977DbgCli(shared_bus_addr8_value8_ptr devBus8, shared_bus_addr8_value16_ptr devBus16,uint8 devAddr,std::string devName):
                devBus8(devBus8),devBus16(devBus16),devAddr(devAddr),devName(devName),
                Ltc2977(devBus8,devBus16,devAddr)
    {
        rootMenu->Insert(
            (devName + ".readByte"),{"<uint8 regAddr>"},
            [&](std::ostream& out, uint8 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:\t0x" \
                    << std::setfill('0') << std::setw(2) << unsigned(readByte(regAddr)) << "\n";    
                },
            "show one uint8 reg voltage"
        ); 
        rootMenu->Insert(
            (devName + ".readWord"),{"<uint16 regAddr>"},
            [&](std::ostream& out, uint8 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:\t0x" \
                    << std::setfill('0') << std::setw(4) << unsigned(readWord(regAddr)) << "\n";    
                },
            "show one uint16 reg voltage"
        ); 
        rootMenu->Insert(
            (devName + ".writeByte"),{"<uint8 regAddr> <uint8 value>"},
            [&](std::ostream& out, uint8 regAddr, uint8 value){
                writeByte(regAddr,value);
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:\t0x" \
                    << std::setfill('0') << std::setw(2) << unsigned(value) << "\n";    
                },
            "write one uint8 reg uint8 value"
        ); 
        rootMenu->Insert(
            (devName + ".writeWord"),{"<uint8 regAddr> <uint16 value>"},
            [&](std::ostream& out, uint8 regAddr, uint16 value){
                writeWord(regAddr,value);
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(1) <<  unsigned(regAddr) <<"]:\t0x" \
                    << std::setfill('0') << std::setw(4) << unsigned(value) << "\n";    
                },
            "write one uint8 reg uint16 value"
        ); 
        rootMenu->Insert(
            (devName + ".status"),{""},
            [&](std::ostream& out){
                    showStatus(out);

                },
            "show all voltage"
        ); 
    }
    ~Ltc2977DbgCli(){}
    void showStatus(std::ostream& out){
        
        fmt::print("input voltage:{:.2f}V\n",getVolageIn());
        fmt::print("temperature:{:.2f}degC\n",getTemperature());
        for (int i = 0 ;i < 7; i++)
        {
            fmt::print("\tchannel voltage [{:1d}]:{:.2f}V\n",i, getChannelVoltage(i));
        }
    }
private:
    shared_bus_addr8_value8_ptr devBus8;
    shared_bus_addr8_value16_ptr devBus16;
    uint8 devAddr;    
    std::string devName;
};
