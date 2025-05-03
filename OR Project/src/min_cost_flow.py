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

def min_cost_flow(n: int, C: List[List[int]], D: List[List[int]], 
                 s: int, t: int, F: int) -> Tuple[int, int]:
    # Initialisation des matrices résiduelles
    R = [row[:] for row in C]  # R est une copie de la matrice de capacité C
    flow = 0
    total_cost = 0
    
    while flow < F:
        # Étape 1: Trouver le chemin le moins cher avec Bellman-Ford
        dist = [float('inf')] * n
        pred = [None] * n
        dist[s] = 0
        
        # Relaxation des arêtes
        for _ in range(n-1):  # On effectue n-1 relaxations
            for u in range(n):
                for v in range(n):
                    if R[u][v] > 0 and dist[u] + D[u][v] < dist[v]:
                        dist[v] = dist[u] + D[u][v]
                        pred[v] = u
        
        # Vérification du chemin complet
        if pred[t] is None:
            print("❌ Aucun chemin vers la cible trouvé!")
            break
            
        # Reconstruction du chemin
        path = []
        node = t
        while node != s:
            path.append(node)
            node = pred[node]
            if node is None:
                print("❌ Chemin incomplet détecté!")
                # Bloque la dernière arête invalide
                R[path[-2]][path[-1]] = 0
                break
        path.append(s)
        path.reverse()
        
        # Validation finale du chemin
        if path[0] != s or path[-1] != t:
            print(f"❌ Chemin invalide ignoré: {'->'.join(str(v) for v in path)}")
            continue
            
        # Calcul du flux possible
        delta = min(R[u][v] for u,v in zip(path, path[1:]))  # Trouver le flux maximal possible
        delta = min(delta, F - flow)  # Ne pas dépasser le flux total désiré
        
        # Mise à jour des flux
        for u,v in zip(path, path[1:]):
            R[u][v] -= delta  # Réduire la capacité résiduelle
            R[v][u] += delta  # Ajouter la capacité à l'arête inverse (flux inverse)
            total_cost += D[u][v] * delta  # Calculer le coût de ce flux
        
        flow += delta  # Augmenter le flux total
        print(f"✔ Chemin: {'->'.join(str(v) for v in path)}")
        print(f"   → Flux envoyé: {delta} unités (total: {flow}/{F})")
        print(f"   → Coût ajouté: {D[u][v] * delta} (total: {total_cost})")
        
        # Affichage des modifications dans le graphe résiduel
        print("Modifications du graphe résiduel:")
        for i in range(n):
            for j in range(n):
                if R[i][j] != C[i][j]:
                    print(f"   → Capacité résiduelle de {i} à {j}: {R[i][j]}")
    
    return flow, total_cost
