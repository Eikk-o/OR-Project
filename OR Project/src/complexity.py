import time
import random
import matplotlib.pyplot as plt
from push_relabel import push_relabel_trace
from min_cost_flow import min_cost_flow
from ford_fulkerson import ford_fulkerson 

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


def measure_execution_time(n_values, algorithm="push_relabel"):

    nb_tries = 100
    results = {}

    for n in n_values:
        print(f"\nFor n = {n} :")
        times = []

        for a in range(nb_tries):
            # Generate a random flow problem
            cap_mtx, cost_mtx = create_random_flow_problem(n)

            # Measure the selected algorithm
            if algorithm == "push_relabel":
                start = time.perf_counter()
                push_relabel_trace(cap_mtx, 0, n - 1)
                end = time.perf_counter()
            elif algorithm == "min_cost_flow":
                start = time.perf_counter()
                min_cost_flow(n, cap_mtx, cost_mtx, 0, n - 1, F=None)  # F=None for max flow
                end = time.perf_counter()
            elif algorithm == "ford_fulkerson":
                start = time.perf_counter()
                ford_fulkerson(cap_mtx, 0, n - 1)
                end = time.perf_counter()
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")

            times.append(end - start)
            print(f"Iteration {a} for {algorithm}: {times[-1]:.6f} seconds")

        results[n] = times

    return results


def plot_results(results, algorithm):

    plt.figure(figsize=(10, 6))

    for n, times in results.items():
        # Plot all 100 times for each n
        plt.scatter([n] * len(times), times, label=f"n = {n}", alpha=0.6)

    # Configure plot
    plt.xlabel("Number of Vertices (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Execution Times for {algorithm}")
    plt.grid(True)
    plt.legend()
    plt.xscale("log")  # Use logarithmic scale for x-axis
    plt.yscale("log")  # Use logarithmic scale for y-axis
    plt.show()


def plot_worst_case(results, algorithm):

    n_values = list(results.keys())
    worst_times = [max(times) for times in results.values()]  # Get the worst time for each n

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, worst_times, marker="o", label=f"Worst-Case {algorithm}")

    # Configure plot
    plt.xlabel("Number of Vertices (n)")
    plt.ylabel("Worst Execution Time (seconds)")
    plt.title(f"Worst-Case Execution Times for {algorithm}")
    plt.grid(True)
    plt.legend()
    plt.xscale("log")  # Use logarithmic scale for x-axis
    plt.yscale("log")  # Use logarithmic scale for y-axis
    plt.show()


if __name__ == "__main__":
    # Values of n to test
    n_values = [10, 20, 40, 100, 400]  # Reduced for faster testing
    # n_values = [10, 20, 40, 100, 400, 1000, 4000] # Full range

    # Specify the algorithm to measure
    algo_to_run = "ford_fulkerson"  # "push_relabel" or "min_cost_flow" or "ford_fulkerson"

    # Measure execution times
    results = measure_execution_time(n_values, algorithm=algo_to_run)

    # Plot results
    plot_results(results, algo_to_run)

    # Plot worst-case times
    plot_worst_case(results, algo_to_run)
