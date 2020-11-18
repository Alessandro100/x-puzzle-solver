from uniformCost import UniformCost
from gbfs import GreedyBestFirstSearch
from a_star import AStar;
import random

class Analysis:
    def __init__(self):
        self.puzzles = []
        self.generare_random_puzzles()
        analysis_output_file = open("analysis_output_file.txt", "w")
        analysis_output_file.write("Algo Analysis \n")
        analysis_output_file.close()

    def generare_random_puzzles(self):
        for x in range(50):
            base_string = '12345670'
            mixed_string = ''.join(random.sample(base_string,len(base_string)))
            formatted_puzzle = " ".join(mixed_string)
            self.puzzles.append(formatted_puzzle)

    def uniform_cost_analysis(self):
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

        cost = 'uc_total_cost: ' + str(uc_total_cost) + " AVG: " + str(uc_total_cost / uc_solutions_found)
        solution_found = 'uc_solutions_found: ' + str(uc_solutions_found)
        exe = 'uc_total_execution_time: ' + str(uc_total_execution_time)+ " AVG: " + str(uc_total_execution_time / uc_solutions_found)
        path = 'uc_total_solution_path_length: ' + str(uc_total_solution_path_length)+ " AVG: " + str(uc_total_solution_path_length / uc_solutions_found)
        path2 = 'uc_total_search_path: ' + str(uc_total_search_path)+ " AVG: " + str(uc_total_search_path / uc_solutions_found)
        print(cost)
        print(solution_found)
        print(exe)
        print(path)
        print(path2)
        with open("analysis_output_file.txt", "a") as analysis_output:
            analysis_output.write("#### Uniform Cost #### \n")
            analysis_output.write(cost + "\n")
            analysis_output.write(solution_found + "\n")
            analysis_output.write(exe + "\n")
            analysis_output.write(path + "\n")
            analysis_output.write(path2 + "\n")
        

    def a_star_analysis(self):
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

        with open("analysis_output_file.txt", "a") as analysis_output:
            analysis_output.write("#### A* ####")
        for h, analysis in analysis_as.items():
            print(h + " " + 'as_total_cost: ' + str(analysis["as_total_cost"]) + " AVG: " + str(analysis["as_total_cost"] / analysis["as_solutions_found"]))
            print(h + " " +' as_solutions_found: ' + str(analysis["as_solutions_found"]))
            print(h + " " + 'as_total_execution_time: ' + str(analysis["as_total_execution_time"])+ " AVG: " + str(analysis["as_total_execution_time"] / analysis["as_solutions_found"]))
            print(h + " " + 'as_total_solution_path_length: ' + str(analysis["as_total_solution_path_length"])+ " AVG: " + str(analysis["as_total_solution_path_length"] / analysis["as_solutions_found"]))
            print(h + " " + 'as_total_search_path: ' + str(analysis["as_total_search_path"])+ " AVG: " + str(analysis["as_total_search_path"] / analysis["as_solutions_found"]))
            with open("analysis_output_file.txt", "a") as analysis_output:
                analysis_output.write(h + " " + 'as_total_cost: ' + str(analysis["as_total_cost"]) + " AVG: " + str(analysis["as_total_cost"] / analysis["as_solutions_found"]) + "\n")
                analysis_output.write(h + " " +' as_solutions_found: ' + str(analysis["as_solutions_found"]) + "\n")
                analysis_output.write(h + " " + 'as_total_execution_time: ' + str(analysis["as_total_execution_time"])+ " AVG: " + str(analysis["as_total_execution_time"] / analysis["as_solutions_found"]) + "\n")
                analysis_output.write(h + " " + 'as_total_solution_path_length: ' + str(analysis["as_total_solution_path_length"])+ " AVG: " + str(analysis["as_total_solution_path_length"] / analysis["as_solutions_found"]) + "\n")
                analysis_output.write(h + " " + 'as_total_search_path: ' + str(analysis["as_total_search_path"])+ " AVG: " + str(analysis["as_total_search_path"] / analysis["as_solutions_found"]) + "\n")

    def gbfs_analysis(self):
        count = 0
        gbfs_total_cost = 0
        gbfs_solutions_found = 0
        gbfs_total_execution_time = 0
        gbfs_total_solution_path_length = 0
        gbfs_total_search_path = 0

        for puzzle in self.puzzles:
            count += 1
            #return {'total cost': total_cost, 'found_a_solution': found_goal, 'solution_path_length': solution_path_len, 'search_path_length': search_count, 'execution_time': str(end - start)}
            algo = GreedyBestFirstSearch(puzzle,2, 4, count)
            stats = algo.run(True)

            if stats['total cost'] is not None:     
                gbfs_total_cost += stats['total cost']
                gbfs_solutions_found += 1
                gbfs_total_execution_time += stats['execution_time']
                gbfs_total_solution_path_length += stats['solution_path_length']
                gbfs_total_search_path += stats['search_path_length']

        print('gbfs_total_cost: ' + str(gbfs_total_cost) + " AVG: " + str(gbfs_total_cost / gbfs_solutions_found))
        print('gbfs_solutions_found: ' + str(gbfs_solutions_found))
        print('gbfs_total_execution_time: ' + str(gbfs_total_execution_time)+ " AVG: " + str(gbfs_total_execution_time / gbfs_solutions_found))
        print('gbfs_total_solution_path_length: ' + str(gbfs_total_solution_path_length)+ " AVG: " + str(gbfs_total_solution_path_length / gbfs_solutions_found))
        print('gbfs_total_search_path: ' + str(gbfs_total_search_path)+ " AVG: " + str(gbfs_total_search_path / gbfs_solutions_found))

        count = 0
        analysis_as = {"h1":{"gbsf_total_cost": 0, "gbfs_solutions_found": 0, "gbfs_total_execution_time": 0, "gbfs_total_solution_path_length": 0, "gbfs_total_search_path": 0},"h2":{"gbfs_total_cost": 0, "gbfs_solutions_found": 0, "gbfs_total_execution_time": 0, "gbfs_total_solution_path_length": 0, "gbfs_total_search_path": 0}}
        with open("analysis_output_file.txt", "a") as analysis_output:
            analysis_output.write("#### Greedy Best First Search #### \n")
            analysis_output.write('gbfs_total_cost: ' + str(gbfs_total_cost) + " AVG: " + str(gbfs_total_cost / gbfs_solutions_found) + "\n")
            analysis_output.write('gbfs_solutions_found: ' + str(gbfs_solutions_found) + "\n")
            analysis_output.write('gbfs_total_execution_time: ' + str(gbfs_total_execution_time)+ " AVG: " + str(gbfs_total_execution_time / gbfs_solutions_found) + "\n")
            analysis_output.write('gbfs_total_solution_path_length: ' + str(gbfs_total_solution_path_length)+ " AVG: " + str(gbfs_total_solution_path_length / gbfs_solutions_found) + "\n")
            analysis_output.write('gbfs_total_search_path: ' + str(gbfs_total_search_path)+ " AVG: " + str(gbfs_total_search_path / gbfs_solutions_found) + "\n")

    def run_algos(self):
        self.uniform_cost_analysis()
        self.a_star_analysis()
        self.gbfs_analysis()
        with open("analysis_output_file.txt", "a") as analysis_output:
                analysis_output.write("#### These are the Puzzles #### \n")
        for puzzle in self.puzzles:
            with open("analysis_output_file.txt", "a") as analysis_output:
                analysis_output.write(puzzle + "\n")


a = Analysis()
a.run_algos()
            
            



