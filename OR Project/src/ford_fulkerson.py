from collections import deque
from reader import display_matrix


def _bfs(residual, source, sink, parent):
    n = len(residual)
    visited = [False] * n
    queue = deque([source])
    visited[source] = True
    parent[source] = -1

    # For trace: record levels
    level = {source: 0}
    print("BFS levels and predecessors:")

    while queue:
        u = queue.popleft()
        for v, cap in enumerate(residual[u]):
            if not visited[v] and cap > 0:
                visited[v] = True
                parent[v] = u
                level[v] = level[u] + 1
                print(f" node {v} <- {u} (level {level[v]})")
                if v == sink:
                    return True
                queue.append(v)
    return False


def ford_fulkerson(capacity, source=0, sink=None):
    n = len(capacity)
    if sink is None:
        sink = n - 1

    # Initialize residual graph
    residual = [row[:] for row in capacity]
    parent = [-1] * n
    max_flow = 0
    iteration = 1

    print("Initial residual graph:")
    display_matrix(residual, "Residual Capacity")

    # Augment while there is a path from source to sink
    while _bfs(residual, source, sink, parent):
        # Reconstruct path and find bottleneck
        path = []
        v = sink
        bottleneck = float('inf')
        while v != source:
            u = parent[v]
            path.append((u, v))
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        path.reverse()

        # Trace output
        print(f"\nIteration {iteration}:")
        print(f" Augmenting path: { ' -> '.join(str(u) for u, _ in path) } -> {sink} with bottleneck {bottleneck}")

        # Update residual capacities
        for u, v in path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        max_flow += bottleneck
        print(" Updated residual graph:")
        display_matrix(residual, "Residual Capacity")

        iteration += 1
        
    return max_flow
