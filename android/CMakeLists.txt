cmake_minimum_required(VERSION 3.10)
project(GrandmaModeDND)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(grandma_dnd_native SHARED
    src/main/cpp/dnd_manager.cpp
    src/main/cpp/native_interface.cpp
)

target_include_directories(grandma_dnd_native PUBLIC
    src/main/cpp/include
)
