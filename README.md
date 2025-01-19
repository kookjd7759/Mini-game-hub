# Mini Game Hub
**Mini Game Hub** is a compact collection of mini-games, featuring 3 game. While most of the games in the hub are well-known game that have been released before, I have personally implemented all the features for each one.

All games in Mini Game Hub efficiently utilize inter-process communication (IPC) to **provide a graphical user interface (GUI)**.
#### Development environment
- Front-end : PyQt5
- Back-end : C++

![main](https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/main.png?raw=true)

The logic for all the games is implemented in C++, while all game windows, including the menu window, are created using Python's PyQt. Communication between the game logic and the windows is handled through a **standard I/O-based communication** method using **pipes**, a form of **inter-process communication (IPC)**.

## Games
### 1. Minesweeper
**Minesweeper** is a classic puzzle game that challenges players to locate hidden mines on a grid. The goal is to clear all non-mine cells without detonating any mines.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/minesweeper.gif?raw=true" width="350" />

Minesweeper in this hub is designed to **guarantee that the first clicked cell and its suㅊrrounding cells are free of mines**. 

It includes three difficulty levels:
 - Beginner : 8x10 grid with 10 mines
 - Intermediate : 14x18 grid with 40 mines
 - Advanced : 20x24 grid with 99 mines

### 2. Tic Tac Toe
**Tic-Tac-Toe** is a two-player game where players take turns placing "X" or "O" on a 3x3 grid. The goal is to get three of the same marks in a row, either horizontally, vertically, or diagonally.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/tic-tac-toe.gif?raw=true" width="350" />

### 2. 2048
**2048** is a logic-based puzzle game where players slide numbered tiles on a 4x4 grid. When tiles with the same number collide, they merge into one tile with a higher number, increasing the score. The goal is to maximize the score before no moves remain.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/2048.gif?raw=true" width="350" />
