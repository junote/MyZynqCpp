#pragma once

#include <string>
#include <mutex>
#include "types.h"
#include "BaseClass.h"

class ZynqSpiDev:public BaseBus<uint8,uint8>
{
    public:
        explicit ZynqSpiDev(std::string devName);
        virtual ~ZynqSpiDev();

        void transfer(uint8 *tx, uint8 *rx, size_t len);
        uint8 busRead(uint8 regAddr);
        void busWrite(uint8 regAddr,uint8 value);
    
    private:
        std::string devName;
        // std::mutex myMutex;
        int devFd;
        uint32 mode = 0;
        uint16 delay = 10;
        uint32 speed = 20000000;
        uint8 bits = 8;
};


