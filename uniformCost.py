import time
from queue import PriorityQueue
from xpuzzle import XPuzzle

## what to do next:
# clean up your code to fit the submission document
# timer

class UniformCost:
    def __init__(self, initial_state, rows, cols, id):
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.goal_node = ()
        self.initial_state = initial_state
        self.rows = rows
        self.cols = cols
        self.id = str(id)

    def run(self, log_result_to_csv = False):
        print('start algo for: ' + self.initial_state)
        if log_result_to_csv:
            self.initialize_txt_files()
        search_count = 0
        start = time.time()
        found_goal = False
        goal_state_1 = self.calculate_goal_state_1()
        goal_state_2 = self.calculate_goal_state_2()
        self.set_state_open_list(self.initial_state, 0) # nodes that need to be visited (priority queue or dictionairy)
        self.close_list = {}
        while not self.open_list.empty():
            # finds the smallest cost path and visits it
            current_node = self.open_list.get()
            current_node_cost = current_node[0]
            current_node_key = current_node[1]
            current_node_prev_key = current_node[2]
            cost_of_current_move = current_node[3]
            tile_that_was_moved = current_node[4]
            search_count += 1

            if current_node_key not in self.close_list or self.close_list[current_node_key][0] > current_node_cost:
                self.close_list[current_node_key] = (current_node_cost, current_node_prev_key, cost_of_current_move, tile_that_was_moved)

                # writes search path to txt file
                if log_result_to_csv:
                    with open(self.id + "_ucs_search.txt", "a") as ucs_search:
                        ucs_search.write(self.id + " " + str(current_node_cost) +" 0 " + current_node_key+"\n")
                
                # checks if goal state was reached
                if(current_node_key == goal_state_1 or current_node_key == goal_state_2):
                    self.goal_node = current_node
                    found_goal = True
                    break

                # now we need to add the new nodes to the open list
                open_list = self.set_state_open_list(current_node_key, current_node_cost)

        end = time.time()
        print('I finished running in: ' + str(end - start) + " seconds")
        solution_array = self.get_algorithm_stats(str(end - start))

        if log_result_to_csv:
            if solution_array == -1:
                with open(self.id+"_ucs_search.txt", "a") as ucs_search:
                        ucs_search.write("No solution")
            else:
                with open(self.id+"_ucs_solution.txt", "a") as ucs_solution:
                        for line in solution_array:
                            ucs_solution.write(line+"\n")

        total_cost = self.goal_node[0] if found_goal else None
        solution_path_len = len(list(solution_array)) - 1
        return {'total cost': total_cost, 'found_a_solution': found_goal, 'solution_path_length': solution_path_len, 'search_path_length': search_count, 'execution_time': (end - start)}


    def normal_move_action_string(self, state, action):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.regular_move(action)
        if( tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1

    def wrapping_move_action_string(self, state, wrap_col = False):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.wrapping_move(wrap_col)
        if( tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1
    
    def diagonal_move_action_string(self, state, is_wrapping):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.diagonal_move(is_wrapping)
        if( tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1
    
    def set_state_open_list(self, current_state, base_amount):
        # 1 cost actions: up, down, left, right
        # 2 cost actions: wrapping_move
        # 3 cost actions: diagonal_move, diagonal_move(wrap)
        # total of 7 actions

        # open list = (total_cost, current_key, previous_key, cost, tile_moved)
        up_action = self.normal_move_action_string(current_state, "up")
        if(up_action != -1): self.open_list.put(((1 + base_amount), up_action['key'], current_state, 1, up_action['tile_moved']))

        down_action = self.normal_move_action_string(current_state, "down")
        if(down_action != -1): self.open_list.put(((1 + base_amount), down_action['key'], current_state, 1, down_action['tile_moved']))

        left_action = self.normal_move_action_string(current_state, "left")
        if(left_action != -1): self.open_list.put(((1 + base_amount), left_action['key'], current_state, 1, left_action['tile_moved']))

        right_action = self.normal_move_action_string(current_state, "right")
        if(right_action != -1): self.open_list.put(((1 + base_amount), right_action['key'], current_state, 1, right_action['tile_moved']))

        wrapping_action = self.wrapping_move_action_string(current_state, False)
        if(wrapping_action != -1): self.open_list.put(((2 + base_amount), wrapping_action['key'], current_state, 2, wrapping_action['tile_moved']))

        diagonal_action = self.diagonal_move_action_string(current_state, False)
        if(diagonal_action != -1): self.open_list.put(((3 + base_amount), diagonal_action['key'], current_state, 3, diagonal_action['tile_moved'])) 

        diagonal_action_wrap = self.diagonal_move_action_string(current_state, True)
        if(diagonal_action_wrap != -1): self.open_list.put(((3 + base_amount), diagonal_action_wrap['key'], current_state, 3, diagonal_action['tile_moved']))

        if self.rows > 2:
            wrapping_action_col = self.wrapping_move_action_string(current_state, True)
            if(wrapping_action_col != -1): self.open_list.put(((2 + base_amount), wrapping_action_col['key'], current_state, 2, wrapping_action_col['tile_moved']))

    def get_algorithm_stats(self, time):
        if(not self.goal_node):
            print('no goal state found')
            return -1
        else:
            summ = "TIME: " + time + "s, COST: " + str(self.goal_node[0])
            order = [summ]
            previous_node = self.goal_node[1]
            print("Found Goal Node")
            print(summ)
            while(previous_node != self.initial_state):
                # 3 = tile moved, 2 = cost of move, 1 = previous move
                value = str(self.close_list[previous_node][3]) + " " + str(self.close_list[previous_node][2]) +" "+ str(previous_node)
                order.append(value)
                previous_node = self.close_list[previous_node][1]
            return reversed(order)

    def initialize_txt_files(self):
        uniform_cost_search_file = open(self.id+"_ucs_search.txt", "w")
        uniform_cost_search_file.write("0 0 0 " + self.initial_state + "\n")
        uniform_cost_search_file.close()
        uniform_cost_solution_file = open(self.id+"_ucs_solution.txt", "w")
        uniform_cost_solution_file.write("0 0 " + self.initial_state + "\n")
        uniform_cost_solution_file.close()

    def calculate_goal_state_1(self):
        goal_string = ''
        for i in range((self.cols * self.rows) - 1):
            goal_string += str(i + 1) + ' '
        goal_string += '0'
        return goal_string
    
    def calculate_goal_state_2(self):
        goal_string = ''
        even = ''
        odd = ''
        for i in range((self.cols * self.rows) - 1):
            if((i + 1) % 2 == 0):
               even += str(i + 1) + " "
            else:
                odd += str(i + 1) + " "
        goal_string = odd + even + "0"
        return goal_string
                

#1 0 3 6 5 2 7 4
#6 3 4 7 1 2 5 0
#3 0 1 4 2 6 5 7
algo1 = UniformCost("1 0 3 6 5 2 7 4", 2, 4, 0)
algo2 = UniformCost("6 3 4 7 1 2 5 0", 2, 4, 1)
algo3 = UniformCost("3 0 1 4 2 6 5 7", 2, 4, 2)
algo4 = UniformCost("1 2 3 4 0 5 6 7 8 9 10 11", 3, 4, 3)

algo1.run()
algo2.run()
algo3.run()
algo4.run()