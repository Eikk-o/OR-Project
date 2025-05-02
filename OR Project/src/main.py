import os
from reader import read_capacity_matrix, read_capacity_and_cost_matrix, display_matrix
from min_cost_flow import bellman_ford 
from push_relabel import push_relabel

PROPOSAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'proposals')

def is_min_cost_problem(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            try:
                n = int(lines[0].strip())
                return len(lines) == 1 + 2 * n
            except ValueError:
                return False
    return False

def main():
    print("==== Project Operation Research ====")
    while True:
        filename = input("Please enter the proposal number (1-10) or 'q' to quit: ")
        if filename.lower() == 'q':
            break

        full_filename = f"proposal_{filename}.txt"
        filepath = os.path.join(PROPOSAL_DIR, full_filename)

        if not os.path.exists(filepath):
            print("❌ File not found. Please verify the number.")
            continue

        try:
            if is_min_cost_problem(filepath):
                print("\nDetection: MINIMAL COST FLOW problem.")
                cap, cost = read_capacity_and_cost_matrix(filepath)
                display_matrix(cap, "Capacity Matrix")
                display_matrix(cost, "Cost Matrix")

                print("\nBellman-Ford algorithm trace (source node = 0):")
                bellman_ford(cap, cost, source=0)

            else:
                print("\nDetection: MAXIMAL FLOW problem.")
                cap = read_capacity_matrix(filepath)
                display_matrix(cap, "Capacity Matrix")

                while True:
                    print("\nChoose the algorithm to perform:")
                    print("1. Push-Relabel")
                    print("2. FF")
                    algorithm_choice = input("Enter the number of the algorithm (1 or 2): ")

                    if algorithm_choice == "1":
                        print("\nPush-Relabel algorithm result:")
                        max_flow = push_relabel(cap, 0, len(cap) - 1)
                        break
                    elif algorithm_choice == "2":
                        print("\nEdmonds-Karp algorithm result:")
                        # max_flow = ff(cap, source, sink)
                        max_flow = 0  # Placeholder for the actual FF algorithm implementation
                        break
                    else:
                        print("❌ Invalid choice. Please enter 1 or 2.")
                print(f"Maximum Flow: {max_flow}")

        except Exception as e:
            print(f"❌ Error during the analysis: {e}")

if __name__ == "__main__":
    main()
