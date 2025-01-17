import subprocess
import os

MINESWEEPER_PATH = os.getcwd() + '\\Mini-game-hub\\game\\minesweeper\\build\\Debug\\Minesweeper.exe'
TICTACTOE_PATH = os.getcwd() + '\\Mini-game-hub\\game\\tic-tac-toe\\build\\Debug\\Tic-tac-toe.exe'

def send(game, st):
    print(f'connector.SEND {st}')
    game.stdin.write(st + '\n')
    game.stdin.flush()
def read(game, ):
    output = game.stdout.readline()
    print(f'connector.READ {output}')
    return output

def MINESWEEPER_EXE():
    game = subprocess.Popen(
            [MINESWEEPER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    return game

def TICTACTOE_EXE():
    game = subprocess.Popen(
            [TICTACTOE_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    return game
