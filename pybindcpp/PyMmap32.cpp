
#include <pybind11/pybind11.h>
#include "Mmap32.h"

namespace py = pybind11;

PYBIND11_MODULE(Mmap32, m)
{
    py::class_<Mmap32>(m, "Mmap32")
        .def(py::init<std::string &, uint32 &, uint32 &>())
        .def("read32", &Mmap32::read32)
        .def("write32", &Mmap32::write32);
}