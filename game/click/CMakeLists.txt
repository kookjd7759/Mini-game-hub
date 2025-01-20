cmake_minimum_required(VERSION 3.0)
 
project(
    Click
    VERSION 1.0.0 
    DESCRIPTION "Click"
    LANGUAGES CXX 
)
 
set(CMAKE_CXX_STANDARD 20)

add_executable(Click main.cpp)