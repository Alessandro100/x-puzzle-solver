from uniformCost import UniformCost
import random

class Analysis:
    def __init__(self):
        self.puzzles = []
        self.generare_random_puzzles()

    def generare_random_puzzles(self):
        for x in range(50):
            base_string = '12345670'
            mixed_string = ''.join(random.sample(base_string,len(base_string)))
            formatted_puzzle = " ".join(mixed_string)
            print(formatted_puzzle)
            self.puzzles.append(formatted_puzzle)

    def run_algos(self):
        count = 0
        uc_total_cost = 0
        uc_solutions_found = 0
        uc_total_execution_time = 0
        uc_total_solution_path_length = 0
        uc_total_search_path = 0

        for puzzle in self.puzzles:
            count += 1
            #        return {'total cost': total_cost, 'found_a_solution': found_goal, 'solution_path_length': solution_path_len, 'search_path_length': search_count, 'execution_time': str(end - start)}
            algo = UniformCost(puzzle,2, 4, count)
            stats = algo.run(False)

            if stats['total cost'] is not None:     
                uc_total_cost += stats['total cost']
                uc_solutions_found += 1
                uc_total_execution_time += stats['execution_time']
                uc_total_solution_path_length += stats['solution_path_length']
                uc_total_search_path += stats['search_path_length']

        print('uc_total_cost: ' + str(uc_total_cost) + " AVG: " + str(uc_total_cost / uc_solutions_found))
        print('uc_solutions_found: ' + str(uc_solutions_found))
        print('uc_total_execution_time: ' + str(uc_total_execution_time)+ " AVG: " + str(uc_total_execution_time / uc_solutions_found))
        print('uc_total_solution_path_length: ' + str(uc_total_solution_path_length)+ " AVG: " + str(uc_total_solution_path_length / uc_solutions_found))
        print('uc_total_search_path: ' + str(uc_total_search_path)+ " AVG: " + str(uc_total_search_path / uc_solutions_found))

a = Analysis()

a.run_algos()
            
            



