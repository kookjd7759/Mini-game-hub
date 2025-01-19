#include <iostream>
#include <random>
#include <set>

using namespace std;

#define Fori(x) for (int i = 0; i < x; ++i)
#define Forj(x) for (int j = 0; j < x; ++j)

enum Cell {
    MASK, CORRECT, FAIL
};

class Game {
private:
    const int size[9]{ 0, 3, 4, 5, 6, 7, 8, 9, 10 };
    const int cnt[9]{ 0, 3, 5, 8, 12, 17, 23, 30, 38 };
    bool** data;
    Cell** board;
    int level = 1, score = 0, level_cnt = 0, correct_cnt = 0, fail_cnt = 0;

    inline bool isOk(int x, int y) const { return (0 <= x && x < size[level] && 0 <= y && y < size[level]); }
    inline bool isEnd() const { return fail_cnt == 3; }

    void create_board(int size) {
        data = new bool* [size];
        board = new Cell * [size];

        Fori(size) data[i] = new bool[size], board[i] = new Cell[size];
        Fori(size) Forj(size) data[i][j] = false, board[i][j] = MASK;
    }
    void setBoard() {
        random_device rd; mt19937 gen(rd());
        uniform_int_distribution<> dis(0, size[level] * size[level] - 1);
        set<int> pos;
        while (pos.size() < cnt[level] + level_cnt) {
            int new_pos(dis(gen));
            if (pos.count(new_pos)) continue;
            pos.insert(new_pos);
        }

        for (const int posIdx : pos) data[posIdx / size[level]][posIdx % size[level]] = true;
    }
    void level_up() {
        Fori(size[level]) delete[] data[i], delete[] board[i];
        delete[] data; delete[] board;

        correct_cnt = 0, fail_cnt = 0;
        ++level_cnt;
        if (level < 8 && level_cnt == 3) ++level, level_cnt = 0;
        create_board(size[level]);
        setBoard();
    }
    void SEND_data(){ Fori(size[level]) Forj(size[level]) cout << (int)data[i][j]; cout << "\n"; }
    void SEND_info() {
        cout << score << "\n";
        Fori(size[level]) Forj(size[level]) cout << board[i][j]; cout << "\n";
    }

public:
    Game() {
        create_board(size[level]);
        setBoard();
    }

    void click(int x, int y) {
        if (!isOk(x, y) || board[x][y] != MASK) return;

        board[x][y] = (data[x][y] ? CORRECT : FAIL);
        data[x][y] ? ++correct_cnt : ++fail_cnt;
    }

    void play() {
        while (true) {
            if (!correct_cnt && !fail_cnt) {
                cout << "new\n";
                SEND_data();
            }
            else cout << "old\n";

            int x, y; cin >> x >> y;
            click(x, y);
            SEND_info();

            if (isEnd()) {
                cout << "end\n";
                break;
            }
            else cout << "continue\n";

            if (correct_cnt == (cnt[level] + level_cnt)) {
                cout << "clear\n";
                level_up();
            }
            else cout << "continue\n";
        }
    }
};

int main() {
    Game game;
    game.play();
}