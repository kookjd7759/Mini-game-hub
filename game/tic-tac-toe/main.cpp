#include <iostream>

using namespace std;

#define Fori(x) for (int i = 0; i < x; ++i)
#define Forj(x) for (int j = 0; j < x; ++j)

enum Cell : int {
    NONE, O, X
};
static inline Cell operator~(Cell& c) { return (c == O ? X : O); }

enum Gameover_info : int {
    DRAW, WIN_O, WIN_X, COUNTINUE
};
string gameOver_st[4]{ "draw", "win_O", "win_X", "continue" };

class Game {
private:
    Cell board[3][3], turn;
    bool isOver = false;

    bool isOk(int x, int y) const { return (0 <= x && x < 3 && 0 <= y && y < 3); }
    Gameover_info isEnd() const {
        Fori(3) {
            if (NONE != board[i][0] && board[i][0] == board[i][1] && board[i][1] == board[i][2]) return (Gameover_info)board[i][0];
            if (NONE != board[0][i] && board[0][i] == board[1][i] && board[1][i] == board[2][i]) return (Gameover_info)board[0][i];
        }
        if (NONE != board[0][0] && board[0][0] == board[1][1] && board[1][1] == board[2][2]) return (Gameover_info)board[0][0];
        if (NONE != board[2][0] && board[2][0] == board[1][1] && board[1][1] == board[0][2]) return (Gameover_info)board[2][0];

        Fori(3) Forj(3) if (board[i][j] == NONE) return COUNTINUE;

        return DRAW;
    }

    void click(int x, int y) {
        if (isOver || !isOk(x, y) || board[x][y] != NONE) return;

        board[x][y] = turn;
        turn = ~turn;
    }
    void SEND_board() const { cout << turn; Fori(3) Forj(3) cout << board[i][j]; cout << "\n"; }
    void SEND_result(Gameover_info gameOver) const { cout << gameOver_st[gameOver] << "\n"; }
public:
    Game() {
        memset(board, NONE, sizeof(board));
        turn = O;
    }

    void play() {
        while (true) {
            int x, y; cin >> x >> y;
            click(x, y);
            SEND_board();
            Gameover_info gameOver(isEnd());
            SEND_result(gameOver);

            if (gameOver != COUNTINUE) break;
        }
    }
};


int main() {
    Game game;
    game.play();
}
