def push_relabel(capacity_mtx, source, sink):
    
    n = len(capacity_mtx)
    flow = [[0] * n for _ in range(n)]
    excess = [0] * n
    height = [0] * n

    def initialize():
        # Initialize preflow and heights.
        print("Initializing preflow and heights...")
        for u in range(n):
            height[u] = 0
            excess[u] = 0
        height[source] = n
        for v in range(n):
            if capacity_mtx[source][v] > 0:
                flow[source][v] = capacity_mtx[source][v]
                flow[v][source] = -capacity_mtx[source][v]
                excess[v] = capacity_mtx[source][v]
                excess[source] -= capacity_mtx[source][v]
                print(f"Preflow initialized: flow[{source}][{v}] = {flow[source][v]}")

    def push(u, v):
        # Push flow from u to v.
        if excess[u] > 0 and capacity_mtx[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
            delta = min(excess[u], capacity_mtx[u][v] - flow[u][v])
            flow[u][v] += delta
            flow[v][u] -= delta
            excess[u] -= delta
            excess[v] += delta
            print(f"Pushed {delta} from {u} to {v}. Updated excess[{u}] = {excess[u]}, excess[{v}] = {excess[v]}")

    def relabel(u):
        # Relabel the height of vertex u.
        if excess[u] > 0:
            min_height = float('inf')
            for v in range(n):
                if capacity_mtx[u][v] - flow[u][v] > 0:
                    min_height = min(min_height, height[v])
            if min_height < float('inf'):
                old_height = height[u]
                height[u] = min_height + 1
                print(f"Relabeled vertex {u}: height changed from {old_height} to {height[u]}")

    def discharge(u):
        # Discharge excess flow from vertex u.
        print(f"Discharging vertex {u} with excess {excess[u]} and height {height[u]}...")
        while excess[u] > 0:
            for v in range(n):
                if excess[u] > 0:
                    push(u, v)
            if excess[u] > 0:
                relabel(u)

    # Initialize preflow
    initialize()

    # Process active vertices
    active = [u for u in range(n) if u != source and u != sink and excess[u] > 0]
    iteration = 0
    while active:
        iteration += 1
        u = max(active, key=lambda x: height[x])
        print(f"\nIteration {iteration}: Processing vertex {u} with height {height[u]} and excess {excess[u]}")
        discharge(u)
        if excess[u] > 0:
            active.append(u)
        active.remove(u)
        print(f"Active vertices after iteration {iteration}: {active}")

    # Calculate the maximum flow
    max_flow = sum(flow[source][v] for v in range(n))
    return max_flow