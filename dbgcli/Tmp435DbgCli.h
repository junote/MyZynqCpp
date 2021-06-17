#pragma once
#include <string>
#include <iomanip>
#include <memory>

#include "BaseDbgCli.h"
#include "Tmp435.h"


class Tmp435DbgCli:public BaseDevCli<uint8,uint8>
{
public:
    Tmp435DbgCli(std::shared_ptr<Tmp435> dev, std::string devName):dev(dev),devName(devName),
        BaseDevCli<uint8,uint8>(std::dynamic_pointer_cast<BaseDev<uint8,uint8>>(dev),devName)
    {
        rootMenu->Insert(
            (devName + ".status"),{""},
            [&](std::ostream& out){
                    showStatus(out);
                },
            "show all voltage"
        );         
    }
    ~Tmp435DbgCli(){}
    void showStatus(std::ostream& out){
        using spdlog::memory_buf_t;
        memory_buf_t buf;
        fmt::format_to(buf,"local temperature:{:.2f}degC\n",dev->getLocalTemperature());
        // out << fmt::to_string(buf);
        fmt::format_to(buf,"remote temperature:{:.2f}degC\n",dev->getRemoteTemperature());
        out << fmt::to_string(buf);
    }
private:
    std::shared_ptr<Tmp435> dev;
    std::string devName;
};