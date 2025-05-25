class Piece:
    RANKS = {
        'rat': 0, 'cat': 1, 'dog': 2, 'wolf': 3,
        'jaguar': 4, 'tiger': 5, 'lion': 6, 'elephant': 7
    }

    SYMBOLS = {
        0: 'r', 1: 'c', 2: 'd', 3: 'w',
        4: 'j', 5: 't', 6: 'l', 7: 'e'
    }

    VALUES = {
        0: 4, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10
    }

    def __init__(self, player, rank, position):
        self.player = player
        self.rank = rank
        self.position = position

    def symbol(self):
        sym = self.SYMBOLS[self.rank]
        return sym.upper() if self.player == 1 else sym

    def can_capture(self, other, board, traps, ponds):
        pos_att = self.position
        pos_def = other.position

        if pos_att in ponds and pos_def in ponds:
            return self.rank == Piece.RANKS['rat'] and other.rank == Piece.RANKS['rat']

        if pos_att in ponds:
            return False

        if self.rank == Piece.RANKS['rat'] and other.rank == Piece.RANKS['elephant']:
            return True

        if self.rank == Piece.RANKS['elephant'] and other.rank == Piece.RANKS['rat']:
            return False

        if pos_def in traps:
            return True

        return self.rank >= other.rank


class JungleGame:
    WIDTH, HEIGHT = 7, 9
    MAX_PASSIVE_TURNS = 50

    TRAPS = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    PONDS = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    DENS = [(3, 8), (3, 0)]
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self):
        self.pieces = []
        self.current_player = 0
        self.passive_moves = 0
        self.winner = None
        self._initialize_pieces()

    def _initialize_pieces(self):
        layout = [
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
        for y, row in enumerate(layout):
            for x, ch in enumerate(row):
                if ch != '.':
                    player = 1 if ch.isupper() else 0
                    rank = Piece.RANKS[ch.lower()]
                    self.pieces.append(Piece(player, rank, (x, y)))

    def _get_piece_at(self, position):
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def _is_in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT

    def _is_own_den(self, pos, player):
        return pos == self.DENS[player]

    def _rat_blocks_jump(self, player, start_pos, dx, dy):
        opponent = 1 - player
        rat = next((p for p in self.pieces if p.player == opponent and p.rank == Piece.RANKS['rat']), None)
        if not rat or rat.position not in self.PONDS:
            return False
        rx, ry = rat.position
        x, y = start_pos
        if dy == 0 and y == ry and ((x < rx < x + dx) or (x + dx < rx < x)):
            return True
        if dx == 0 and x == rx and ((y < ry < y + dy) or (y + dy < ry < y)):
            return True
        return False

    def _valid_move_positions(self, piece):
        x, y = piece.position
        moves = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            if not self._is_in_bounds(next_pos):
                continue
            if self._is_own_den(next_pos, piece.player):
                continue
            if next_pos in self.PONDS and piece.rank not in (Piece.RANKS['rat'], Piece.RANKS['tiger'], Piece.RANKS['lion']):
                continue
            if piece.rank in (Piece.RANKS['tiger'], Piece.RANKS['lion']) and next_pos in self.PONDS:
                jump_len = 3 if dx != 0 else 4
                if self._rat_blocks_jump(piece.player, piece.position, dx * jump_len, dy * jump_len):
                    continue
                jump_pos = (x + dx * jump_len, y + dy * jump_len)
                if not self._is_in_bounds(jump_pos):
                    continue
                next_pos = jump_pos
            dest_piece = self._get_piece_at(next_pos)
            if dest_piece is None:
                moves.append(next_pos)
            elif dest_piece.player != piece.player and piece.can_capture(dest_piece, self, self.TRAPS, self.PONDS):
                moves.append(next_pos)
        return moves

    def generate_moves(self):
        player_pieces = [p for p in self.pieces if p.player == self.current_player]
        moves = []
        for piece in player_pieces:
            valid_positions = self._valid_move_positions(piece)
            for pos in valid_positions:
                moves.append((piece.position, pos))
        return moves

    def apply_move(self, move):
        if move is None:
            self.current_player = 1 - self.current_player
            return
        start_pos, end_pos = move
        piece = self._get_piece_at(start_pos)
        if not piece or piece.player != self.current_player:
            raise ValueError("Invalid move: no piece to move or not player's piece.")
        target_piece = self._get_piece_at(end_pos)
        if target_piece and target_piece.player == self.current_player:
            raise ValueError("Invalid move: cannot capture own piece.")
        if end_pos not in self._valid_move_positions(piece):
            raise ValueError("Invalid move: move not allowed by rules.")
        if target_piece:
            self.pieces.remove(target_piece)
            self.passive_moves = 0
        else:
            self.passive_moves += 1
        piece.position = end_pos
        self.current_player = 1 - self.current_player

    def check_winner(self):
        opponent = 1 - self.current_player
        if all(p.player != opponent for p in self.pieces):
            self.winner = self.current_player
            return True
        den_pos = self.DENS[opponent]
        den_piece = self._get_piece_at(den_pos)
        if den_piece and den_piece.player == self.current_player:
            self.winner = self.current_player
            return True
        if self.passive_moves >= self.MAX_PASSIVE_TURNS:
            self.winner = None
            return True
        return False

    def play_move(self, player, move_str):
        if player != self.current_player:
            raise ValueError("Not this player's turn")
        parts = move_str.split()
        if len(parts) != 4:
            raise ValueError("Invalid move format")
        coords = tuple(map(int, parts))
        if coords == (-1, -1, -1, -1):
            move = None
        else:
            move = ((coords[0], coords[1]), (coords[2], coords[3]))
        if move is not None and move not in self.generate_moves():
            raise ValueError("Illegal move")
        self.apply_move(move)
        if self.check_winner():
            return 0 if self.winner is None else 2 * self.winner - 1
        return None

    def print_board(self):
        board_repr = [['.' for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        for piece in self.pieces:
            x, y = piece.position
            board_repr[y][x] = piece.symbol()
        for row in board_repr:
            print(''.join(row))
        print()
