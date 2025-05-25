import random
import sys
import time
import os
from copy import deepcopy

INFINITY = 99999

def log_move_time(move_number, start_time, end_time,move, filename="Alpha_move_times.log"):
    duration = end_time - start_time
    with open(os.path.join(os.path.dirname(__file__), filename), "a") as f:
        f.write(f"Move {move_number}: {duration:.4f} seconds\n Actual move: {move}\n")

class Jungle:
    PIECE_VALUES = {0: 4, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10}
    MAXIMAL_PASSIVE = 100
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}
        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """
        B = [x.strip() for x in pieces.split() if len(x) > 0]
        T = dict(zip("rcdwjtle", range(8)))
        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != ".":
                    if "A" <= c <= "Z":
                        player = 1
                    else:
                        player = 0
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True
        if pos1 in Jungle.ponds:
            return False
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def rat_is_blocking(self, player_unused, pos, dx, dy):
        x, y = pos
        nx = x + dx
        for player in [0, 1]:
            if Jungle.rat not in self.pieces[1 - player]:
                continue
            rx, ry = self.pieces[1 - player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0 and x == rx:
                return True
            if dx != 0 and y == ry and abs(x - rx) <= 2 and abs(nx - rx) <= 2:
                return True
        return False

    def moves(self, player):
        res = []
        for p, pos in self.pieces[player].items():
            x, y = pos
            for dx, dy in Jungle.dirs:
                pos2 = (nx, ny) = (x + dx, y + dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        if p == Jungle.tiger or p == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x + dx, y + dy)
                    if self.board[ny][nx]:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player:
                            continue
                        if not self.can_beat(p, piece2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    def do_move(self, m):
        self.curplayer = 1 - self.curplayer
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]
        x2, y2 = pos2
        if self.board[y2][x2]:
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1
        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None

    def victory(self, player):
        oponent = 1 - player
        if len(self.pieces[oponent]) == 0:
            self.winner = player
            return True
        x, y = self.dens[oponent]
        if self.board[y][x]:
            self.winner = player
            return True
        if self.peace_counter >= Jungle.MAXIMAL_PASSIVE:
            self.winner = player
            return True
        return False

    def update(self, player, move_string):
        assert player == self.curplayer
        move = tuple(int(m) for m in move_string.split())
        if len(move) != 4:
            raise "WrongMove"
        possible_moves = self.moves(player)
        if not possible_moves:
            if move != (-1, -1, -1, -1):
                raise "WrongMove"
            move = None
        else:
            move = ((move[0], move[1]), (move[2], move[3]))
            if move not in possible_moves:
                raise "WrongMove"
        self.do_move(move)
        if self.victory(player):
            assert self.winner is not None
            return 2 * self.winner - 1
        else:
            return None

    def best_move(self, moves, player):
        depth_limit = 4
        best_score = -INFINITY
        best_move = None
        for move in moves:
            saved = deepcopy((self.board, self.pieces, self.peace_counter, self.curplayer))
            self.do_move(move)
            score = self.alpha_beta(depth_limit - 1, -INFINITY, INFINITY, False, player)
            self.board, self.pieces, self.peace_counter, self.curplayer = saved
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def alpha_beta(self, depth, alpha, beta, maximizing, root_player):
        if depth == 0 or self.victory(0) or self.victory(1):
            return self.evaluate_position(root_player)
        current_player = self.curplayer
        moves = self.moves(current_player)
        if not moves:
            return self.evaluate_position(root_player)
        if maximizing:
            max_eval = -INFINITY
            for move in moves:
                saved = deepcopy((self.board, self.pieces, self.peace_counter, self.curplayer))
                self.do_move(move)
                eval = self.alpha_beta(depth - 1, alpha, beta, False, root_player)
                self.board, self.pieces, self.peace_counter, self.curplayer = saved
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = INFINITY
            for move in moves:
                saved = deepcopy((self.board, self.pieces, self.peace_counter, self.curplayer))
                self.do_move(move)
                eval = self.alpha_beta(depth - 1, alpha, beta, True, root_player)
                self.board, self.pieces, self.peace_counter, self.curplayer = saved
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_position(self, player):
        opponent = 1 - player
        score = 0

        for p, pos in self.pieces[player].items():
            dx, dy = self.dens[opponent]
            dist = abs(dx - pos[0]) + abs(dy - pos[1])
            score += (12 - dist) * Jungle.PIECE_VALUES[p]
            score += Jungle.PIECE_VALUES[p] * 10

            x, y = pos
            if 2 <= x <= 4 and 2 <= y <= 6:
                score += 2  # center control
            if player == 0:
                score += y  # advanced bonus
            else:
                score += (8 - y)

            for trap in Jungle.traps:
                if abs(pos[0] - trap[0]) + abs(pos[1] - trap[1]) <= 1:
                    score += 3

        for p, pos in self.pieces[opponent].items():
            dx, dy = self.dens[player]
            dist = abs(dx - pos[0]) + abs(dy - pos[1])
            score -= (12 - dist) * Jungle.PIECE_VALUES[p]
            score -= Jungle.PIECE_VALUES[p] * 10

            x, y = pos
            if 2 <= x <= 4 and 2 <= y <= 6:
                score -= 2
            if opponent == 0:
                score -= y
            else:
                score -= (8 - y)

            for trap in Jungle.traps:
                if abs(pos[0] - trap[0]) + abs(pos[1] - trap[1]) <= 1:
                    score -= 3

        for p1, pos1 in self.pieces[player].items():
            for p2, pos2 in self.pieces[opponent].items():
                dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
                if dist == 1 and not self.can_beat(p1, p2, pos1, pos2):
                    score -= 5

        return score



class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Jungle()
        self.my_player = 1
        self.say("RDY")

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        move_number = 0
        while True:
            cmd, args = self.hear()
            if cmd == "HEDID":
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1, -1, -1):
                    move = None
                else:
                    xs, ys, xd, yd = move
                    move = ((xs, ys), (xd, yd))

                self.game.do_move(move)
            elif cmd == "ONEMORE":
                move_number = 0
                self.reset()
                continue
            elif cmd == "BYE":
                break
            else:
                assert cmd == "UGO"
                # assert not self.game.move_list
                self.my_player = 0

            start = time.time()
            moves = self.game.moves(self.my_player)
            if moves:
                # move = random.choice(moves)
                move = self.game.best_move(moves, self.my_player)
                self.game.do_move(move)
                move = (move[0][0], move[0][1], move[1][0], move[1][1])
            else:
                self.game.do_move(None)
                move = (-1, -1, -1, -1)
            self.say("IDO %d %d %d %d" % move)

            end = time.time()
            log_move_time(move_number, start, end, move)
            move_number += 1


if __name__ == "__main__":
    player = Player()
    player.loop()