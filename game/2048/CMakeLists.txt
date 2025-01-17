cmake_minimum_required(VERSION 3.0)
 
project(
    2048
    VERSION 1.0.0 
    DESCRIPTION "2048"
    LANGUAGES CXX 
)
 
set(CMAKE_CXX_STANDARD 20)

add_executable(2048 main.cpp)