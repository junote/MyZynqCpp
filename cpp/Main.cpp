// #include "Cpld.h"
// #include "Fpga.h"
// #include "Si534x.h"
// #include "Tmp435.h"
// #include "At24c128.h"
#include <iostream>
#include "Cs4343.h"


int main(int argc, char const *argv[])
{
    using namespace std;
    // shared_bus_addr8_value8_ptr cpldBus = make_shared<ZynqSpiDev>("spidev0.0");
    // shared_dev_addr8_value8_ptr cpld = make_shared<Cpld>(cpldBus);

    // shared_bus_addr32_value32_ptr fpgaBus = std::make_shared<Mmap32>("mem",0x43c00000,0x10000);
    // shared_dev_addr32_value32_ptr fpga = std::make_shared<Fpga>(fpgaBus);

    // shared_bus_addr8_value8_ptr cpldI2cBus_clk = std::make_shared<CpldGenericI2cBus<uint8,uint8>>(cpld,0x70);
    // Si534x clk45(cpldI2cBus_clk,0x68);
    // Si534x clk42(cpldI2cBus_clk,0x69);
    // cout << hex << unsigned(clk42.read(2)) << endl;
    // cout << hex << unsigned(clk45.read(2)) << endl;
    // clk42.write(1,1);
    // cout << hex << unsigned(clk42.read(1)) << endl;
    // clk42.write(1,0);
    // cout << hex << unsigned(clk42.read(1)) << endl;

    // shared_bus_addr8_value8_ptr cpldI2cBus_tpm435 = std::make_shared<CpldGenericI2cBus<uint8,uint8>>(cpld,0x80);
    // Tmp435 tmp435(cpldI2cBus_tpm435,0x4c);
    // cout << hex << unsigned(tmp435.read(0)) <<endl;
    // cout << hex << unsigned(tmp435.read(1)) <<endl;
    // cout << hex << unsigned(tmp435.read(3)) <<endl;
    // cout << hex << unsigned(tmp435.read(0xa)) <<endl;

    // cout << hex << unsigned(tmp435.read(0x10)) <<endl;
    // cout << hex << unsigned(tmp435.read(0x15)) <<endl;
    // cout << tmp435.getLocalTemperature() << endl;

    // shared_bus_addr16_value8_ptr cpldI2cBus_eprom = std::make_shared<CpldGenericI2cBus<uint16,uint8>>(cpld,0x88);
    // At24c128 eprom(cpldI2cBus_eprom,0x50);
    
    // shared_bus_addr8_value8_ptr cpldBus_cs4343 = std::make_shared<ZynqSpiDev>("spidev0.0");
    // cpld_cs4343 = std::make_shared<Cpld>(cpldBus_cs4343);
    // uint8 edcReset = cpld_cs4343->read(0x20);
    // cpld_cs4343->write(0x20,edcReset|0x7);



    return 0;
}
