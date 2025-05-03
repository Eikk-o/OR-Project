def bellman_ford(capacity, cost, source):
    n = len(capacity)
    dist = [float('inf')] * n
    dist[source] = 0

    print(f"Step 0 : {['∞' if d == float('inf') else d for d in dist]}")
    
    # Iterations Bellman-Ford
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

    # Detection nagatif cycle
    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                print("⚠️ Negatif cycle detected.")
                return None

    return dist

# min_cost_flow(capacity_matrix, cost_matrix, s, t, flow_val)
