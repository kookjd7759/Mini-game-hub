#include <iostream>
#include <random>

using namespace std;

#define Fori(x) for (int i = 0; i < x; ++i)
#define Forj(x) for (int j = 0; j < x; ++j)
#define Fork(x) for (int k = 0; k < x; ++k)

enum Dir {
	UP, DOWN, LEFT, RIGHT
};

class Game {
private:
	int board[4][4], score = 0, emptySize = 16;

	bool isEnd() const {
		if (emptySize) return false;

		Fori(4) Forj(3) if (board[i][j] == board[i][j + 1] || board[j][i] == board[j + 1][i]) return false;

		return true;
	}
	bool isSame(int temp[4][4]) {
		Fori(4) Forj(4) if (temp[i][j] != board[i][j]) return false;
		return true;
	}

	void create() {
		random_device rd; mt19937 gen(rd());
		uniform_int_distribution<> block_dis(1, 10);
		int block = (block_dis(gen) <= 2 ? 4 : 2);
		uniform_int_distribution<> posIdx_dis(1, emptySize);
		int posIdx = posIdx_dis(gen);
		Fori(4) Forj(4) {
			if (board[i][j] == 0) {
				--posIdx;
				if (!posIdx) {
					board[i][j] = block;
					--emptySize;
					return;
				}
			}
		}
	}
	int moveLine(Dir dir, int idx) {
		int dest, sum(0);
		if (dir == LEFT) {
			dest = 0;
			for (int i = 1; i < 4; i++) {
				if (!board[idx][i]) continue;

				if (!board[idx][dest]) board[idx][dest] = board[idx][i];
				else {
					if (board[idx][dest] & board[idx][i]) {
						board[idx][dest] <<= 1;
						sum += board[idx][dest];
						dest++;
						++emptySize;
					}
					else {
						dest++;
						if (dest == i) continue;
						board[idx][dest] = board[idx][i];
					}
				}
				board[idx][i] = 0;
			}
		}
		else if (dir == RIGHT) {
			dest = 3;
			for (int i = 2; i >= 0; i--) {
				if (!board[idx][i]) continue;

				if (!board[idx][dest]) board[idx][dest] = board[idx][i];
				else {
					if (board[idx][dest] & board[idx][i]) {
						board[idx][dest] <<= 1;
						sum += board[idx][dest];
						dest--;
						++emptySize;
					}
					else {
						dest--;
						if (dest == i) continue;
						board[idx][dest] = board[idx][i];
					}
				}
				board[idx][i] = 0;
			}
		}
		else if (dir == UP) {
			dest = 0;
			for (int i = 1; i < 4; i++) {
				if (!board[i][idx]) continue;

				if (!board[dest][idx]) board[dest][idx] = board[i][idx];
				else {
					if (board[dest][idx] & board[i][idx]) {
						board[dest][idx] <<= 1;
						sum += board[dest][idx];
						dest++;
						++emptySize;
					}
					else {
						dest++;
						if (dest == i) continue;
						board[dest][idx] = board[i][idx];
					}
				}
				board[i][idx] = 0;
			}
		}
		else {
			dest = 3;
			for (int i = 2; i >= 0; i--) {
				if (!board[i][idx]) continue;

				if (!board[dest][idx]) board[dest][idx] = board[i][idx];
				else {
					if (board[dest][idx] & board[i][idx]) {
						board[dest][idx] <<= 1;
						sum += board[dest][idx];
						dest--;
						++emptySize;
					}
					else {
						dest--;
						if (dest == i) continue;
						board[dest][idx] = board[i][idx];
					}
				}
				board[i][idx] = 0;
			}
		}
		return sum;
	}
	int move(Dir dir) {
		int sum(0);
		Fori(4) sum += moveLine(dir, i);
		return sum;
	}
	void SEND_score() const { cout << score << "\n"; }
	void SEND_board() const { Fori(4) Forj(4) cout << board[i][j] << ' '; cout << "\n"; }

public:
	Game() {
		memset(board, 0, sizeof(board));
		create(); create();
	}

	void slide(Dir dir) {
		int temp[4][4]; memcpy(temp, board, sizeof(board));
		int gain = move(dir);
		if (isSame(temp)) return;
		score += gain;
		create();
	}
	void play() {
		SEND_board();
		SEND_score();
		cout << "continue\n";
		while (true) {
			int dir; cin >> dir;
			slide((Dir)dir);
			SEND_board();
			SEND_score();
			if (isEnd()) {
				cout << "end\n";
				break;
			}
			else cout << "continue\n";
		}
	}
};

int main() {
	Game game;
	game.play();
}