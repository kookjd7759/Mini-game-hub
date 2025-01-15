cmake_minimum_required(VERSION 3.0)
 
project(
    Minesweeper
    VERSION 1.0.0 
    DESCRIPTION "Minesweeper"
    LANGUAGES CXX 
)
 
set(CMAKE_CXX_STANDARD 20)

add_executable(Minesweeper main.cpp)