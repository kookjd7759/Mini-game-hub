# Mini Game Hub
**Mini Game Hub** is a compact collection of mini-games, featuring 1 game. While most of the games in the hub are well-known game that have been released before, I have personally implemented all the features for each one.

All games in Mini Game Hub efficiently utilize inter-process communication (IPC) to **provide a graphical user interface (GUI)**.
#### Development environment
- Front-end : PyQt5
- Back-end : C++

![main](images/main.png)

The logic for all the games is implemented in C++, while all game windows, including the menu window, are created using Python's PyQt. Communication between the game logic and the windows is handled through a **standard I/O-based communication** method using **pipes**, a form of **inter-process communication (IPC)**.

## Games
### 1. Minesweeper
**Minesweeper** is a classic puzzle game that challenges players to locate hidden mines on a grid. The goal is to clear all non-mine cells without detonating any mines.

![minesweeper](https://github.com/user-attachments/assets/399ad977-b83c-4473-b637-af0df8133b59)

Minesweeper in this hub is designed to **guarantee that the first clicked cell and its surrounding cells are free of mines**. 

It includes three difficulty levels:
 - Beginner : 8x10 grid with 10 mines
 - Intermediate : 14x18 grid with 40 mines
 - Advanced : 20x24 grid with 99 mines
