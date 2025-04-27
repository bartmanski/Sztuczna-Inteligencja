from collections import deque
from nonograms import generate_possibilities, deduction, cross_out
from nonograms import matrix_to_output

""" Będziemy macierz wypełniać liczbami 1 (na pewno zamazane pole), oraz 0 (na pewno puste pole).
Na początku mamy macierz height x width wypełnioną samymi -1."""


class NonogramSolver:
    def __init__(self, input: str):
        """Bierze input i przetwarza na odpowiednie wartości w polach:
        - matrix to dotychczasowe rozwiazanie
        - row/col_possibilities przechowuje dane nam możliwości rozwiązań
            dla danego wiersza / kolumny. Będziemy je skreślali później,
            tak żeby uzyskać tylko jedną możliwość."""
        tab = input.split("\n")[:-1]  # usuwamy \n z końca
        height, width = map(int, tab[0].split(" "))

        # wskazowki podane w inpucie, przesuwamy o 1 bo odczytaliśmy już width i height
        hint_rows = [[int(y) for y in x.split(" ")] for x in tab[1 : height + 1]]
        hint_cols = [[int(y) for y in x.split(" ")] for x in tab[height + 1 :]]

        self.matrix = [[-1 for __ in range(width)] for __ in range(height)]

        # policz możliwości dla każdego wiersza i każdej kolumny
        self.row_possibilities = {
            r: generate_possibilities(width, hint) for r, hint in enumerate(hint_rows)
        }
        self.col_possibilities = {
            c: generate_possibilities(height, hint) for c, hint in enumerate(hint_cols)
        }

    def solve(self):
        """Korzystamy z algorytmu AC3"""
        # trzeba sprawdzić wszystkie wiersze, oraz kolumny
        to_check = deque(
            [("r", r) for r in range(len(self.matrix))]
            + [("c", c) for c in range(len(self.matrix[0]))]
        )

        while to_check:
            kind, index = to_check.popleft()
            if kind == "r":
                possibilities = self.row_possibilities[index]
            else:
                possibilities = self.col_possibilities[index]

            conclusions = deduction(possibilities)

            for k, v in conclusions.items():
                """ 1. Zamaż wydedukowany kwadracik. 
                2. wykreśl niepasujące możliwości,
                3. sprawdź kolumne/wiersz czy da się więcej wydedukować """
                if kind == "r" and self.matrix[index][k] != v:
                    self.matrix[index][k] = v
                    cross_out(self.col_possibilities, k, index, v)
                    if ("c", k) not in to_check:
                        to_check.append(("c", k))

                elif kind == "c" and self.matrix[k][index] != v:
                    self.matrix[k][index] = v
                    cross_out(self.row_possibilities, k, index, v)
                    if ("r", k) not in to_check:
                        to_check.append(("r", k))

        return self.matrix


with open("zad_input.txt", "r") as input_file:
    solver = NonogramSolver(input_file.read())

solution = solver.solve()
output = matrix_to_output(solution)

with open("zad_output.txt", "w") as output_file:
    output_file.write(output)
