from collections import deque
from typing import List, Tuple
from reader import display_matrix  # Assure-toi que display_matrix est bien importée de ton module reader

def label(u: int) -> str:
    return chr(ord('A') + u)

def push_relabel_trace(C: List[List[int]], s: int, t: int) -> Tuple[int, List[List[int]]]:
    n = len(C)
    R = [row[:] for row in C]  # Copie de la matrice C (capacités résiduelles)
    height = [0] * n  # Hauteurs initiales
    excess = [0] * n  # Excédents initiaux
    height[s] = n  # Hauteur du sommet source
    
    # Initialisation du pré-flux
    for v in range(n):
        if C[s][v] > 0:
            flow = C[s][v]
            R[s][v] -= flow
            R[v][s] += flow
            excess[v] = flow
            excess[s] -= flow
            print(f"PUSH {flow} from {label(s)} to {label(v)} (initial preflow)")

    # Liste des sommets actifs
    active = deque([u for u in range(n) if u not in (s, t) and excess[u] > 0])
    iteration = 1
    print(f"\nInitial Residual Capacities (R):")
    display_matrix(R, "Residual Matrix")  # Affichage avec la fonction importée
    print(f"\nInitial Heights: {height}")
    print(f"Initial Excesses: {excess}")
    
    while active:
        u = active[0]
        pushed = False
        
        for v in range(n):
            if R[u][v] > 0 and height[u] == height[v] + 1:
                delta = min(excess[u], R[u][v])
                R[u][v] -= delta
                R[v][u] += delta
                excess[u] -= delta
                old_excess_v = excess[v]
                excess[v] += delta
                print(f"Iteration {iteration}: PUSH {delta} from {label(u)} to {label(v)}; excess[{label(u)}]={excess[u]}; excess[{label(v)}]={excess[v]}")
                if v not in (s, t) and old_excess_v == 0:
                    active.append(v)
                if excess[u] == 0:
                    active.popleft()
                pushed = True
                break
        
        if not pushed:
            # Relabel si aucune poussée n'a eu lieu
            min_h = min(height[v] for v in range(n) if R[u][v] > 0)
            old_h = height[u]
            height[u] = min_h + 1
            print(f"Iteration {iteration}: RELABEL {label(u)} from {old_h} to {height[u]}")

        # Affichage après chaque itération
        print(f"\nAfter iteration {iteration}:")
        print(f"Heights: {height}")
        print(f"Excesses: {excess}")
        display_matrix(R, "Residual Matrix")  # Affichage avec la fonction importée
        iteration += 1

    max_flow = excess[t]
    print(f"\nValue of the max flow max = {max_flow}\n")
    return max_flow, R
