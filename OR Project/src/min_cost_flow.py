from typing import List, Tuple


def label(i, n):
    # Si i == 0, on retourne 'S' pour le premier noeud
    if i == 0:
        return 'S'
    # Si i == n-1, on retourne 'T' pour le dernier noeud
    elif i == n - 1:
        return 'T'
    # Pour les autres indices, on retourne les lettres intermédiaires
    return chr(65 + i - 1)  # 65 est 'A' dans ASCII, donc on commence à 'A' après 'S'

def display_labeled_matrix(matrix, name="Residual Graph"):
    n = len(matrix)
    labels = [label(i, n) for i in range(n)]
    print(f"\n{name}:")
    header = "    " + " ".join(f"{l:>4}" for l in labels)
    print(header)
    print("    " + "-----" * n)
    
    for i in range(n):
        row = " ".join(f"{matrix[i][j]:>4}" for j in range(n))
        print(f"{labels[i]:>2} | {row}")



def letter_to_index(letter):

    return ord(letter.upper()) - ord('S')  

def bellman_ford(capacity, cost, source):
    n = len(capacity)
    dist = [float('inf')] * n
    dist[source] = 0

    print(f"Step 0 : {['∞' if d == float('inf') else d for d in dist]}")

    for k in range(n - 1):
        updated = False
        new_dist = dist.copy()
        for u in range(n):
            for v in range(n):
                if capacity[u][v] > 0 and dist[u] + cost[u][v] < new_dist[v]:
                    new_dist[v] = dist[u] + cost[u][v]
                    updated = True
        dist = new_dist
        affichage = ['∞' if d == float('inf') else d for d in dist]
        print(f"Step {k+1} : {affichage}")
        if not updated:
            break

    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                print("⚠️ Negatif cycle detected.")
                return None

    return dist

min_cost_flow(capacity_matrix, cost_matrix, s, t, flow_val)
