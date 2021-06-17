#include <pybind11/pybind11.h>
#include <iostream>

int add(int i, int j) {
    return i + j;
}



struct  Pet1
{
   Pet1(const std::string &name): name(name){}
   void setName(const std::string &name_){ name = name_; }
   const std::string &getName(){return name;}
   
    std::string name;
};


namespace py = pybind11;


int usePython()
{
    py::print("try to use python");
    py::object tryP2C = py::module::import("tryP2C");
    py::object tryPythonAdd = tryP2C.attr("addPython");
    py::print(tryPythonAdd(1,2));
    return py::int_(tryPythonAdd(1,2));
}

class Pet {
public:
    Pet(const std::string &name, const std::string &species)
        : m_name(name), m_species(species) {}
    std::string name() const { return m_name; }
    std::string species() const { return m_species; }
private:
    std::string m_name;
    std::string m_species;
};

class Dog : public Pet {
public:
    Dog(const std::string &name) : Pet(name, "dog") {}
    std::string bark() const { return "Woof!"; }
};

class MyPet
{
private:
    Pet& pet;
public:
    MyPet(Pet& _pet):pet(_pet){}
    std::string myName()const {return pet.name();}
};


PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");

    m.def("usePython", &usePython);


    py::class_<Pet1>(m, "Pet1")
    .def(py::init<const std::string &>())
    .def("setName", &Pet1::setName)
    .def("getName", &Pet1::getName)
    .def("__repr__",
        [](const Pet1 &a)
        {return "simpleExample.Pet named " + a.name;});
    //Exporting variables
    m.attr("num1") = 100;
    py::object world = py::cast("World");
    m.attr("what") = world;

    py::class_<Pet> pet_class(m, "Pet");
    pet_class
        .def(py::init<std::string, std::string>())
        .def("name", &Pet::name)
        .def("species", &Pet::species);

    py::class_<Dog>(m, "Dog", pet_class)
        .def(py::init<std::string>())
        .def("bark", &Dog::bark);

    py::class_<MyPet>(m, "MyPet")
        .def(py::init<Pet&>())
        .def("myName", &MyPet::myName);

}


