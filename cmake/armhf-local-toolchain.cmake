set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR armhf)

SET(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabihf-g++-8)
SET(CMAKE_C_COMPILER /usr/bin/arm-linux-gnueabihf-gcc-8)

set(CMAKE_CXX_STANDARD 14)

#add_definitions(-fPIC -DZ_LINUX  -DLINUX_COMPILE)

# for warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pthread")
# The line below should replace the above one once all projects have no warnings.
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function") # allow unused functions for now
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-missing-field-initializers") # disable warning - g++ is overly paranoid
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-parameter") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-reorder") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-sign-compare") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-but-set-variable")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-type-limits ") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-function") # allow unused functions for now
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-missing-field-initializers") # disable warning - g++ is overly paranoid
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-ignored-qualifiers")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-write-strings")

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wstringop-truncation")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wformat-truncation")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wcast-function-type")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wstrict-aliasing")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wimplicit-fallthrough")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wextra")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wformat")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fpermissive")


set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-implicit-function-declaration")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-pointer-to-int-cast")
# warnings


# pybind11# Disable pybind11 python search mechanism
set(PYTHON_MODULE_EXTENSION ".so" CACHE INTERNAL "Cross python lib extension")
set(PYTHONLIBS_FOUND TRUE CACHE INTERNAL "") 




