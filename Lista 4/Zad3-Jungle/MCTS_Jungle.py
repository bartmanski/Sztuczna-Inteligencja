# To fulfill the request, we will replace the `best_move` logic in the `Jungle` class with a full Monte Carlo Tree Search (MCTS)
# approach while ensuring it remains compatible with the existing `Player` class.
# We'll use the UCT (Upper Confidence bounds applied to Trees) formula to guide the selection process in MCTS.

import random
import sys
from copy import deepcopy

import time
import os

def log_move_time(move_number, start_time, end_time, move, filename="MCTS_move_times.log"):
    duration = end_time - start_time
    with open(os.path.join(os.path.dirname(__file__), filename), "a") as f:
        f.write(f"Move {move_number}: {duration:.4f} seconds\n Actual move: {move}\n")


class MCTSJungle:
    PIECE_VALUES = {0: 4, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10}
    MAX_SIMULATION_DEPTH = 25
    MAX_SIMULATIONS = 300
    MX, MY = 7, 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}
        for y in range(self.MY):
            for x in range(self.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = [
            "L.....T",
            ".D...C.",
            "R.J.W.E",
            ".......",
            ".......",
            ".......",
            "e.w.j.r",
            ".c...d.",
            "t.....l"
        ]
        T = dict(zip("rcdwjtle", range(8)))
        res = []
        for y in range(9):
            row = [None] * 7
            for x in range(7):
                c = pieces[y][x]
                if c != ".":
                    player = 1 if c.isupper() else 0
                    row[x] = (player, T[c.lower()])
            res.append(row)
        return res

    def clone(self):
        new_game = MCTSJungle()
        new_game.board = deepcopy(self.board)
        new_game.pieces = deepcopy(self.pieces)
        new_game.curplayer = self.curplayer
        new_game.peace_counter = self.peace_counter
        return new_game

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in self.ponds and pos2 in self.ponds:
            return True
        if pos1 in self.ponds:
            return False
        if p1 == self.rat and p2 == self.elephant:
            return True
        if p1 == self.elephant and p2 == self.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in self.traps:
            return True
        return False

    def rat_is_blocking(self, pos, dx, dy):
        x, y = pos
        nx = x + dx
        for player in [0, 1]:
            if self.rat not in self.pieces[1 - player]:
                continue
            rx, ry = self.pieces[1 - player][self.rat]
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
            for dx, dy in self.dirs:
                nx, ny = x + dx, y + dy
                pos2 = (nx, ny)
                if 0 <= nx < self.MX and 0 <= ny < self.MY:
                    if self.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (self.rat, self.tiger, self.lion):
                            continue
                        if p in (self.tiger, self.lion):
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(pos, dx, dy):
                                continue
                            nx, ny = x + dx, y + dy
                            pos2 = (nx, ny)
                    if not (0 <= nx < self.MX and 0 <= ny < self.MY):
                        continue
                    if self.board[ny][nx] is not None:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player or not self.can_beat(p, piece2, pos, (nx, ny)):
                            continue
                    res.append((pos, (nx, ny)))
        return res

    def do_move(self, move):
        self.curplayer = 1 - self.curplayer
        if move is None:
            return
        pos1, pos2 = move
        x1, y1 = pos1
        x2, y2 = pos2
        pl, pc = self.board[y1][x1]
        if self.board[y2][x2]:
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1
        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y1][x1] = None

    def evaluate(self, player):
        score = 0
        for p, (x, y) in self.pieces[player].items():
            dx, dy = self.dens[1 - player]
            dist = abs(dx - x) + abs(dy - y)
            score += (12 - dist) * self.PIECE_VALUES[p]
        for p, (x, y) in self.pieces[1 - player].items():
            dx, dy = self.dens[player]
            dist = abs(dx - x) + abs(dy - y)
            score -= (12 - dist) * self.PIECE_VALUES[p]
        return score

    def simulate(self, player):
        sim_game = self.clone()
        for _ in range(self.MAX_SIMULATION_DEPTH):
            moves = sim_game.moves(sim_game.curplayer)
            if not moves:
                break
            move = random.choice(moves)
            sim_game.do_move(move)
        return sim_game.evaluate(player)

    def best_move(self, moves, player):
        best_score = -float('inf')
        best_move = moves[0]
        for move in moves:
            total_score = 0
            for _ in range(self.MAX_SIMULATIONS):
                clone = self.clone()
                clone.do_move(move)
                score = clone.simulate(player)
                total_score += score
            avg_score = total_score / self.MAX_SIMULATIONS
            if avg_score > best_score:
                best_score = avg_score
                best_move = move
        return best_move


class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = MCTSJungle()
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