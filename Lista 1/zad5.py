import numpy as np

def opt_dist(lst, D):
    n = len(lst)
    min_changes = float('inf')
    
    for start in range(n - D + 1):
        changes = sum(1 for i in range(n) if (start <= i < start + D) != (lst[i] == 1))
        min_changes = min(min_changes, changes)
    
    if D == 0:
        return lst.count(1)
    
    return min_changes

def calculate_dist(board,row_sums, col_sums):
    n , m = board.shape 
    row_dist = 0
    col_dist = 0
    for i in range(n):
        #print(f'row: {board[i]} , row_data: {row_sums[i]} , opt_dist: {opt_dist(board[i], row_sums[i])}')
        row_dist += opt_dist(board[i], row_sums[i])
    for i in range(m):
        col_dist += opt_dist(board[:, i], col_sums[i])
    return row_dist + col_dist

def parse_board(board):
    n , m = board.shape
    return '\n'.join([''.join(['#' if board[i][j] == 1 else '.' for j in range(m)]) for i in range(n)])

def HasZerosBetweenOnes(row):
    ones = False
    for i in range(len(row)):
        if row[i] == 1:
            ones = True
        if row[i] == 0 and ones:
            return True
    return False

def solve(data):
    datacp = data
    data = data.split('\n')
    n, m = data[0].split()
    n,m = int(n), int(m)
    board = np.zeros((n, m))
    row_sums = []
    col_sums = []
    for i in range(1, n+1):
        row_sums.append(int(data[i]))
    
    for i in range(n+1, n+m+1):
        col_sums.append(int(data[i]))
    
    curr_row_sum = np.zeros(n)
    curr_col_sum = np.zeros(m)
    max_iter = 100
    dist = calculate_dist(board,row_sums, col_sums)

    for j in range(max_iter):
        if(dist == 0):
            break
        random_row=np.random.randint(n)
        min_dist = float('inf')
        licznik = 0
        while row_sums[random_row] == curr_row_sum[random_row] and not HasZerosBetweenOnes(board[random_row]):
            
            if(licznik >= n):
                random_row = np.random.randint(n)
            random_row = random_row + 1
            if random_row == n:
                random_row = 0
            licznik += 1
        
        '''
        print(f'wybrałem kolumne {random_row}')
        print('plansza:')
        print(board)
        print('/////////////////////////')
        print(f'row_sums: {curr_row_sum} , what should be: {row_sums}')
        print(f'col_sums: {curr_col_sum} , what should be: {col_sums}')
        print(f'dist: {dist}')
        '''

        for i in range(m):
            # kopia board-a zeby nie zmieniac oryginalki
            test_row_sum = np.copy(curr_row_sum)
            test_col_sum = np.copy(curr_col_sum)
            test_row_sum[random_row] = curr_row_sum[random_row] + 1 - 2*board[random_row][i]
            test_col_sum[i] = curr_col_sum[i] + 1 - 2*board[random_row][i]
            test_board = np.copy(board)
            test_board[random_row][i] = 1 - test_board[random_row][i]
            test_dist = calculate_dist(test_board, row_sums, col_sums)
            if test_dist < min_dist:
                # szukanie min

                min_board = test_board
                min_dist = test_dist
                min_row_sum = test_row_sum
                min_col_sum = test_col_sum
                min_i = i

        board = min_board
        dist = min_dist
        curr_row_sum = min_row_sum
        curr_col_sum = min_col_sum
    if(dist==0):
        return parse_board(board), col_sums, row_sums, dist
    else:
        return solve(datacp)

inputy = [{'inp': '7 7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n7\n',
                     'out': '#######\n'
                            '#######\n'
                            '#######\n'
                            '#######\n'
                            '#######\n'
                            '#######\n'
                            '#######\n'},
                    {'inp': '7 7\n2\n2\n7\n7\n2\n2\n2\n2\n2\n7\n7\n2\n2\n2\n',
                     'out': '..##...\n'
                            '..##...\n'
                            '#######\n'
                            '#######\n'
                            '..##...\n'
                            '..##...\n'
                            '..##...\n'},
                    {'inp': '7 7\n2\n2\n7\n7\n2\n2\n2\n4\n4\n2\n2\n2\n5\n5\n',
                     'out': '##.....\n'
                            '##.....\n'
                            '#######\n'
                            '#######\n'
                            '.....##\n'
                            '.....##\n'
                            '.....##\n'},
                    {'inp': '7 7\n7\n6\n5\n4\n3\n2\n1\n1\n2\n3\n4\n5\n6\n7\n',
                     'out': '#######\n'
                            '.######\n'
                            '..#####\n'
                            '...####\n'
                            '....###\n'
                            '.....##\n'
                            '......#\n'},
                    {'inp': '7 7\n7\n5\n3\n1\n1\n1\n1\n1\n2\n3\n7\n3\n2\n1\n',
                     'out': '#######\n'
                            '.#####.\n'
                            '..###..\n'
                            '...#...\n'
                            '...#...\n'
                            '...#...\n'
                            '...#...\n'}]
                

for input in inputy:
    board,rows,cols,dist = solve(input['inp'])
    print('///////////////////////////////////')
    print(board)
    print('///////////////////////////////////')
    print(input['out'])
    print('///////////////////////////////////')
    print(dist)

#print(solve(inputy[0]['inp']))
