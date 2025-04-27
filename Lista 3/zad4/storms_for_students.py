import sys

def B(i, j):
    return f"B_{i}_{j}"

def domains(variables):
    return [var + " in 0..1" for var in variables]

def filled_squares_constraints(triples):
    return [f"{B(i, j)} #= {v}" for i, j, v in triples]

def get_row(i):
    return [B(i, j) for j in range(width)]

def get_col(j):
    return [B(i, j) for i in range(height)]

def sum_equals(variables, K):
    return " + ".join(variables) + f" #= {K}"

def hint_constraints(hint_rows, hint_cols):
    constraints = []
    for i, hint in enumerate(hint_rows):
        constraints.append(sum_equals(get_row(i), hint))
    for j, hint in enumerate(hint_cols):
        constraints.append(sum_equals(get_col(j), hint))
    return constraints

def illegal_rectangles_constraints():
    constraints = []

    for i in range(height):
        for j in range(1, width - 1):
            constraints.append(
                f"tuples_in([[{B(i, j-1)}, {B(i, j)}, {B(i, j+1)}]], [[0,0,0],[0,0,1],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])"
            )

    for i in range(1, height - 1):
        for j in range(width):
            constraints.append(
                f"tuples_in([[{B(i-1, j)}, {B(i, j)}, {B(i+1, j)}]], [[0,0,0],[0,0,1],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])"
            )

    for i in range(height - 1):
        for j in range(width - 1):
            square = f"[[{B(i, j)}, {B(i, j+1)}, {B(i+1, j)}, {B(i+1, j+1)}]]"
            constraints.append(
                f"tuples_in({square}, [[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]])"
            )

    return constraints

def write_constraints(constraints, indent, d):
    position = indent
    print(" " * indent, end="")
    for c in constraints:
        print(c + ",", end=" ")
        position += len(c)
        if position > d:
            position = indent
            print()
            print(" " * indent, end="")

def storms(hint_rows, hint_cols, triples):
    global height
    global width
    height = len(hint_rows)
    width = len(hint_cols)

    variables = [B(i, j) for i in range(height) for j in range(width)]

    print(":- use_module(library(clpfd)).")
    print(f"solve([{', '.join(variables)}]) :-")

    constraints = (
        domains(variables)
        + filled_squares_constraints(triples)
        + hint_constraints(hint_rows, hint_cols)
        + illegal_rectangles_constraints()
    )
    write_constraints(constraints, 4, 70)

    print()
    print(f"    labeling([ff], [{', '.join(variables)}]).")
    print()
    print(":- solve(X), write(X), nl.")

# ------------------------------------------------------

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    
    rows = list(map(int, lines[0].split()))
    cols = list(map(int, lines[1].split()))
    triples = []

    for line in lines[2:]:
        triples.append(list(map(int, line.split())))

    storms(rows, cols, triples)
