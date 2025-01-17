# Mini Game Hub
**Mini Game Hub** is a compact collection of mini-games, featuring 1 game. While most of the games in the hub are well-known game that have been released before, I have personally implemented all the features for each one.

All games in Mini Game Hub efficiently utilize inter-process communication (IPC) to **provide a graphical user interface (GUI)**.
#### Development environment
- Front-end : PyQt5
- Back-end : C++

The logic for all the games is implemented in C++, while all game windows, including the menu window, are created using Python's PyQt. Communication between the game logic and the windows is handled through a **standard I/O-based communication** method using **pipes**, a form of **inter-process communication (IPC)**.

## Games
### 1. Minesweeper
//TODO