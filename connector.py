import subprocess
import os

MINESWEEPER_EXE = os.getcwd() + '\\Mini-game-hub\\game\\minesweeper\\build\\Debug\\forest-raven.exe'

game = None

def send(st):
    print(f'connector.SEND {st}')
    game.stdin.write(st + '\n')
    game.stdin.flush()
def read():
    output = game.stdout.readline()
    print(f'connector.READ {output}')
    return output

def START_MINESWEEPER():
    global game
    if game is None or game.poll() is not None:
        game = subprocess.Popen(
            [MINESWEEPER_EXE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

