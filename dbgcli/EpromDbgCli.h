#pragma once
#include <string>
#include <iomanip>
#include <memory>

#include "BaseDbgCli.h"
#include "At24c128.h"


class EpromDbgCli:public BaseDevCli<uint16,uint8>
{
public:
    EpromDbgCli(std::shared_ptr<At24c128> dev, std::string devName):dev(dev),devName(devName),
        BaseDevCli<uint16,uint8>(std::dynamic_pointer_cast<BaseDev<uint16,uint8>>(dev),devName)
    {}
    ~EpromDbgCli(){}

private:
    std::shared_ptr<At24c128> dev;
    std::string devName;
};