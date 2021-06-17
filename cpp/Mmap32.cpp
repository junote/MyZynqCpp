#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

#include <fstream>
#include <string>

#include "Mmap32.h"
#include <mutex>

// #include <pybind11/pybind11.h>

using std::string;

Mmap32::Mmap32(std::string devName,
               uint32 offset,
               uint32 size)
    : devName(devName),
      offset(offset),
      size(size),
      baseAddr(loadModulesAndGetBaseAddress(devName, offset, size)),
      BaseBus<uint32,uint32>()
{
}
Mmap32::~Mmap32()
{
    munmap(mapAddr, size);
}
uint32 Mmap32::loadModulesAndGetBaseAddress(string devName, uint32 offset, uint32 size)
{
    uint32 theBaseAddress;
    // Need to load the  Kernel module before mapping against it.
    bool koLoaded = false;
    string line;
    string myDevName = "/dev/" + devName;

    int fd = open(myDevName.c_str(), O_RDWR);

    assert(fd > 0);

    // void *mapAddr;
    mapAddr = mmap(NULL,                   // requested address to map to
                   size,                   // size of range to map
                   PROT_READ | PROT_WRITE, // set both read and write permissions
                   MAP_SHARED,             // changes to range are shared
                   fd,                     // file descriptor for this device
                   offset);

    // The device can close now
    close(fd);

    assert(mapAddr != MAP_FAILED);
    theBaseAddress = reinterpret_cast<uint32>(mapAddr);
    printf("Mmap32 driver initialized: Virtual Base Addr = 0x%08X, Size = 0x%08X\n", theBaseAddress, size);
    return theBaseAddress;
}


uint32 Mmap32::busRead(uint32 offset)
{
    // uint32 data = *reinterpret_cast<const volatile uint32 *>(((char *))mapAddr + offset);
    uint32 data = *(reinterpret_cast<uint32 *>((char *)mapAddr + offset));
    // uint32 data = *reinterpret_cast<const volatile uint32 *>(baseAddr + offset);
    // (reinterpret_cast<uint32>(baseAddr) + reinterpret_cast<uint32>(offset));

    return data;
}

void Mmap32::busWrite(uint32 offset, uint32 value)
{
    // *reinterpret_cast<volatile uint32 *>((char *)mapAddr + offset) = value;
    *reinterpret_cast<uint32 *>((char *)mapAddr + offset) = value;
    // *reinterpret_cast<volatile uint32 *>(baseAddr + offset) = value;

    // (reinterpret_cast<uint32>(baseAddr) + reinterpret_cast<uint32>(offset)) = value;
}

// namespace py = pybind11;

// PYBIND11_MODULE(Mmap32, m)
// {
//     py::class_<Mmap32>(m, "Mmap32")
//         .def(py::init<std::string &, uint32 &, uint32 &>())
//         .def("read32", &Mmap32::read32)
//         .def("write32", &Mmap32::write32);
// }
