#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <linux/types.h>
#include <linux/spi/spidev.h>

#include <mutex>
#include <string>

#include <stdio.h>
// #include <pybind11/pybind11.h>

#include "ZynqSpiDev.h"
#include "types.h"

using std::string;

ZynqSpiDev::ZynqSpiDev(std::string devName):devName(devName),BaseBus<uint8,uint8>()
{
    int ret;

    string myDevName = "/dev/" + devName;
    devFd = open(myDevName.c_str(),O_RDWR);
    if(devFd < 0 )
    {
        printf("can't open spi dev");
        return;
    }

    //spi mode
	ret = ioctl(devFd, SPI_IOC_WR_MODE32, &mode);
	if (ret == -1)
		printf("can't set spi mode");

	ret = ioctl(devFd, SPI_IOC_RD_MODE32, &mode);
	if (ret == -1)
		printf("can't get spi mode");

    //bit per word
	ret = ioctl(devFd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if (ret == -1)
		printf("can't set bits per word");

	ret = ioctl(devFd, SPI_IOC_RD_BITS_PER_WORD, &bits);
	if (ret == -1)
		printf("can't get bits per word");

	//max speed
	ret = ioctl(devFd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
	if (ret == -1)
		printf("can't set max speed hz");

	ret = ioctl(devFd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
	if (ret == -1)
		printf("can't get max speed hz");

	printf("spi mode: 0x%x\n", mode);
	printf("bits per word: %d\n", bits);
	printf("max speed: %d Hz (%d KHz)\n", speed, speed/1000);

}

ZynqSpiDev::~ZynqSpiDev()
{
    close(devFd);
}

void ZynqSpiDev::transfer(uint8 *tx, uint8 *rx, size_t len)
{
    int ret;
    struct spi_ioc_transfer tr = {
		.tx_buf = (unsigned long)tx,
		.rx_buf = (unsigned long)rx,
		.len = len,
		.speed_hz = speed,
		.delay_usecs = delay,
		.bits_per_word = bits,
	};
	ret = ioctl(devFd, SPI_IOC_MESSAGE(1), &tr);
	if (ret < 1)
		printf("can't send spi message\n");
    
    // printf("tx:");
    // for(int i = 0; i < len; ++i){
    //     printf("%02x\t",*tx++);
    // }
    // printf("\n");
    // printf("rx:");
    // for(int i = 0; i < len; ++i){
    //     printf("%02x\t",*rx++);
    // }
    // printf("\n");

}

uint8 ZynqSpiDev::busRead(uint8 regAddr)
{
    uint8 dout[5],din[5];
    dout[0] = 0;
    dout[1] = (regAddr & 0xff00) >> 8 ;
    dout[2] = regAddr & 0xff;
    dout[3] = 0;
    dout[4] = 0;

    transfer(dout,din,5);

    return din[4];

}

void ZynqSpiDev::busWrite(uint8 regAddr, uint8 value)
{
    uint8 dout[5],din[5];
    dout[0] = 1;
    dout[1] = (regAddr & 0xff00) >> 8 ;
    dout[2] = regAddr & 0xff;
    dout[3] = value;
    dout[4] = 0;

    transfer(dout,din,5);
}

// namespace py = pybind11;

// PYBIND11_MODULE(ZynqSpiDev, m)
// {
//     py::class_<ZynqSpiDev>(m, "ZynqSpiDev")
//         .def(py::init<std::string>())
//         .def("read8", &ZynqSpiDev::read8)
//         .def("write8", &ZynqSpiDev::write8);
// }
