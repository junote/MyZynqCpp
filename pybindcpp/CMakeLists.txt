pybind11_add_module(example example.cpp)
#pybind11_add_module(Mmap64 Mmap64.cpp)


pybind11_add_module(Mmap32 SHARED PyMmap32.cpp)
target_link_libraries(Mmap32 PRIVATE hal::hal spdlog::spdlog_header_only )
pybind11_add_module(ZynqSpiDev PyZynqSpiDev.cpp)
target_link_libraries(ZynqSpiDev PRIVATE hal::hal spdlog::spdlog_header_only)

# INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/3rdParty/pmc/pm5990_3.3.12/include/pm5990Drv)
# pybind11_add_module(digi4 SHARED Pm5990.cpp)
# TARGET_LINK_LIBRARIES(digi4 PRIVATE  g4sdk)
# TARGET_LINK_LIBRARIES(digi4 PRIVATE  g4sdk-3312)




# pybind11_add_module(fpga SHARED Fpga.cpp)


# INCLUDE_DIRECTORIES(
#     ${CMAKE_SOURCE_DIR}/3rdParty/inphi/cs4343/include
#     ${CMAKE_SOURCE_DIR}/3rdParty/inphi/cs4343/platform/include)
# set(CS4343_SRC Cs4343.cpp Fpga.cpp)
# aux_source_directory(${CMAKE_SOURCE_DIR}/3rdParty/inphi/cs4343/src SRC_LIST)
# aux_source_directory(${CMAKE_SOURCE_DIR}/3rdParty/inphi/cs4343/platform/src SRC_LIST)
# pybind11_add_module(cs4343 SHARED ${CS4343_SRC} ${SRC_LIST})
# pybind11_add_module(cs4343 SHARED ${CS4343_SRC})
# TARGET_LINK_LIBRARIES(cs4343 PRIVATE  cs4343sdk)
# TARGET_LINK_LIBRARIES(cs4343 PRIVATE  cs4343sdk-300)



# INCLUDE_DIRECTORIES(
#     ${CMAKE_SOURCE_DIR}/3rdParty/inphi/vega_public_release_1.63.1803/api
#     ${CMAKE_SOURCE_DIR}/3rdParty/inphi/vega_public_release_1.63.1803/api/platform)
# set(VEGA_SRC Vega.cpp Fpga.cpp)
# pybind11_add_module(vega SHARED ${VEGA_SRC})
# TARGET_LINK_LIBRARIES(vega PRIVATE  vegasdk)
# TARGET_LINK_LIBRARIES(vega PRIVATE  vegasdk-1631803)
