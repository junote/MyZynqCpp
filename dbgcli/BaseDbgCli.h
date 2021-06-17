#pragma once
#include <string>
#include <iomanip>
#include "cli/cli.h"
#include "types.h"

#include "BaseClass.h"
#include "spdlog/fmt/bin_to_hex.h"
std::unique_ptr<cli::Menu> rootMenu = std::make_unique<cli::Menu>("CLI");


template<typename AddrType,typename ValueType>
class BaseDevCli
{
public:
    BaseDevCli(std::shared_ptr<BaseDev<AddrType,ValueType>> dev,std::string baseMenu):dev(dev),baseMenu(baseMenu){

        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,AddrType regAddr){
                readOne(out,regAddr);
            },
            "read single regs"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr", "len "},
            [&](std::ostream& out,AddrType regAddr, int len = 1){
                readMore(out,regAddr, len);
            },
            "read mutiRegs"
        );    
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,AddrType regAddr, ValueType value){
                writeOne(out,regAddr,value);
            },
            "write regs value"
        );     
        rootMenu->Insert(
            (baseMenu + ".dump8"),{""},
            [&](std::ostream& out, AddrType start){
                dump8(out, start);
            },
            "write regs value"
        ); 
    }
    ~BaseDevCli()=default;
    void readOne(std::ostream& out,AddrType regAddr){
        uint8 width = sizeof(AddrType)*2;
        out <<  std::hex << "[0x" << std::setfill('0') << std::setw(width) <<  unsigned(regAddr) <<"]:\t0x" \
                << std::setfill('0') << std::setw(width) << unsigned(dev->read(regAddr)) << "\n";       
    }
    void readMore(std::ostream& out, AddrType regAddr, int len){
        uint8 width = sizeof(AddrType)*2;
        uint step = (sizeof(AddrType) == 4)? 4:1;
        for(int i = 0; i < len; i++){
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(width) <<  unsigned(regAddr + i * step) <<"]:\t0x" \
                     << std::setfill('0') << std::setw(width) << unsigned(dev->read(regAddr + i * step)) << "\n";
        }
    } 
    void writeOne(std::ostream& out,AddrType regAddr, ValueType value){
        dev->write(regAddr,value);
        uint8 width = sizeof(AddrType)*2;
        out << "[0x" <<  std::setfill('0') << std::setw(width) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(width) << unsigned(value) << "\n";        
    }   
    void dump8(std::ostream& out, AddrType start){
        std::vector<ValueType> buf(256);
        for(int i = start; i< (start + 256); i++ ){
              buf.push_back(dev->read(start + i));
        }
        devInfoLog("\n{:a}",spdlog::to_hex(std::begin(buf) + 0x100,std::end(buf),16));
    }    
private:
    std::string baseMenu;
    std::shared_ptr<BaseDev<AddrType,ValueType>> dev;
};

template class BaseDevCli<uint8,uint8>;
template class BaseDevCli<uint32,uint32>;

#if 0

class Base32DbgCli
{
public:
    Base32DbgCli(shared_basedev_ptr dev, std::string baseMenu):dev(dev),baseMenu(baseMenu){
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,uint32 regAddr){
                    readOne(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr len"},
            [&](std::ostream& out,uint32 regAddr, int len){
                    readMore(out,regAddr,len);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint32 regAddr, uint32 value){
                writeOne(out, regAddr, value);
            },
            "write regs"
        ); 
    }
    ~Base32DbgCli(){}

    void readOne(std::ostream& out,uint32 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(8) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(8) << unsigned(dev->read(regAddr)) << "\n";       
    }

    void readMore(std::ostream& out, uint32 regAddr, int len){
        for(int i = 0; i < len; i++){
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(8) <<  unsigned(regAddr + i * 4) <<"]:0x" \
                     << std::setfill('0') << std::setw(8) << unsigned(dev->read(regAddr + i * 4)) << "\n";
        }
    }
    
    void writeOne(std::ostream& out,uint32 regAddr, uint32 value){
        dev->write(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(8) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(8) << unsigned(value) << "\n";        
    }

private:
    shared_basedev_ptr dev;
    std::string baseMenu;
};

class Base16DbgCli
{
public:
    Base16DbgCli(shared_basedev_ptr dev, std::string baseMenu):dev(dev),baseMenu(baseMenu){
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,uint16 regAddr){
                    readOne(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr len"},
            [&](std::ostream& out,uint16 regAddr, int len){
                    readMore(out,regAddr,len);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint16 regAddr, uint16 value){
                writeOne(out, regAddr, value);
            },
            "write regs"
        ); 
    }
    ~Base16DbgCli(){}

    void readOne(std::ostream& out,uint16 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(4) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(4) << unsigned(dev->read(regAddr)) << "\n";       
    }

    void readMore(std::ostream& out, uint16 regAddr, int len){
        for(int i = 0; i < len; i++){
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(4) <<  unsigned(regAddr + i) <<"]:0x" \
                     << std::setfill('0') << std::setw(4) << unsigned(dev->read(uint16(regAddr + i ))) << "\n";
        }
    }
    
    void writeOne(std::ostream& out,uint16 regAddr, uint16 value){
        dev->write(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(4) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(4) << unsigned(value) << "\n";        
    }

private:
    shared_basedev_ptr dev;
    std::string baseMenu;
};

class Base8DbgCli
{
public:
    Base8DbgCli(shared_basedev_ptr dev, std::string baseMenu):dev(dev),baseMenu(baseMenu){
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,uint8 regAddr){
                    readOne(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr len"},
            [&](std::ostream& out,uint8 regAddr, int len){
                    readMore(out,regAddr,len);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint8 regAddr, uint8 value){
                writeOne(out, regAddr, value);
            },
            "write regs"
        ); 
    }
    ~Base8DbgCli(){}

    void readOne(std::ostream& out,uint8 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(2) << unsigned(dev->read(regAddr)) << "\n";       
    }

    void readMore(std::ostream& out, uint8 regAddr, int len){
        for(int i = 0; i < len; i++){
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr + i) <<"]:0x" \
                     << std::setfill('0') << std::setw(2) << unsigned(dev->read(uint8(regAddr + i ))) << "\n";
        }
    }
    
    void writeOne(std::ostream& out,uint8 regAddr, uint8 value){
        dev->write(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(2) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(2) << unsigned(value) << "\n";        
    }

private:
    shared_basedev_ptr dev;
    std::string baseMenu;
};






class BaseAddr16Value8DbgCLi
{
public:
    BaseAddr16Value8DbgCLi(shared_BaseAddr16Value8_ptr dev, std::string baseMenu):dev(dev),baseMenu(baseMenu){
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,uint16 regAddr){
                    readOne(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr len"},
            [&](std::ostream& out,uint16 regAddr, int len){
                    readMore(out,regAddr,len);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,uint16 regAddr, uint8 value){
                writeOne(out, regAddr, value);
            },
            "write regs"
        ); 
    }
    ~BaseAddr16Value8DbgCLi(){}

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
    shared_BaseAddr16Value8_ptr dev;
    std::string baseMenu;
};



class PmbusDbgCLi
{
public:
    PmbusDbgCLi(shared_PmbusDev_ptr dev, std::string baseMenu):dev(dev),baseMenu(baseMenu){
        rootMenu->Insert(
            (baseMenu + ".readByte"),{"regAddr"},
            [&](std::ostream& out,uint8 regAddr){
                    readByte(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".readWord"),{"regWord"},
            [&](std::ostream& out,uint8 regAddr){
                    readWord(out,regAddr);
                },
            "read one reg"
        ); 
        rootMenu->Insert(
            (baseMenu + ".writeByte"),{"regAddr", "value"},
            [&](std::ostream& out,uint8 regAddr, uint8 value){
                writeByte(out, regAddr, value);
            },
            "write byte regs"
        ); 
        rootMenu->Insert(
            (baseMenu + ".writeWord"),{"regAddr", "value"},
            [&](std::ostream& out,uint8 regAddr, uint16 value){
                writeWord(out, regAddr, value);
            },
            "write word regs"
        ); 
    }
    ~PmbusDbgCLi(){}

    void readByte(std::ostream& out,uint8 regAddr){
                out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(2) << unsigned(dev->readByte(regAddr)) << "\n";       
    }

    void readWord(std::ostream& out, uint8 regAddr){
        out <<  std::hex << "[0x" << std::setfill('0') << std::setw(2) <<  unsigned(regAddr) <<"]:0x" \
                     << std::setfill('0') << std::setw(4) << unsigned(dev->readWord(uint8(regAddr ))) << "\n";
    }
    
    void writeByte(std::ostream& out,uint8 regAddr, uint8 value){
        dev->writeByte(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(2) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(2) << unsigned(value) << "\n";        
    }
    void writeWord(std::ostream& out,uint8 regAddr, uint16 value){
        dev->writeWord(regAddr,value);
        out << "[0x" <<  std::setfill('0') << std::setw(2) << unsigned(regAddr) <<"]:\t0x" \
            << std::setfill('0') << std::setw(4) << unsigned(value) << "\n";        
    }
private:
    shared_PmbusDev_ptr dev;
    std::string baseMenu;
};
#endif






#if 0
template <typename T>
class BaseDbgCli
{
public:
    BaseDbgCli(std::string baseMenu, int baseBits):baseMenu(baseMenu), baseBits(baseBits){

        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr"},
            [&](std::ostream& out,T regAddr){
            int dataWidth = BaseDbgCli::baseBits/4;
            out <<  std::hex << "[0x" << std::setfill('0') << std::setw(dataWidth) <<  (unsigned)(regAddr) <<"]:\t0x" \
                << std::setfill('0') << std::setw(dataWidth) << (unsigned)(read(regAddr )) << "\n";
            },
            "read single regs"
        ); 
        rootMenu->Insert(
            (baseMenu + ".read"),{"regAddr", "len "},
            [&](std::ostream& out,T regAddr, int len = 1){
                int addStep = (baseBits/32)? 4:1;
                int dataWidth = BaseDbgCli::baseBits/4;
                for(int i = 0; i < len; i++){
                    out <<  std::hex << "[0x" << std::setfill('0') << std::setw(dataWidth) <<  (unsigned)(regAddr + i * addStep) <<"]:\t0x" \
                        << std::setfill('0') << std::setw(dataWidth) << (unsigned)(read(regAddr + i * addStep)) << "\n";
                }
            },
            "read mutiRegs"
        );    
        rootMenu->Insert(
            (baseMenu + ".write"),{"regAddr", "value"},
            [&](std::ostream& out,T regAddr, T value){
                write(regAddr,value);
                int dataWidth = BaseDbgCli::baseBits/4;
                out << "[0x" <<  std::setfill('0') << std::setw(dataWidth) << (unsigned)(regAddr) <<"]:\t0x" \
                    << std::setfill('0') << std::setw(dataWidth) << (unsigned)(value) << "\n";
            },
            "write regs value"
        );     
    }

    virtual T read(T regAddr){return 0;}
    virtual void write(T regAddr, T vaule){}
// private:
    std::string baseMenu;
    int baseBits;
};

#endif

