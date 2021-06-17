cmake_minimum_required(VERSION 3.0)

include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/armhf-local-toolchain.cmake)
# include(arm64-local-toolchain.cmake)
# include(aarch-xilinx-linux.cmake)
project(hal)


find_package(PythonLibs 3 REQUIRED)

set(CUSTOM_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CUSTOM_LIBRARY_OUTPUT_DIRECTORY})


add_subdirectory(3rdParty)
add_subdirectory(cpp)
# add_subdirectory(pybindcpp)
add_subdirectory(dbgcli)

