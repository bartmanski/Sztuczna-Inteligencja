from collections import deque

KING_MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ROOK_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def PosToXY(pos):
    return (ord(pos[0]) - ord('a'), int(pos[1]) - 1)

def InBounds(pos):
    return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

def XYToPos(x, y):
    return chr(x + ord('a')) + str(y + 1)

def IsWhiteKingBetween(WKing, WRook, BKing):
    return (WRook[1]==BKing[1]==WKing[1] and min(BKing[0], WRook[0]) < WKing[0] < max(BKing[0], WRook[0])) or (WRook[0]==BKing[0]==WKing[0] and (min(BKing[1], WRook[1]) < WKing[1] < max(BKing[1], WRook[1])))

def IsKingCheckByRook(WKing,WRook,BKing):
    return (WRook != BKing) and ((WRook[0] == BKing[0] and not IsWhiteKingBetween(WKing, WRook, BKing)) or (WRook[1] == BKing[1] and not IsWhiteKingBetween(WKing, WRook, BKing)))

def IsKingCheck(WKing,WRook,BKing):
    return  ((abs(WKing[0]-BKing[0]) <= 1) and (abs(WKing[1]-BKing[1]) <= 1)) or IsKingCheckByRook(WKing,WRook,BKing)

def IsWinnable(WKing,WRook,BKing,WhoStarts):
    if(WhoStarts =='white'):
        return True
    for move in KING_MOVES:
        new_pos = (BKing[0] + move[0], BKing[1] + move[1])
        if InBounds(new_pos) and not IsKingCheck(WKing, WRook, new_pos):
            return True
    return IsKingCheck(WKing, WRook, BKing)

def GenBlackKingMoves(WKing,WRook,BKing):
    moves = []
    for move in KING_MOVES:
        new_pos = (BKing[0] + move[0], BKing[1] + move[1])
        if InBounds(new_pos) and not IsKingCheck(WKing, WRook, new_pos):
            moves.append(new_pos)
    return moves

def GenWhiteKingMoves(WKing,WRook,BKing):
    moves = []
    for move in KING_MOVES:
        new_pos = (WKing[0] + move[0], WKing[1] + move[1])
        if InBounds(new_pos) and not IsKingCheck(new_pos, WRook, BKing):
            moves.append(new_pos)
    return moves

def GenWhiteRookMoves(WKing,WRook,BKing):
    moves = []
    for move in ROOK_MOVES:
        licznik = 1
        while True:
            new_pos = (WRook[0] +licznik * move[0], WRook[1] + licznik * move[1])
            if InBounds(new_pos):
                if(WRook != BKing and WRook != WKing):
                    moves.append(new_pos)
            else:
                break
            licznik += 1
    return moves

def Pos_BFS(WKing,WRook,BKing,WhoStarts,mode='debug'):
    pos=(WKing,WRook,BKing)
    if not IsWinnable(WKing,WRook,BKing,WhoStarts):
        return 'INF'
    moves_made = []
    visited = dict(pos)
    que = deque()
    que.append((pos, moves_made, WhoStarts))
    while que:
        pos, moves_made, WhoStarts = que.popleft()
        WKing, WRook, BKing = pos
        if WhoStarts == 'white':
            for move in GenWhiteKingMoves(WKing,WRook,BKing):
                new_pos = (move, WRook, BKing)
                if new_pos not in visited:
                    visited[new_pos] = True
                    moves_made1 = moves_made.copy()
                    moves_made1.append('K'+XYToPos(move[0],move[1]))
                    que.append((new_pos,moves_made1, 'black'))
            for move in GenWhiteRookMoves(WKing,WRook,BKing):
                new_pos = (WKing, move, BKing)
                if new_pos not in visited:
                    visited[new_pos] = True
                    moves_made1 = moves_made.copy()
                    moves_made1.append('R'+XYToPos(move[0],move[1]))
                    que.append((new_pos, moves_made1, 'black'))
        else:
            moves = GenBlackKingMoves(WKing,WRook,BKing)
            for move in moves:
                new_pos = (WKing, WRook, move)
                if new_pos not in visited:
                    visited[new_pos] = True
                    moves_made1 = moves_made.copy()
                    moves_made1.append('K'+XYToPos(move[0],move[1]))
                    que.append((new_pos, moves_made1, 'white'))
            if(moves == []):
                print(moves_made)
                break
        if(len(moves_made) > 10):
            break
    if(mode=='debug'):
        print(moves_made, len(moves_made))
    if(mode=='input'):
        print(len(moves_made))

data = input()
WhoMoves,WKing,WRook,BKing = data.split()
WKing = PosToXY(WKing)
WRook = PosToXY(WRook)
BKing = PosToXY(BKing)

Pos_BFS(WKing,WRook,BKing,WhoMoves,mode='debug')


