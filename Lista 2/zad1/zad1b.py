import random

MX = 16
LM = 100

n, m = 0, 0
cel_row = [[] for _ in range(MX)]
cel_col = [[] for _ in range(MX)]
cur_row = [[] for _ in range(MX)]
cur_col = [[] for _ in range(MX)]
sum_cel_row = [0] * MX
sum_cel_col = [0] * MX
sum_cur_row = [0] * MX
sum_cur_col = [0] * MX
board = [[0] * MX for _ in range(MX)]

# Count continuous blocks of 1s in a row
def count_blocks_row(i):
    vec = []
    length = 0
    for j in range(m):
        if board[i][j] == 1:
            length += 1
        else:
            if length > 0:
                vec.append(length)
            length = 0
    if length > 0:
        vec.append(length)
    return vec

# Count continuous blocks of 1s in a column
def count_blocks_col(j):
    vec = []
    length = 0
    for i in range(n):
        if board[i][j] == 1:
            length += 1
        else:
            if length > 0:
                vec.append(length)
            length = 0
    if length > 0:
        vec.append(length)
    return vec

# Count sum of 1s in a row
def count_sum_row(i):
    return sum(board[i][:m])

# Count sum of 1s in a column
def count_sum_col(j):
    return sum(board[i][j] for i in range(n))

# Check if two lists are identical
def same(a, b):
    return a == b

# Get all rows/columns that don’t match the target
def bad():
    pos = []
    for i in range(n):
        if not same(cel_row[i], cur_row[i]):
            pos.append(i)
    for j in range(m):
        if not same(cel_col[j], cur_col[j]):
            pos.append(j + n)
    return pos

# Check how many numbers match between two lists (sorted)
def zgadza(a, b):
    return len(set(a) & set(b))

def eval(i, j):
    board[i][j] ^= 1 
    b_r = count_blocks_row(i)
    b_c = count_blocks_col(j)
    s_r = count_sum_row(i)
    s_c = count_sum_col(j)
    res = 0
    board[i][j] ^= 1

    if abs(len(b_r) - len(cel_row[i])) < abs(len(cur_row[i]) - len(cel_row[i])):
        res += 1
    if abs(len(b_c) - len(cel_col[j])) < abs(len(cur_col[j]) - len(cel_col[j])):
        res += 1
    if abs(s_r - sum_cel_row[i]) < abs(sum_cur_row[i] - sum_cel_row[i]):
        res += 1
    if abs(s_c - sum_cel_col[j]) < abs(sum_cur_col[j] - sum_cel_col[j]):
        res += 1
    if zgadza(b_r, cel_row[i]) > zgadza(cur_row[i], cel_row[i]):
        res += 1
    if zgadza(b_c, cel_col[j]) > zgadza(cur_col[j], cel_col[j]):
        res += 1

    return res

games = 0
changes = 0

def dawaj():
    global changes, games

    for i in range(n):
        for j in range(m):
            board[i][j] = random.randint(0, 1)

    for i in range(n):
        sum_cur_row[i] = count_sum_row(i)
        cur_row[i] = count_blocks_row(i)

    for j in range(m):
        sum_cur_col[j] = count_sum_col(j)
        cur_col[j] = count_blocks_col(j)

    limit = n * m * 30

    while bad() and limit > 0:
        limit -= 1
        changes += 1

        pos = bad()
        random.shuffle(pos)

        ind = pos[0]
        best = float('-inf')
        candidates = []

        if ind < n:  # Row
            for col in range(m):
                e = eval(ind, col)
                if e > best:
                    candidates = [(ind, col)]
                    best = e
                elif e == best:
                    candidates.append((ind, col))
        else:  # Column
            for row in range(n):
                e = eval(row, ind - n)
                if e > best:
                    candidates = [(row, ind - n)]
                    best = e
                elif e == best:
                    candidates.append((row, ind - n))

        random.shuffle(candidates)
        R, C = candidates[0]

        board[R][C] ^= 1

        sum_cur_col[C] = count_sum_col(C)
        sum_cur_row[R] = count_sum_row(R)
        cur_row[R] = count_blocks_row(R)
        cur_col[C] = count_blocks_col(C)

    games += 1
    return not bad()

def main():
    global n, m, cel_row, cel_col, sum_cel_row, sum_cel_col

    with open("zad_input.txt", "r") as test, open("zad_output.txt", "w") as OUT:
        while True:
            line = test.readline().strip()
            if not line:
                break

            n, m = map(int, line.split())

            cel_row = [[] for _ in range(n)]
            cel_col = [[] for _ in range(m)]
            sum_cel_row = [0] * n
            sum_cel_col = [0] * m

            # Read row constraints
            for i in range(n):
                row_data = list(map(int, test.readline().strip().split()))
                cel_row[i] = row_data
                sum_cel_row[i] = sum(row_data)

            # Read column constraints
            for j in range(m):
                col_data = list(map(int, test.readline().strip().split()))
                cel_col[j] = col_data
                sum_cel_col[j] = sum(col_data)

            # Solve puzzle
            while True:
                if dawaj():
                    for i in range(n):
                        OUT.write("".join('#' if board[i][j] else '.' for j in range(m)) + '\n')
                    break

if __name__ == "__main__":
    main()
