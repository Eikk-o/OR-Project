import time
import random
from push_relabel import push_relabel
from min_cost_flow import min_cost_flow
# from ford_fulkerson import ford_fulkerson  # Uncomment if implemented

def create_random_flow_problem(n):

    # Initialize capacity and cost matrices with zeros
    C = [[0] * n for _ in range(n)]
    D = [[0] * n for _ in range(n)]

    # Generate random capacities and costs for E(n^2 / 2) edges
    num_edges = (n * (n - 1)) // 2  # E(n^2 / 2)
    edges = random.sample([(i, j) for i in range(n) for j in range(n) if i != j], num_edges)

    for i, j in edges:
        C[i][j] = random.randint(1, 100)  # Random capacity
        D[i][j] = random.randint(1, 100)  # Random cost

    return C, D


def measure_execution_time(n_values):
    nb_tries = 100

    for n in n_values:
        print(f"\nFor n = {n} :")
        pr_times = []
        # min_cost_times = []
        # ff_times = []

        for a in range(nb_tries):
            # Generate a random flow problem
            cap_mtx, cost_mtx = create_random_flow_problem(n)

            # Measure Push-Relabel
            start = time.perf_counter()
            push_relabel(cap_mtx, 0, n - 1)
            end = time.perf_counter()
            pr_times.append(end - start)

            """ # Measure Min-Cost Flow
            start = time.perf_counter()
            min_cost_flow(n, cap_mtx, cost_mtx, 0, n - 1, F=None)  # F=None for max flow
            end = time.perf_counter()
            min_cost_times.append(end - start) """

            """  # Measure Ford-Fulkerson (if implemented)
            start = time.perf_counter()
            ford_fulkerson(cap_mtx, 0, n - 1)
            end = time.perf_counter()
            ff_times.append(end - start) """

            # Print results
            print(f"Iteration {a} for push_relabel: {pr_times[-1]:.6f} seconds")

        # Store average times
        results["push_relabel"][n] = sum(pr_times) / nb_tries
        # results["min_cost_flow"][n] = sum(min_cost_times) / nb_tries
        # results["ford_fulkerson"][n] = sum(ff_times) / nb_tries

    return pr_times

if __name__ == "__main__":
    # Values of n to test
    n_values = [10, 20, 40, 100, 400, 1000, 4000]

    # Measure execution times
    results = measure_execution_time(n_values)

    # Print results
    print("\nExecution Times (in seconds):")
    for algo, times in results.items():
        print(f"\n{algo}:")
        for n, time_taken in times.items():
            print(f"  n = {n}: {time_taken:.6f} seconds")
