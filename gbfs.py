import time
from queue import PriorityQueue
from xpuzzle import XPuzzle
import numpy as np

class GreedyBestFirstSearch:
    def __init__(self, initial_state, rows, cols, id):
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.goal_node = ()
        self.initial_state = initial_state
        self.rows = rows
        self.cols = cols
        self.id = str(id)

    def run(self):
        print('start algo for: ' + self.initial_state)
        self.initialize_txt_files()
        start = time.time()
        goal_state_1 = self.calculate_goal_state_1()
        goal_state_2 = self.calculate_goal_state_2()
        # nodes that need to be visited (priority queue or dictionairy)
        self.set_state_open_list(self.initial_state, 0)
        self.close_list = {}
        while (not self.open_list.empty()):
            if (time.time() - start > 60):
                        break
            # finds the smallest cost path and visits it
            current_node = self.open_list.get()
            current_node_cost = current_node[0]
            current_node_key = current_node[1]
            current_node_prev_key = current_node[2]
            cost_of_current_move = current_node[3]
            tile_that_was_moved = current_node[4]
            total_path_cost = current_node[5]

            if current_node_key not in self.close_list:
                self.close_list[current_node_key] = (
                    current_node_cost, current_node_prev_key, cost_of_current_move, tile_that_was_moved)

                # writes search path to txt file
                with open(self.id + "_gbfs_h0_search.txt", "a") as gbfs_search:
                    gbfs_search.write(
                        self.id + " " + str(total_path_cost) + " 0 " + current_node_key+"\n")

                # checks if goal state was reached
                if(current_node_key == goal_state_1 or current_node_key == goal_state_2):
                    self.goal_node = current_node
                    break

                # now we need to add the new nodes to the open list
                open_list = self.set_state_open_list(
                    current_node_key, total_path_cost)

        end = time.time()
        print('I finished running in: ' + str(end - start) + " seconds")
        solution_array = self.get_algorithm_stats(str(end - start))

        if solution_array == -1:
            with open(self.id+"_gbfs_h0_search.txt", "a") as gbfs_search:
                gbfs_search.write("No solution")
        else:
            with open(self.id+"_gbfs_h0_solution.txt", "a") as gbfs_solution:
                for line in solution_array:
                    gbfs_solution.write(line+"\n")

    def normal_move_action_string(self, state, action):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.regular_move(action)
        if(tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1

    def wrapping_move_action_string(self, state, wrap_col=False):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.wrapping_move(wrap_col)
        if(tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1

    def diagonal_move_action_string(self, state, is_wrapping):
        puzzle = XPuzzle(self.rows, self.cols, state)
        tile_moved = puzzle.diagonal_move(is_wrapping)
        if(tile_moved != -1):
            return {'key': puzzle.current_state_to_string(), 'tile_moved': tile_moved}
        else:
            return -1

    def set_state_open_list(self, current_state, base_amount):
        # 1 cost actions: up, down, left, right
        # 2 cost actions: wrapping_move
        # 3 cost actions: diagonal_move, diagonal_move(wrap)
        # total of 8 actions

        # up_action = self.normal_move_action_string(current_state, "up") ## THIS IS THE POTENTIAL NEXT STATE
        # if(up_action != -1): self.open_list.put((HEURISTIC(UP_ACTION['KEY']), up_action['key'], current_state, 1, up_action['tile_moved']))

       # open list = (heuristic-choice,total cost, current_key, previous_key, cost, tile_moved, cumulative cost)
        up_action = self.normal_move_action_string(current_state, "up")
        if(up_action != -1): self.open_list.put(((self.heuristic_0(
            up_action['key'])), up_action['key'], current_state, 1, up_action['tile_moved'], (1 + base_amount)))

        down_action = self.normal_move_action_string(current_state, "down")
        if(down_action != -1): self.open_list.put(((self.heuristic_0(
            down_action['key'])), down_action['key'], current_state, 1, down_action['tile_moved'], (1 + base_amount)))

        left_action = self.normal_move_action_string(current_state, "left")
        if(left_action != -1): self.open_list.put(((self.heuristic_0(
            left_action['key'])), left_action['key'], current_state, 1, left_action['tile_moved'], (1 + base_amount)))

        right_action = self.normal_move_action_string(current_state, "right")
        if(right_action != -1): self.open_list.put(((self.heuristic_0(
            right_action['key'])), right_action['key'], current_state, 1, right_action['tile_moved'], (1 + base_amount)))

        wrapping_action = self.wrapping_move_action_string(
            current_state, False)
        if(wrapping_action != -1): self.open_list.put(((self.heuristic_0(
            wrapping_action['key'])), wrapping_action['key'], current_state, 2, wrapping_action['tile_moved'], (2 + base_amount)))

        diagonal_action = self.diagonal_move_action_string(
            current_state, False)
        if(diagonal_action != -1): self.open_list.put(((self.heuristic_0(
            diagonal_action['key'])), diagonal_action['key'], current_state, 3, diagonal_action['tile_moved'], (3 + base_amount)))

        diagonal_action_wrap = self.diagonal_move_action_string(
            current_state, True)
        if(diagonal_action_wrap != -1): self.open_list.put(((self.heuristic_0(
            diagonal_action_wrap['key'])), diagonal_action_wrap['key'], current_state, 3, diagonal_action['tile_moved'], (3 + base_amount)))

        if self.rows > 2:
            wrapping_action_col = self.wrapping_move_action_string(
                current_state, True)
            if(wrapping_action_col != -1): self.open_list.put(((self.heuristic_0(
                wrapping_action_col['key'])), wrapping_action_col['key'], current_state, 2, wrapping_action_col['tile_moved'], (2 + base_amount)))

# for h0 - given heuristics -checks if 0 is in the right place
    def heuristic_0(self, state):
        if state[len(state)-1] == "0":
            return 0
        else: return 1


# for h1 - hamming distance

    def heuristic_1(self, state):
        goal_state_1 = self.calculate_goal_state_1()
        goal_state_2 = self.calculate_goal_state_2()
        return (min(self.hamming_distance_goal_1(state, goal_state_1),
                    self.hamming_distance_goal_2(state, goal_state_2)))
# for h1 - hamming distance

    def hamming_distance_goal_1(self, state, goal_state1):
        ham1 = 0
        for x in range(len(state)):
            if goal_state1[x] != state[x]:
                ham1 += 1
        return ham1
# for h1 - hamming distance

    def hamming_distance_goal_2(self, state, goal_state2):
        ham2 = 0
        for x in range(len(state)):
            if goal_state2[x] != state[x]:
                ham2 += 1
        return ham2

# for h2 - manhattan distance
    def heuristic_2(self, successor_state):
        manhattan_distances = []
        
        for index, goal_state in enumerate([self.calculate_goal_state_1(), self.calculate_goal_state_2()]):
            temp_successor_state = successor_state
            goal_state = goal_state.split(" ")
            np_goal = np.reshape(goal_state, (self.cols, self.rows))
            temp_successor_state = temp_successor_state.split(" ")
            np_succ = np.reshape(temp_successor_state, (self.cols, self.rows))
            manhattan_distances.append(0)
            
            for i in range(self.cols * self.rows):
                beg = np.where(np_succ == str(i))
                np.shape(beg)
                beg_row = beg[0][0]
                beg_col = beg[1][0]

                dest = np.where(np_goal == str(i))
                dest_row = dest[0][0]
                dest_col = dest[1][0]

                dist = abs(dest_row - beg_row) + abs(dest_col - beg_col)
                manhattan_distances[index] += dist
        return min(manhattan_distances)
    
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

    def get_algorithm_stats(self, time):
        if(not self.goal_node):
            print('no goal state found')
            return -1
        else:
            summ = "TIME: " + time + "s, COST: " + str(self.goal_node[5])
            order = [summ]
            previous_node = self.goal_node[1]
            print("Found Goal Node")
            print(summ)
            while(previous_node != self.initial_state):
                # 3 = tile moved, 2 = cost of move, 1 = previous move
                value = str(self.close_list[previous_node][3]) + " " + str(
                    self.close_list[previous_node][2]) + " " + str(previous_node)
                order.append(value)
                previous_node = self.close_list[previous_node][1]
            return reversed(order)

    def initialize_txt_files(self):
        uniform_cost_search_file = open(self.id+"_gbfs_h0_search.txt", "w")
        uniform_cost_search_file.write("0 0 0 " + self.initial_state + "\n")
        uniform_cost_search_file.close()
        uniform_cost_solution_file = open(self.id+"_gbfs_h0_solution.txt", "w")
        uniform_cost_solution_file.write("0 0 " + self.initial_state + "\n")
        uniform_cost_solution_file.close()

    


algo1 = GreedyBestFirstSearch("1 0 3 6 5 2 7 4", 2, 4, 0)
algo2 = GreedyBestFirstSearch("6 3 4 7 1 2 5 0", 2, 4, 1)
algo3 = GreedyBestFirstSearch("3 0 1 4 2 6 5 7", 2, 4, 2)
algo4 = GreedyBestFirstSearch("1 2 3 4 0 5 6 7 8 9 10 11", 3, 4, 3)

algo1.run()
algo2.run()
algo3.run()
algo4.run()
