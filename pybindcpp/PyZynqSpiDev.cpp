#include <pybind11/pybind11.h>
#include "ZynqSpiDev.h"

namespace py = pybind11;

PYBIND11_MODULE(ZynqSpiDev, m)
{
    py::class_<ZynqSpiDev>(m, "ZynqSpiDev")
        .def(py::init<std::string>())
        .def("read8", &ZynqSpiDev::read8)
        .def("write8", &ZynqSpiDev::write8);
}
