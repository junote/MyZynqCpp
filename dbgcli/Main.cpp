#include <iostream>
#include <memory>

#include <cli/cli.h>
#include <cli/clilocalsession.h>
#include <cli/loopscheduler.h>

#include "BaseClass.h"
#include "types.h"
#include "Fpga.h"
#include "Cpld.h"
#include "FpgaDbgCli.h"
#include "CpldDbgCli.h"
#include "Si534x.h"
#include "Si534xDbgCli.h"
#include "Tmp435DbgCli.h"
#include "EpromDbgCli.h"
#include "Ltc2977DbgCli.h"

using namespace cli;
using namespace std;



int main(int argc, char const *argv[])
{
    using namespace std;
    shared_bus_addr8_value8_ptr cpldBus = make_shared<ZynqSpiDev>("spidev0.0");
    shared_dev_addr8_value8_ptr cpld = make_shared<Cpld>(cpldBus);

    shared_bus_addr32_value32_ptr fpgaBus = std::make_shared<Mmap32>("mem",0x43c00000,0x10000);
    shared_dev_addr32_value32_ptr fpga = std::make_shared<Fpga>(fpgaBus);

    shared_bus_addr8_value8_ptr cpldI2cBus_clk = std::make_shared<CpldGenericI2cBus<uint8,uint8>>(cpld,0x70);
    shared_dev_addr8_value8_ptr clk42 = make_shared<Si534x>(cpldI2cBus_clk,0x69);
    shared_dev_addr8_value8_ptr clk45 = make_shared<Si534x>(cpldI2cBus_clk,0x68);

    shared_bus_addr8_value8_ptr cpldI2cBus_tmp435 = std::make_shared<CpldGenericI2cBus<uint8,uint8>>(cpld,0x80);
    std::shared_ptr<Tmp435> tmp435 = make_shared<Tmp435>(cpldI2cBus_tmp435,0x4c);

    shared_bus_addr16_value8_ptr cpldI2cBus_eprom = std::make_shared<CpldGenericI2cBus<uint16,uint8>>(cpld,0x88);
    std::shared_ptr<At24c128> eprom = make_shared<At24c128>(cpldI2cBus_eprom,0x50);
 
    shared_bus_addr8_value8_ptr cpldI2cBus_ltc2977_byte = std::make_shared<CpldGenericI2cBus<uint8,uint8>>(cpld,0x78);
    shared_bus_addr8_value16_ptr cpldI2cBus_ltc2977_word = std::make_shared<CpldGenericI2cBus<uint8,uint16>>(cpld,0x78);
  



    try
    {
        spdlog::set_pattern("\n[%Y-%m-%d] [%H:%M:%S:%f] [%^%l%$] [thread %t] %v");
        spdlog::set_level(spdlog::level::trace);
        CmdHandler colorCmd;
        CmdHandler nocolorCmd;
        SetColor();
        colorCmd.Disable();
        nocolorCmd.Enable();    
        rootMenu->Insert(
            "setLogLevel",
            [](std::ostream& out, uint8 level){spdlog::set_level(spdlog::level::level_enum(level));},
            "setLogLevel"
        );

        FpgaDbgCli fpgaCli(fpga, "fpga");
        CpldDbgCli cpldCli(cpld, "cpld");
        Si534xDbgCli clk42Cli(clk42,"clk42");
        Si534xDbgCli clk45Cli(clk45,"clk45");
        Tmp435DbgCli tmp435Cli(tmp435,"tmp435");
        EpromDbgCli epromCli(eprom,"eprom");
        Ltc2977DbgCli ltc2977Cli(cpldI2cBus_ltc2977_byte,cpldI2cBus_ltc2977_word,0x5c,"ltc2977");



        Cli cli( std::move(rootMenu) );
        // global exit action
        cli.ExitAction( [](auto& out){ out << "Goodbye and thanks.\n"; } );
        LoopScheduler scheduler;
        CliLocalTerminalSession localSession(cli, scheduler,std::cout);
        localSession.ExitAction(
        [&scheduler](auto& out) // session exit action
            {
                out << "Closing App...\n";
                scheduler.Stop();
            }
        );


        scheduler.Run();
    }
    catch (const std::exception& e)
    {
        cerr << "Exception caugth in main: " << e.what() << endl;
    }
    catch (...)
    {
        cerr << "Unknown exception caugth in main." << endl;
    }
    return -1;
}
