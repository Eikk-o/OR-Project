import os
from reader import read_capacity_matrix, read_capacity_and_cost_matrix, display_matrix
from min_cost_flow import min_cost_flow, bellman_ford, letter_to_index, build_node_map, index_to_letter, bellman
from push_relabel import push_relabel_trace, display_matrix

from ford_fulkerson import ford_fulkerson

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

                source_letter = input("Enter the source node (as a letter, e.g. 'a'): ").strip()
                target_letter = input("Enter the target node (as a letter, e.g. 'b'): ").strip()
                source_index = letter_to_index(source_letter, len(cap))
                target_index = letter_to_index(target_letter, len(cap))

                F = int(input("Enter the desired total flow (F): "))

                
                print(f"\nRunning Bellman algorithm (from '{source_letter}' to '{target_letter}')")
                distances, predecessors = bellman(cost, source_index)



                print(f"\nRunning Min Cost Flow algorithm (from '{source_letter}' to '{target_letter}', F = {F})")
                flow, total_cost = min_cost_flow(cap, cost, F, source_index, target_index)

                print(f"\n✅ Min-Cost Flow completed:\n   ➤ Total flow sent: {flow}\n   ➤ Total cost: {total_cost}")

            else:
                print("\nDetection: MAXIMAL FLOW problem.")
                cap = read_capacity_matrix(filepath)
                display_matrix(cap, "Capacity Matrix")

                while True:
                    print("\nChoose the algorithm to perform:")
                    print("1. Push-Relabel")
                    print("2. Ford-Fulkerson")
                    algorithm_choice = input("Enter the number of the algorithm (1 or 2): ")

                    if algorithm_choice == "1":
                        print("\nPush-Relabel algorithm result:")
                        max_flow, residual_graph = push_relabel_trace(cap, 0, len(cap) - 1)
    
                        print(f"\nMax Flow: {max_flow}")
                        print("\nResidual Graph after Push-Relabel:")
                        display_matrix(residual_graph, "Residual Matrix")
                        break
                    elif algorithm_choice == "2":
                        print("\nFord-Fulkerson algorithm trace:")
                        max_flow = ford_fulkerson(cap, source=0, sink=len(cap) - 1)
                        break
                    else:
                        print("❌ Invalid choice. Please enter 1 or 2.")

                print(f"\n✅ Maximum Flow: {max_flow}")

        except Exception as e:
            print(f"❌ Error during the analysis: {e}")

if __name__ == "__main__":
    main()
