import os

def read_capacity_matrix(filepath):
    """Read a capacity matrix from a .txt file"""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())  # nombre de sommets
        capacity_matrix = []

        for i in range(1, n+1):
            row = list(map(int, lines[i].strip().split()))
            if len(row) != n:
                raise ValueError(f"Error : line {i} doesn't contain {n} elements.")
            capacity_matrix.append(row)

    return capacity_matrix

def read_capacity_and_cost_matrix(filepath):
    """Read a minimal cost flow file and return capacity and cost matrices."""
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    n = int(lines[0])
    if len(lines) != 1 + 2 * n:
        raise ValueError(f"Incorrect Format : {len(lines)} founded lines for n = {n}, expected {1 + 2 * n}")
    
    capacity_matrix = []
    cost_matrix = []

    for i in range(1, 1 + n):
        row = list(map(int, lines[i].split()))
        if len(row) != n:
            raise ValueError(f"Capacity line {i} wrong : {row}")
        capacity_matrix.append(row)

    for i in range(1 + n, 1 + 2 * n):
        row = list(map(int, lines[i].split()))
        if len(row) != n:
            raise ValueError(f"Cost line {i} wrong : {row}")
        cost_matrix.append(row)

    return capacity_matrix, cost_matrix



def display_matrix(matrix, name="Matrix"):
    print(f"\n{name}:")
    n = len(matrix)

    letters = ['S'] + [chr(ord('A') + i) for i in range(n - 1)]  
    if n > 1:
        letters[-1] = 'T'  

    print("     " + " ".join(f"{l:>4}" for l in letters)) 
    print("    " + "-----" * n)  

    for i in range(n):
        row = " ".join(f"{matrix[i][j]:>4}" for j in range(n))
        print(f"{letters[i]:>2} | {row}")  
