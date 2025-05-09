# <img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/main_icon.png?raw=true" width="30" /> Mini Game Hub
**Mini Game Hub** is a compact collection of mini-games, featuring 5 game. While most of the games in the hub are well-known game that have been released before, I have personally implemented all the features for each one.

All games in Mini Game Hub efficiently utilize inter-process communication (IPC) to **provide a graphical user interface (GUI)**.
#### Development environment
- Front-end : python-PyQt5
- Core Logic / Engine : C++

![main](https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/main.png?raw=true)

The logic for all the games is implemented in C++, while all game windows, including the menu window, are created using Python's PyQt. Communication between the game logic and the windows is handled through a **standard I/O-based communication** method using **pipes**, a form of **inter-process communication (IPC)**.

## Games
The games are implemented to be playable using both the **keyboard** and the **mouse**.

---

### 1. Minesweeper
**Minesweeper** is a classic puzzle game that challenges players to locate hidden mines on a grid. The goal is to clear all non-mine cells without detonating any mines.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/minesweeper.gif?raw=true" width="350" />

Minesweeper in this hub is designed to **guarantee that the first clicked cell and its surrounding cells are free of mines**. 

It includes three difficulty levels:
 - Beginner : 8x10 grid with 10 mines
 - Intermediate : 14x18 grid with 40 mines
 - Advanced : 20x24 grid with 99 mines

---

### 2. Tic Tac Toe
**Tic-Tac-Toe** is a two-player game where players take turns placing "X" or "O" on a 3x3 grid. The goal is to get three of the same marks in a row, either horizontally, vertically, or diagonally.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/tic-tac-toe.gif?raw=true" width="350" />

---

### 3. 2048
**2048** is a logic-based puzzle game where players slide numbered tiles on a 4x4 grid. When tiles with the same number collide, they merge into one tile with a higher number, increasing the score. The goal is to maximize the score before no moves remain.

When sliding, a new tile with a value of either 2 or 4 is generated in an empty spot, with the following probabilities:
 - 2 : 80%
 - 4 : 20%

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/2048.gif?raw=true" width="350" />

This game is implemented to be played using the **keyboard**, where the **four arrow keys are used to specify the direction of sliding**.

---

### 4. Memory
**Memory** is a memory game where blocks light up in a sequence, and players must click the corresponding blocks. As the game progresses, the sequence becomes longer and more challenging. The goal is to match the most blocks and achieve the highest score.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/memory.gif?raw=true" width="350" />

The game ends if three blocks are clicked incorrectly in a single level. The levels are structured as follows: :
 - level 1 : 3x3 grid with 3 blocks
 - level 2 : 4x4 grid with 5 blocks
 - level 3 : 5x5 grid with 8 blocks
 - level 4 : 6x6 grid with 12 blocks
 - level 5 : 7x7 grid with 17 blocks
 - level 6 : 8x8 grid with 23 blocks
 - level 7 : 9x9 grid with 30 blocks
 - level 8 : 10x10 grid with 38 blocks
 
 Each level is played three times, and with each round, one additional block is added to the sequence that must be matched.

---

### 5. Click !
**Click !** is a reaction time test game where the goal is to quickly turn the button back to "off" when it changes to the "on" state. It offers options for 3, 5, or 10 attempts, and measures the average reaction time for each attempt. The game ends immediately if the button is clicked when it is not in the "off" state, requiring fast and precise responses.

<img src="https://github.com/kookjd7759/Mini-game-hub/blob/main/image/screenShot/click.gif?raw=true" width="350" />

---
