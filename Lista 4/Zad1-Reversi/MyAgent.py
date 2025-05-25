import random
import sys


class Reversi:
    M = 8
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    DEPTH = 4
    CORNER = 16
    BAD_CORNER = -6
    ROUND = 0
    BC2 = [
        ((0, 7), (1, 7)),
        ((0, 7), (0, 6)),
        ((0, 0), (1, 0)),
        ((0, 0), (0, 1)),
        ((7, 0), (7, 1)),
        ((7, 0), (6, 0)),
        ((7, 7), (6, 7)),
        ((7, 7), (7, 6)),
    ]

    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    INFINITY = 999999

    def __init__(self):
        self.board = self.initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i][j] is None:
                    self.fields.add((j, i))

    def initial_board(self):
        B = [[None] * self.M for _ in range(self.M)]
        B[3][3] = 1
        B[4][4] = 1
        B[3][4] = 0
        B[4][3] = 0
        return B

    def draw(self):
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = self.board[i][j]
                if b is None:
                    res.append(".")
                elif b == 1:
                    res.append("#")
                else:
                    res.append("o")
            print("".join(res))
        print("")

    def moves(self, player):
        res = []
        for x, y in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in self.DIRS):
                res.append((x, y))
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < self.M and 0 <= y < self.M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for nx, ny in to_beat:
                    self.board[ny][nx] = player

    def result(self, player):
        res = 0
        for y in range(self.M):
            for x in range(self.M):
                b = self.board[y][x]
                if b == 1 - player:
                    res -= 1
                elif b == player:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None  # noqa: E711

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def undo_last_move(self):
        last_move = self.move_list[-1]
        self.board = self.history[-1]
        del self.move_list[-1]
        del self.history[-1]
        if last_move is not None:
            self.fields.add(last_move)

    def shallow(self,move):
        self.do_move(move)
        if self.terminal(): return self.result()
        self.undo_last_move(move)

    def alpha_beta(self, maximizingPlayer, alpha, beta, my_player, depth):
        if self.terminal():
            return self.result(my_player)

        if depth == Reversi.DEPTH:
            return self.score(my_player)

        if maximizingPlayer:
            value = -Reversi.INFINITY
            # moves =  self.moves(my_player)
            # if Reversi.ROUND < 10 :
            #     moves = sorted(moves,key=self.shallow)
            for move in self.moves(my_player):
                self.do_move(move, my_player)
                value = max(
                    value, self.alpha_beta(False, alpha, beta, my_player, depth + 1)
                )
                self.undo_last_move()
                if value and value >= beta:
                    return value
                alpha = max(alpha, value)
        else:
            value = Reversi.INFINITY
            for move in self.moves(1 - my_player):
                self.do_move(move, 1 - my_player)
                value = min(
                    value, self.alpha_beta(True, alpha, beta, my_player, depth + 1)
                )
                self.undo_last_move()
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value

    def best_move(self, player):
        Reversi.ROUND += 1
        ms = self.moves(player)
        best = (-Reversi.INFINITY - 1, None)
        if ms:
            if len(ms) == 1:
                return ms[0]
            for move in ms:
                self.do_move(move, player)
                score = self.alpha_beta(
                    False, -Reversi.INFINITY, Reversi.INFINITY, player, 0
                )
                self.undo_last_move()
                if score > best[0]:
                    best = (score, move)
            return best[1]
        return None

    def in_corner(self, player):
        count = 0
        for corner_x, corner_y in [(0, 7), (0, 0), (7, 0), (7, 7)]:
            if self.board[corner_y][corner_x] == player:
                count += 1
        return count

    def borders(self, player):
        ret = 0
        for i in range(1, 7):
            if self.board[0][i] == player and (
                self.board[0][0] == player or self.board[0][7] == player
            ):
                ret += 1
            elif self.board[7][i] == player and (
                self.board[7][0] == player or self.board[7][7] == player
            ):
                ret += 1
            elif self.board[i][0] == player and (
                self.board[0][0] == player or self.board[7][0] == player
            ):
                ret += 1
            elif self.board[i][7] == player and (
                self.board[0][7] == player or self.board[7][7] == player
            ):
                ret += 1
            # elif self.board[i][0] == player and self.board[i][6] is None: ret+=1
        return ret

    def bad_corner(self, player):
        count = 0
        for corner, opposite_corner in [
            ((0, 7), (1, 6)),
            ((0, 0), (1, 1)),
            ((7, 0), (6, 1)),
            ((7, 7), (6, 6)),
        ] + self.BC2:
            corner_x, corner_y = corner
            opposite_x, opposite_y = opposite_corner
            if (
                self.board[opposite_x][opposite_y] == player
                and self.board[corner_y][corner_x] is None
            ):
                count += 1
        return count

    def score(self, player):
        result = self.result(player)
        result = 0
        result -= self.CORNER * self.in_corner(1 - player)
        result += self.CORNER * self.in_corner(player)
        result -= self.BAD_CORNER * self.bad_corner(1 - player)
        result += self.BAD_CORNER * self.bad_corner(player)
        # result += 0.5* self.borders(player)
        # result -= 0.5*self.borders(1-player)
        # if result < 0 :
        # result += len(self.moves(player))
        # if(Reversi.ROUND > -1):
        result += len(self.moves(player))
        result -= len(self.moves(1 - player))
        return result


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Reversi()
        self.my_player = 1
        self.say("RDY")

    def say(self, message):
        sys.stdout.write(message)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def hear(self):
        message = sys.stdin.readline().split()
        return message[0], message[1:]

    def loop(self):
        while True:
            command, args = self.hear()
            if command == "ONEMORE":
                self.reset()
                continue
            elif command == "BYE":
                break
            elif command == "UGO":
                self.my_player = 0
            elif command == "HEDID":
                move = tuple(int(arg) for arg in args[2:])
                if move == (-1, -1):
                    move = None
                self.game.do_move(move, 1 - self.my_player)
            else:
                continue

            move = self.game.best_move(self.my_player)
            self.game.do_move(move, self.my_player)

            if move is None:
                move = (-1, -1)
            self.say("IDO %d %d" % move)


if __name__ == "__main__":
    write = open("err.txt", "w")
    player = Player()
    player.loop()

    # else: file.write("%d,%d\n"%move)
