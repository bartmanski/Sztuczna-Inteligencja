from queue import PriorityQueue,Queue


def hash(positions, kolumny , wiersze):
        a,b=0,0
        what = max(kolumny, wiersze)
        mno=1
        for pos in positions:
            a+=pos[0]*mno
            b+=pos[1]*mno
            mno*=what
        return (a,b)

def manhatan_heuristic(positions, end_positions):
    distance = 0
    for pos in positions:
        min_dist = float('inf')
        for end_pos in end_positions:
            dist = abs(pos[0] - end_pos[0]) + abs(pos[1] - end_pos[1])
            min_dist = min(min_dist, dist)
        distance += min_dist
    return distance

def multi_source_bfs(grid, n, m, goal_positions):
    dist = [[float('inf')] * m for _ in range(n)]
    q = Queue()
    
    for gx, gy in goal_positions:
        dist[gx][gy] = 0
        q.put((gx, gy))
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while not q.empty():
        x, y = q.get()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != '#':
                if dist[nx][ny] > dist[x][y] + 1:
                    dist[nx][ny] =dist[x][y] + 1
                    q.put((nx, ny))  # Enqueue the new position
    
    return dist

def PFS_hueristic(positions, dist):
    distance = 0
    for pos in positions:
        if dist[pos[0]][pos[1]] == float('inf'):
            return float('inf')
        distance += dist[pos[0]][pos[1]]
    
    return distance

def PFS_MAX_hueristic(positions, dist):
    max_distance = 0
    for pos in positions:
        if dist[pos[0]][pos[1]] == float('inf'):
            return float('inf')
        max_distance = max(max_distance, dist[pos[0]][pos[1]])
    
    return max_distance

def PFS_MAX_PlUS_MOVES_hueristic(positions, moves, dist):
    max_distance = 0
    for pos in positions:
        if dist[pos[0]][pos[1]] == float('inf'):
            return float('inf')
        max_distance = max(max_distance, dist[pos[0]][pos[1]]+moves)
    
    return max_distance

class state:
    def __init__(self, posible_positions,moves_made=''):
        self.positions = posible_positions
        self.moves_made = moves_made

    def __str__(self):
        return f"Positions: {self.positions}, Moves: {self.moves_made}"
    
    def __repr__(self):
        positions_str = '\n'.join([f"\t{pos}" for pos in self.positions])
        return f"Positions:\n{positions_str}\nMoves: {self.moves_made}"
    
    def all_good(self, end_positions):
        for pos in self.positions:
            if pos not in end_positions:
                return False
        return True

    def move_all(self, dx, dy, letter):
        new_positions = set()
        for pos in self.positions:
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != '#':
                new_positions.add((new_x, new_y))
            else:
                new_positions.add(pos)
        return state(new_positions, self.moves_made + letter)

    def gen_new_states(self):
        new_states = []
        for dx, dy, letter in [(1, 0, 'D'), (-1, 0, 'U'), (0, 1, 'R'), (0, -1, 'L')]:
            new_state = self.move_all(dx, dy, letter)
            new_states.append(new_state)
        return new_states
    
    
    def solve(self, end_positions, kolumny, wiersze, prepocessed_heuristic=None):
        queue = PriorityQueue()
        queue.put((0,id(self), self))
        visited = set()
        visited.add(hash(self.positions,kolumny, wiersze))
        
        while not queue.empty():
            _, _, current_state = queue.get()
            
            if current_state.all_good(end_positions):
                return current_state.moves_made
            
            for new_state in current_state.gen_new_states():
                if hash(new_state.positions,kolumny,wiersze) not in visited:
                    visited.add(hash(new_state.positions,kolumny, wiersze))
                    queue.put((PFS_MAX_PlUS_MOVES_hueristic(new_state.positions,len(new_state.moves_made),prepocessed_heuristic),id(new_state), new_state))
        
        return None

def preprocess(grid):
    start_positions = set()
    end_positions = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start_positions.add((i, j))
            elif grid[i][j] == 'B':
                start_positions.add((i, j))
                end_positions.add((i, j))
            elif grid[i][j] == 'G':
                end_positions.add((i, j))
    return state(start_positions), end_positions

file = open("zad_input.txt", "r")
grid = [list(line.strip()) for line in file.readlines()]
file.close()

start_state, end_positions = preprocess(grid)
dist = multi_source_bfs(grid, len(grid), len(grid[0]), end_positions)
res=start_state.solve(end_positions, len(grid[0]), len(grid), dist)
file = open("zad_output.txt", "w")
file.write(res)
file.close()