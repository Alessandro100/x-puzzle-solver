import time
from queue import PriorityQueue
from xpuzzle import XPuzzle

## what to do next:
# clean up your code to fit the submission document
# timer

class UniformCost:
    def __init__(self, initial_state):
        print("class init")
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.goal_node = ()
        self.initial_state = initial_state

    def run(self):
        self.initialize_txt_files()
        start = time.time()
        goal_state = "1 2 3 4 5 6 7 0"
        self.set_state_open_list(self.initial_state, 0) # nodes that need to be visited (priority queue or dictionairy)

        print('start loop')
        self.close_list = {}
        while not self.open_list.empty():
            # finds the smallest cost path and visits it
            current_node = self.open_list.get()
            current_node_cost = current_node[0]
            current_node_key = current_node[1]
            current_node_prev_key = current_node[2]
            cost_of_current_move = current_node[3]
            tile_that_was_moved = current_node[4]

            if current_node_key not in self.close_list or self.close_list[current_node_key][0] > current_node_cost:
                self.close_list[current_node_key] = (current_node_cost, current_node_prev_key, cost_of_current_move, tile_that_was_moved)

                # writes search path to txt file
                with open("0_ucs_search.txt", "a") as ucs_search:
                    ucs_search.write("0 "+ str(current_node_cost) +" 0 " + current_node_key+"\n")
                
                # checks if goal state was reached
                if(current_node_key == goal_state):
                    self.goal_node = current_node
                    break

                # now we need to add the new nodes to the open list
                open_list = self.set_state_open_list(current_node_key, current_node_cost)

        end = time.time()
        print('I finished running in: ' + str(end - start) + " seconds")
        solution_array = self.get_algorithm_stats(str(end - start))

        if solution_array == -1:
            with open("0_ucs_search.txt", "a") as ucs_search:
                    ucs_search.write("No solution")
        else:
            with open("0_ucs_solution.txt", "a") as ucs_solution:
                    for line in solution_array:
                        ucs_solution.write(line+"\n")


    def normal_move_action_string(self, state, action):
        puzzle = XPuzzle(2,4, state)
        tile_moved = puzzle.regular_move(action)
        if( tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1

    def wrapping_move_action_string(self, state):
        puzzle = XPuzzle(2,4, state)
        tile_moved = puzzle.wrapping_move()
        if( tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1
    
    def diagonal_move_action_string(self, state, is_wrapping):
        puzzle = XPuzzle(2,4, state)
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

        wrapping_action = self.wrapping_move_action_string(current_state)
        if(wrapping_action != -1): self.open_list.put(((2 + base_amount), wrapping_action['key'], current_state, 2, wrapping_action['tile_moved']))

        diagonal_action = self.diagonal_move_action_string(current_state, False)
        if(diagonal_action != -1): self.open_list.put(((3 + base_amount), diagonal_action['key'], current_state, 3, diagonal_action['tile_moved'])) 

        diagonal_action_wrap = self.diagonal_move_action_string(current_state, True)
        if(diagonal_action_wrap != -1): self.open_list.put(((3 + base_amount), diagonal_action_wrap['key'], current_state, 3, diagonal_action['tile_moved'])) 

    def get_algorithm_stats(self, time):
        if(not self.goal_node):
            return -1
        else:
            print("COST: " + str(self.goal_node[0]))
            print("KEY: " + str(self.goal_node[1]))
            print("PREV: " + str(self.goal_node[2]))
            summ = "TIME: " + time + "s, COST: " + str(self.goal_node[0])
            order = [summ]
            previous_node = self.goal_node[1]
            print("GOAL NODE")
            print(previous_node)
            while(previous_node != self.initial_state):
                # 3 = tile moved, 2 = cost of move, 1 = previous move
                value = self.close_list[previous_node][3] + " " + str(self.close_list[previous_node][2]) +" "+ previous_node
                print(value)
                order.append(value)
                previous_node = self.close_list[previous_node][1]
            print("done!")
            return reversed(order)

    def initialize_txt_files(self):
        uniform_cost_search_file = open("0_ucs_search.txt", "w")
        uniform_cost_search_file.write("0 0 0 " + self.initial_state + "\n")
        uniform_cost_search_file.close()
        uniform_cost_solution_file = open("0_ucs_solution.txt", "w")
        uniform_cost_solution_file.write("0 0 " + self.initial_state + "\n")
        uniform_cost_solution_file.close()
                

#1 0 3 6 5 2 7 4
#6 3 4 7 1 2 5 0
#3 0 1 4 2 6 5 7
algo = UniformCost("3 0 1 4 2 6 5 7")
#algo = UniformCost("6 3 4 7 1 2 5 0")

algo.run()