
add_executable(cli Main.cpp)
target_compile_definitions(cli PRIVATE CLI_EXAMPLES_USE_LOOP_SCHEDULER)
target_link_libraries(cli PUBLIC cli::cli hal::hal spdlog::spdlog_header_only)
