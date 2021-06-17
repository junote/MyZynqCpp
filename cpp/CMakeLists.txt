
file(GLOB sources ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)
file(GLOB headers ${CMAKE_CURRENT_SOURCE_DIR}/*.h)

add_library(hal ${sources} ${headers})
add_library(hal::hal ALIAS hal)
target_include_directories(hal PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(hal PUBLIC spdlog::spdlog_header_only cs4343sdk)
target_compile_options(hal PUBLIC -fPIC)


add_executable(halmain ${sources} ${headers})
target_link_libraries(halmain PUBLIC spdlog::spdlog_header_only cs4343sdk)






