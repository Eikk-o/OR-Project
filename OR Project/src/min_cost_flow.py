import copy
from reader import read_capacity_and_cost_matrix, display_matrix

import heapq

def index_to_letter1(i, n):
    if i == 0:
        return 's'
    elif i == n - 1:
        return 't'
    else:
        return chr(ord('a') + i - 1)
    
def bellman(cost, source):
    n = len(cost)
    dist = [float('inf')] * n
    pred = [-1] * n
    visited = [False] * n
    dist[source] = 0

    pq = [(0, source)]
    step = 0
    no_update_steps = 0

    print(f"Step {step} : {['∞' if d == float('inf') else d for d in dist]}")

    while pq and no_update_steps < 1:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True

        updated = False

        for v in range(n):
            if cost[u][v] != 0 and not visited[v]:
                new_dist = dist[u] + cost[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    pred[v] = u
                    heapq.heappush(pq, (new_dist, v))
                    updated = True

        print(f"Step {step + 1} : {['∞' if d == float('inf') else d for d in dist]}")

        
        if updated:
            no_update_steps = 0  
        else:
            no_update_steps += 1  

        step += 1

    if no_update_steps >= 1:
        print(f"🔁 Stopping early: no updates for 2 consecutive steps.")

    print("\nShortest paths from source:")
    for target in range(n):
        if dist[target] == float('inf'):
            print(f" - Node {index_to_letter1(target, n)}: unreachable")
        else:
            path = []
            current = target
            while current != -1:
                path.append(index_to_letter1(current, n))
                current = pred[current]
            path.reverse()
            print(f" - Node {index_to_letter1(target, n)}: distance = {dist[target]}, path = {path}")

    return dist, pred






def letter_to_index(letter, n):
   
    letter = letter.upper()
    if letter == 'S':
        return 0  # Source
    elif letter == 'T':
        return n - 1  # Sink
    else:
        return ord(letter) - ord('A') + 1

def index_to_letter(index, n):
    
    if index == 0:
        return 'S'  # Source
    elif index == n - 1:
        return 'T'  # Sink
    else:
        return chr(ord('A') + index - 1)


def build_node_map(capacity):
   
    n = len(capacity)
    node_map = {}
    for i in range(n):
        if i == 0:
            node_map[i] = 'Source'
        elif i == n - 1:
            node_map[i] = 'Sink'
        else:
            node_map[i] = chr(ord('A') + i - 1)
    return node_map

def create_residual_graph(capacity, cost):
    n = len(capacity)
    residual_capacity = [[0 for _ in range(n)] for _ in range(n)]
    residual_cost = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if capacity[i][j] > 0:
                residual_capacity[i][j] = capacity[i][j]
                residual_cost[i][j] = cost[i][j]
                residual_cost[j][i] = -cost[i][j]

    return residual_capacity, residual_cost

def bellman_ford(capacity, cost, source, sink, show_steps=False):
    n = len(capacity)
    dist = [float('inf')] * n
    dist[source] = 0
    pred = [-1] * n

    if show_steps:
        print(f"Initial distances: {['∞' if d == float('inf') else d for d in dist]}")

    for k in range(n - 1):
        updated = False
        new_dist = dist.copy()

        for u in range(n):
            for v in range(n):
                if capacity[u][v] > 0 and dist[u] + cost[u][v] < new_dist[v]:
                    new_dist[v] = dist[u] + cost[u][v]
                    pred[v] = u
                    updated = True
        
        dist = new_dist

        if show_steps:
            affichage = ['∞' if d == float('inf') else d for d in dist]
            print(f"Step {k + 1} : {affichage}")

        if not updated:
            break

    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                print("⚠️ Negative cycle detected.")
                return None, None

    if dist[sink] == float('inf'):
        print(" ")
        return None, None

    path = []
    curr = sink
    while curr != source:
        path.append(curr)
        curr = pred[curr]
    path.append(source)
    path.reverse()

    bottleneck = float('inf')
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        bottleneck = min(bottleneck, capacity[u][v])

    return path, bottleneck


def augment_flow(capacity, path, flow):
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        capacity[u][v] -= flow
        capacity[v][u] += flow

def calculate_max_flow_possible(capacity, cost, source, sink):
   
    residual_capacity, residual_cost = create_residual_graph(capacity, cost)
    max_flow = 0
    while True:
        path, flow = bellman_ford(residual_capacity, residual_cost, source, sink)
        if path is None:
            break
        max_flow += flow
        augment_flow(residual_capacity, path, flow)
    return max_flow

def min_cost_flow(capacity, cost, target_flow=None, source=0, sink=None):
    
    if sink is None:
        sink = len(capacity) - 1  
    
    max_possible_flow = calculate_max_flow_possible(capacity, cost, source, sink)
    if target_flow > max_possible_flow:
        print(f"\n❌ The demanded flow ({target_flow}) cannot be reach.")
        print(f"✔️ Maximum Flow impossible between '{source}' et '{sink}' is  {max_possible_flow}.")
        return 0, 0

    
    if target_flow is None:
        max_possible_flow = calculate_max_flow_possible(capacity, cost, source, sink)
        print(f"\nThe maximum possible flow in this network is: {max_possible_flow}")
        while True:
            try:
                print(f"Enter desired flow value (1-{max_possible_flow}): ")
                target_flow = int(input(">> "))
                if 0 < target_flow <= max_possible_flow:
                    break
                print(f"Please enter a value between 1 and {max_possible_flow}")
            except ValueError:
                print("Please enter a valid number")

    residual_capacity, residual_cost = create_residual_graph(capacity, cost)
    total_flow = 0
    total_cost = 0
    iteration = 1

    
    display_matrix(residual_capacity, "Residual Capacity")
    display_matrix(residual_cost, "Residual Cost")

    while total_flow < target_flow:
        path, flow = bellman_ford(residual_capacity, residual_cost, source, sink, show_steps=False)

        if path is None:
            print(f"\nCannot achieve desired flow of {target_flow}.")
            print(f"Maximum flow possible is {total_flow} with cost {total_cost}.")
            return total_flow, total_cost

        flow = min(flow, target_flow - total_flow)
        total_flow += flow

        path_cost = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_cost += residual_cost[u][v] * flow
        total_cost += path_cost

        path_letters = [index_to_letter(node, len(capacity)) for node in path]

        print(f"\nIteration {iteration}:")
        print(f"Augmenting path: {' -> '.join(path_letters)}")
        print(f"Bottleneck flow: {flow}")
        print(f"Path cost: {path_cost}")

        augment_flow(residual_capacity, path, flow)

        print("Updated residual graphs:")
        display_matrix(residual_capacity, "Residual Capacity")
        display_matrix(residual_cost, "Residual Cost")

        iteration += 1

    print("\nFinal result:")
    print(f"Achieved flow: {total_flow}")
    print(f"Minimum cost: {total_cost}")
    return total_flow, total_cost
