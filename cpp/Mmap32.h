#pragma once

#include <string>
#include <cstdint>
#include <mutex>
#include "types.h"
#include "BaseClass.h"


class Mmap32:public BaseBus<uint32,uint32>
{
public:
    explicit Mmap32(std::string devName,
                    uint32 offset,
                    uint32 size);
    virtual ~Mmap32();

    uint32 busRead(uint32 regAddr);
    void busWrite(uint32 regAddr, uint32 value);

private:
    std::string devName;
    uint32 offset;
    uint32 size;
    // std::mutex &myMutex;
    void *mapAddr;
    uint32 baseAddr;
    uint32 loadModulesAndGetBaseAddress(std::string devName, uint32 offset, uint32 size);
};
