import os

def read_capacity_matrix(filepath):
    """Lit une matrice de capacité à partir d’un fichier .txt"""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        n = int(lines[0].strip())  # nombre de sommets
        capacity_matrix = []

        for i in range(1, n+1):
            row = list(map(int, lines[i].strip().split()))
            if len(row) != n:
                raise ValueError(f"Erreur : la ligne {i} ne contient pas {n} éléments.")
            capacity_matrix.append(row)

    return capacity_matrix

def read_capacity_and_cost_matrix(filepath):
    """Lit un fichier de flot de coût minimal et retourne les matrices capacité et coût."""
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    n = int(lines[0])
    if len(lines) != 1 + 2 * n:
        raise ValueError(f"Format incorrect : {len(lines)} lignes trouvées pour n = {n}, attendu {1 + 2 * n}")
    
    capacity_matrix = []
    cost_matrix = []

    for i in range(1, 1 + n):
        row = list(map(int, lines[i].split()))
        if len(row) != n:
            raise ValueError(f"Ligne de capacité {i} incorrecte : {row}")
        capacity_matrix.append(row)

    for i in range(1 + n, 1 + 2 * n):
        row = list(map(int, lines[i].split()))
        if len(row) != n:
            raise ValueError(f"Ligne de coût {i} incorrecte : {row}")
        cost_matrix.append(row)

    return capacity_matrix, cost_matrix



def display_matrix(matrix, name="Matrix"):
    print(f"\n{name}:")
    n = len(matrix)
    
    # Afficher l'en-tête
    print("    " + " ".join(f"{j+1:>4}" for j in range(n)))
    print("    " + "-----" * n)

    # Afficher chaque ligne avec l'indice de la ligne
    for i in range(n):
        row = " ".join(f"{matrix[i][j]:>4}" for j in range(n))
        print(f"{i+1:>2} | {row}")