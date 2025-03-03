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
    print(f'{WRook} and {BKing} are same:{WRook == BKing}')
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

def Pos_BFS(WKing,WRook,BKing,WhoStarts,mode='debug'):
    pos=(WKing,WRook,BKing)
    if not IsWinnable(WKing,WRook,BKing,WhoStarts):
        return 'INF'
    moves_made = 0
    visited = dict(pos)
    

    if(mode=='debug'):
        history = []
        queue = deque([(pos,moves_made,history,WhoStarts)])
        while queue:
            pos,moves_made,history,WhoStarts = queue.popleft()
            if(WhoStarts=='white'):
                pass
            else:
                WKing,WRook,BKing = pos
                IsMateFlag = True
                for move in KING_MOVES:
                    new_bk_pos = (BKing[0] + move[0], BKing[1] + move[1])
                    new_pos = (WKing, WRook, new_bk_pos)
                    print(XYToPos(*WKing),XYToPos(*WRook),XYToPos(*new_bk_pos))
                    if InBounds(new_bk_pos) and not IsKingCheck(WKing, WRook, new_bk_pos):
                        IsMateFlag = False
                        if new_bk_pos in visited:
                            continue
                        visited[new_pos] = moves_made + 1
                        history.append(new_pos)
                        queue.append((new_pos, moves_made + 1,history, 'white'))
                if IsMateFlag:
                    return moves_made,history
    if(mode=='input'):
        queue = deque([(pos,moves_made,WhoStarts)])
        print('miau')
WKing = PosToXY(input())
WRook = PosToXY(input())
BKing = PosToXY(input())

print(Pos_BFS(WKing,WRook,BKing,'black','debug'))



