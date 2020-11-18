from uniformCost import UniformCost
from a_star import AStar;
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
            #print(formatted_puzzle)
            self.puzzles.append(formatted_puzzle)

    def run_algos(self):
        # count = 0
        # uc_total_cost = 0
        # uc_solutions_found = 0
        # uc_total_execution_time = 0
        # uc_total_solution_path_length = 0
        # uc_total_search_path = 0

        # for puzzle in self.puzzles:
        #     count += 1
        #     #        return {'total cost': total_cost, 'found_a_solution': found_goal, 'solution_path_length': solution_path_len, 'search_path_length': search_count, 'execution_time': str(end - start)}
        #     algo = UniformCost(puzzle,2, 4, count)
        #     stats = algo.run(False)

        #     if stats['total cost'] is not None:     
        #         uc_total_cost += stats['total cost']
        #         uc_solutions_found += 1
        #         uc_total_execution_time += stats['execution_time']
        #         uc_total_solution_path_length += stats['solution_path_length']
        #         uc_total_search_path += stats['search_path_length']

        # print('uc_total_cost: ' + str(uc_total_cost) + " AVG: " + str(uc_total_cost / uc_solutions_found))
        # print('uc_solutions_found: ' + str(uc_solutions_found))
        # print('uc_total_execution_time: ' + str(uc_total_execution_time)+ " AVG: " + str(uc_total_execution_time / uc_solutions_found))
        # print('uc_total_solution_path_length: ' + str(uc_total_solution_path_length)+ " AVG: " + str(uc_total_solution_path_length / uc_solutions_found))
        # print('uc_total_search_path: ' + str(uc_total_search_path)+ " AVG: " + str(uc_total_search_path / uc_solutions_found))

        count = 0
        analysis_as = {"h1":{"as_total_cost": 0, "as_solutions_found": 0, "as_total_execution_time": 0, "as_total_solution_path_length": 0, "as_total_search_path": 0},"h2":{"as_total_cost": 0, "as_solutions_found": 0, "as_total_execution_time": 0, "as_total_solution_path_length": 0, "as_total_search_path": 0}}
        
        for puzzle in self.puzzles:
            count += 1
            print("Puzzle",count)
            algo = AStar(puzzle,2, 4)
            stats = algo.run_algo()
            print("")

            for h, stat in stats.items():
                if stat['total cost'] is not None:     
                    analysis_as[h]["as_total_cost"] += stat['total cost']
                    analysis_as[h]["as_solutions_found"] += 1
                    analysis_as[h]["as_total_execution_time"] += stat['execution_time']
                    analysis_as[h]["as_total_solution_path_length"] += stat['solution_path_length']
                    analysis_as[h]["as_total_search_path"] += stat['search_path_length']

        for h, analysis in analysis_as.items():
            print(h + " " + 'as_total_cost: ' + str(analysis["as_total_cost"]) + " AVG: " + str(analysis["as_total_cost"] / analysis["as_solutions_found"]))
            print(h + " " +' as_solutions_found: ' + str(analysis["as_solutions_found"]))
            print(h + " " + 'as_total_execution_time: ' + str(analysis["as_total_execution_time"])+ " AVG: " + str(analysis["as_total_execution_time"] / analysis["as_solutions_found"]))
            print(h + " " + 'as_total_solution_path_length: ' + str(analysis["as_total_solution_path_length"])+ " AVG: " + str(analysis["as_total_solution_path_length"] / analysis["as_solutions_found"]))
            print(h + " " + 'as_total_search_path: ' + str(analysis["as_total_search_path"])+ " AVG: " + str(analysis["as_total_search_path"] / analysis["as_solutions_found"]))

a = Analysis()
a.run_algos()
            
            



