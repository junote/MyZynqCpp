#pragma once

#include <stdint.h>
#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"

typedef int8_t sint8;
typedef uint8_t uint8;

typedef int16_t sint16;
typedef uint16_t uint16;

typedef int32_t sint32;
typedef uint32_t uint32;

typedef int64_t sint64;
typedef uint64_t uint64;

typedef float float32;
typedef double float64;

#define devTraceLog(...) spdlog::trace(__VA_ARGS__)
#define devDebugLog(...) spdlog::debug(__VA_ARGS__)
#define devInfoLog(...) spdlog::info(__VA_ARGS__)
#define devWarnLog(...) spdlog::warn(__VA_ARGS__)
#define devErrLog(...) spdlog::error(__VA_ARGS__)
#define devCritLog(...) spdlog::critical(__VA_ARGS__)

// spdlog::set_pattern("[%H:%M:%S %z] [%^%L%$] [thread %t] %v");
// spdlog::set_level(spdlog::level::SPDLOG_LEVEL_ERROR);
