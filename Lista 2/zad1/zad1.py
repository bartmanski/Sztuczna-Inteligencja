import numpy as np
import copy as cp
import subprocess
'''
def update_row_sum(row_sum, j, new_value):
    if(new_value == 0):
        for index,(start,size) in enumerate(row_sum):
            if (start > j):
                continue
            if (start + size > j and start < j):
                row_sum.pop(index)
                row_sum.append((start, j-start))
                if start + size - j-1 != 0:
                    row_sum.append((j+1, start + size - j - 1))
                row_sum.sort()
                return
            if (start + size == j):
                if(size == 1):
                    row_sum.pop(index)
                    row_sum.sort()
                    return
                row_sum[index] = (start, size - 1)
                row_sum.sort()
                return
            if start == j:
                if(size == 1):
                    row_sum.pop(index)
                    row_sum.sort() 
                    return
                row_sum[index] = (start + 1, size - 1)
                row_sum.sort()
                return
    else:
        for index,(start,size) in enumerate(row_sum):
            if (start == j + 1):
                row_sum[index] = (j, size + 1)
                return
            if (start > j):
                continue
            if (start + size == j):
                if (index != len(row_sum)-1 and row_sum[index+1][0] == j+1):
                    row_sum[index] = (start, size + row_sum[index+1][1] + 1)
                    row_sum.pop(index+1)
                    row_sum.sort()
                    return
                row_sum[index] = (start, size + 1)
                row_sum.sort() 
                return
            

        row_sum.append((j, 1))
        row_sum.sort()

def update_col_sum(col_sum, i, new_value):
    if(new_value == 0):
        for index,(start,size) in enumerate(col_sum):
            if (start > i):
                continue
            if (start + size > i and start < i):
                col_sum.pop(index)
                col_sum.append((start, i-start))
                if start + size - i-1 != 0:
                    col_sum.append((i+1, start + size - i - 1))
                col_sum.sort()
                return
            if (start + size == i):
                if(size == 1):
                    col_sum.pop(index)
                    col_sum.sort()
                    return
                col_sum[index] = (start, size - 1)
                col_sum.sort()
                return
            if start == i:
                if(size == 1):
                    col_sum.pop(index)
                    col_sum.sort() 
                    return
                col_sum[index] = (start + 1, size - 1)
                col_sum.sort()
                return
    else:
        for index,(start,size) in enumerate(col_sum):
            if (start == i + 1):
                col_sum[index] = (i, size + 1)
                return
            if (start > i):
                continue
            if (start + size == i):
                if (index != len(col_sum)-1 and col_sum[index+1][0] == i+1):
                    col_sum[index] = (start, size + col_sum[index+1][1] + 1)
                    col_sum.pop(index+1)
                    col_sum.sort()
                    return
                col_sum[index] = (start, size + 1)
                col_sum.sort() 
                return
            

        col_sum.append((i, 1))
        col_sum.sort()

def check_row(row_spec, row_sum):
    how_wrong = 0
    i = 0
    j = 0

    while i < len(row_spec) and j < len(row_sum):
        how_wrong += abs(row_spec[i] - row_sum[j][1])
        i += 1
        j += 1
    
    while i < len(row_spec):
        how_wrong += row_spec[i]
        i += 1

    while j < len(row_sum):
        how_wrong += row_sum[j][1]
        j += 1

    return how_wrong

def check_col(col_spec, col_sum):
    how_wrong = 0
    i = 0
    j = 0

    while i < len(col_spec) and j < len(col_sum):
        how_wrong += abs(col_spec[i] - col_sum[j][1])
        i += 1
        j += 1
    
    while i < len(col_spec):
        how_wrong += col_spec[i]
        i += 1

    while j < len(col_sum):
        how_wrong += col_sum[j][1]
        j += 1

    return how_wrong

def check_board(board, row_spec, col_spec, row_sums, col_sums):
    how_wrong = 0
    for i in range(len(board)):
        how_wrong += check_row(row_spec[i], row_sums[i])
    for j in range(len(board[0])):
        how_wrong += check_col(col_spec[j], col_sums[j])
    return how_wrong
#'''



def parse_board(board):
    n , m = board.shape
    return '\n'.join([''.join(['#' if board[i][j] == 1 else '.' for j in range(m)]) for i in range(n)])

def parse_input():
    file = open('zad_input.txt', 'r')
    lines = file.readlines()
    
    how_many_rows,how_many_cols = lines[0].split()
    how_many_rows = int(how_many_rows)
    how_many_cols = int(how_many_cols)
    board = np.zeros((int(how_many_rows), int(how_many_cols)))  
    num_ones = np.random.randint(1, how_many_rows * how_many_cols)  # Random number of ones
    for _ in range(num_ones):
        x = np.random.randint(0, how_many_rows)
        y = np.random.randint(0, how_many_cols)
        board[x][y] = 1
    row_specyfication = []
    col_specyfication = []
    for i in range(1, len(lines)):
        lines[i] = lines[i].strip()
        spec = lines[i].split()
        spec = [int(x) for x in spec]
        if(i < how_many_rows+1):
            row_specyfication.append(spec)
        else:
            col_specyfication.append(spec)

    return board, row_specyfication, col_specyfication

def opt_dist(line,line_spec):

    def opt_dist_one_block(start,line,block_size):
        how_wrong = 0
        for i in range(start, start + block_size):
            
            if(i >= len(line)):
                return float('inf')
            #print(line[i])
            if(line[i] == 0):
                how_wrong += 1
        return how_wrong

    num_of_blocks = len(line_spec)
    length_of_line = len(line)
    prefix_sum = [0]*(length_of_line)
    for i in range(length_of_line):
        if(i==0):
            prefix_sum[i] = int(line[i])
        elif(line[i] == 1):
            prefix_sum[i] = prefix_sum[i-1] + 1
        else:
            prefix_sum[i] = prefix_sum[i-1]
    dp = np.full((num_of_blocks, length_of_line), np.inf)


    
    for i in range(num_of_blocks):
        block_size = line_spec[i]
        for j in range(length_of_line):
            koniec = j + block_size - 1
            if(i == 0):
                if(j==0):
                    # buduje blok
                    dp[i][j] = opt_dist_one_block(j, line, block_size)
                else:
                    if(koniec<length_of_line):
                        dp[i][j] =min(
                            # zeruje prefix buduje blok tu
                            opt_dist_one_block(j, line, block_size) + prefix_sum[j-1],
                            # gdzies zbudowalem blok i zeruje sufix
                            dp[i][j-1] + int(line[koniec])
                            )
                    else:
                        # nie mam jak zbudowac bloku wiec zeruje sufix
                        dp[i][j] = dp[i][j-1]
            else:
                prev_block_size = line_spec[i-1]
                if(j<prev_block_size+1):
                    # conajmniej te pola juz sa zajete bo stoi tam blok i przerwa
                    dp[i][j] = float('inf')
                else:
                    if(koniec<length_of_line):
                        # patrze jak najtaniej zbudowalem blok tam gdzie moglem najwczesniej i dobudowuje odrazu swój (nowy), i koszt zerowania przerwy 
                        dp[i][j] = min(dp[i-1][j-prev_block_size-1] + opt_dist_one_block(j, line, block_size) + int(line[j-1]),
                        # gdzies juz zbudowalem blok i zeruje sufix
                        dp[i][j-1] + int(line[koniec]))
                    else:
                        # nie mam jak zbudowac bloku wiec zeruje sufix
                        dp[i][j] = dp[i][j-1]
    #print(dp)
    return int(dp[-1][-1])

def board_dist(board, row_spec, col_spec):
    how_wrong = 0
    for i in range(len(board)):
        how_wrong += opt_dist(board[i], row_spec[i])
    for j in range(len(board[0])):
        how_wrong += opt_dist(board[:,j], col_spec[j])
    return how_wrong

def brute_dist(line, line_spec, start):
    if start >= len(line) and len(line_spec) == 0:
        return 0
    if start >= len(line) and len(line_spec) != 0:
        return float('inf')
    if line_spec == []:
        return sum(line[start:])
    return min(
        brute_dist(line, line_spec[1:], start + line_spec[0]) + line_spec[0] - sum(line[start:start + line_spec[0]]),
        brute_dist(line, line_spec, start + 1) + int(line[start]))

def solve(board, row_spec, col_spec, how_many_tries = 15*15, mode = 'n' ):
    
    while how_many_tries > 0:
        how_many_tries -= 1
        i = np.random.randint(0, len(board))

        min_error = float('inf')
        min_j = -1
        for j in range(len(board[0])):
            test_row = cp.copy(board[i])
            test_col = cp.copy(board[:,j])
            test_row[j] = 1 - test_row[j]
            test_col[i] = 1 - test_col[i]
            row_error = opt_dist(test_row, row_spec[i])
            col_error = opt_dist(test_col, col_spec[j])
            row_error1 = brute_dist(test_row, row_spec[i], 0)
            col_error1 = brute_dist(test_col, col_spec[j], 0)
            '''
            if( row_error1!= row_error):
                print('row_error:', row_error1, row_error , test_row, row_spec[i])
            if( col_error1!= col_error):
                print('col_error:', col_error1, col_error , test_col, col_spec[j])
            #'''
            if(mode =='d1'):
                print('row:', test_row)
                print('col:', test_col)
                print('row_spec:', row_spec[i])
                print('col_spec:', col_spec[j])
                print('row_error:', row_error)
                print('col_error:', col_error)
            error = row_error + col_error
            if(error < min_error):
                min_error = error
                min_j = j

        board[i][min_j] = 1 - board[i][min_j]
        if(mode == 'd'):
            print(board)
            print('error:', min_error)
            print('row_spec:', row_spec[i])
            print('row:', board[i])
            print('col_spec:', col_spec[min_j])
            print('col:', board[:,min_j])
        board_error = board_dist(board, row_spec, col_spec)
        if(board_error == 0):
            return board
    return board_error

retries = 100

    

#board, row_spec, col_spec = parse_input()
'''
for i in range(retries):
    
    odp = solve(board, row_spec, col_spec, mode = 'n')
    print(f'try: {i}, {odp}')
    if isinstance(odp, np.ndarray):
        break
if(isinstance(odp, int)):
    print('Nie udalo sie')
else:
    file = open('zad_output.txt', 'w')
    file.write(parse_board(odp))
#'''
#board[0] = np.array([1,1,1,1,0,1,1,1,0])
#row_spec[0] = [2,2]
#print(opt_dist(board[0], row_spec[0]))
result = subprocess.run(["zad1.exe"], capture_output=True, text=True)
with open("zad_output.txt", "w") as f:
    f.write(result.stdout)