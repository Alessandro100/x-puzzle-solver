from xpuzzle import XPuzzle
from queue import PriorityQueue
import copy
import numpy as np
import ctypes
import time

class AStar: 
    #def __init__(self, filename, rows, columns):
    def __init__(self, puzzle, rows, columns):
        #self.read_input_file(filename)
        self.inputs = [puzzle]
        self.goal_state1 = [['1', '2', '3', '4',],['5', '6', '7', '0']]
        self.goal_state2 = [['1', '3', '5', '7'],['2','4','6','0']]
        #self.heuristics = ['h1', 'h2', 'h0']
        self.heuristics = ['h1', 'h2']
        self.heuristic = ''
        self.rows = 2
        self.columns = 4
        self.puzzle = XPuzzle(self.rows, self.columns, puzzle)
        #self.goal_state1 = [['1', '2', '3', '4',],['5', '6', '7', '8'],['9','10','11','0']]
        #self.goal_state2 = [['1', '4', '7', '10'],['2','5','8','11'],['3','6','9','0']]
        self.analysis = {}
    
    def reset(self, initial_state):
        self.close_list = PriorityQueue()
        self.open_list = PriorityQueue()
        self.puzzle = XPuzzle(self.rows, self.columns, initial_state)
        self.initial_state = (0,copy.deepcopy(self.puzzle.arr),0,0,0,0, None, 0)
        self.is_goal_state = False
        self.ignore_move = ''
        self.search_space = {}

    def read_input_file(self, filename):
        with open(filename) as f:
            self.inputs = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        self.inputs = [x.strip() for x in self.inputs]
        #print(self.inputs)

    def add_to_search(self, successor_state):
        if (not repr(successor_state[1]) in self.search_space):
            self.search_space[repr(successor_state[1])] = str(successor_state[0]) + " " + str(successor_state[5]) + " " + str(successor_state[4]) + " " + str(self.stringify_state(successor_state[1]))        

    def add_successors_to_open_list(self, state):
        #print("current zero", self.puzzle.zero_position)
        valid_moves = self.puzzle.find_valid_moves()

        for move in valid_moves:
            if move == self.ignore_move:
                continue
            successor, cost, tile_changed = self.swap(copy.deepcopy(state[1]), move, self.puzzle.zero_position)
            
            g_n = state[5] + cost
            #choose heuristic
            h_n = 0
            if (self.heuristic == 'h1'):
                h_n = self.get_hamming_distance(successor)
            elif (self.heuristic == 'h2'):
                h_n = self.get_manhattan_distance(successor)
            elif (self.heuristic == 'h0'):
                h_n = self.get_h0(successor)
            f_n = h_n + g_n

            successor_state = (f_n, successor, move, cost, h_n, g_n, state, tile_changed)
            self.add_to_search(successor_state)

            temp_state = successor_state[1]

            #check if exists in closed list
            new_close_list = PriorityQueue()
            place_in_open = False
            for s in self.close_list.queue:
                if temp_state == s[1]:
                    if successor_state[0] < s[0]:
                        self.open_list.put(successor_state)
                        place_in_open = True
                        #print('better closed')
                else:
                    new_close_list.put(s)
            self.close_list = new_close_list
            if place_in_open:
                continue

            #check if exists in open list
            new_open_list = PriorityQueue()
            replaced = False
            for s in self.open_list.queue:
                if temp_state == s[1]:
                    if successor_state[0] < s[0]:
                        new_open_list.put(successor_state)
                        replaced = True
                        #print('better open')
                else:
                    new_open_list.put(s)
            self.open_list = new_open_list
            if replaced:
                continue

            # if its not already in open or closed then simply add into openlist
            self.open_list.put(successor_state)

    def swap(self, state, move, zero_position):
        zero0, zero1 = zero_position[0], zero_position[1]
        if (move == 'up'):
            state[zero0][zero1] = state[zero0-1][zero1]
            state[zero0-1][zero1] = '0'
            cost = 1
            tile_changed = state[zero0][zero1]
        elif (move == 'down'):
            state[zero0][zero1] = state[zero0+1][zero1]
            state[zero0+1][zero1] = '0'
            cost = 1
            tile_changed = state[zero0][zero1]
        elif (move == 'left'):
            state[zero0][zero1] = state[zero0][zero1 - 1]
            state[zero0][zero1 - 1] = '0'
            cost = 1
            tile_changed = state[zero0][zero1]
        elif (move == 'right'):
            state[zero0][zero1] = state[zero0][zero1 + 1]
            state[zero0][zero1 + 1] = '0'
            cost = 1
            tile_changed = state[zero0][zero1]
        elif (move == 'top_left_wrap'):
            state[zero0][zero1] = state[zero0][-1]
            state[zero0][-1] = '0'
            cost = 2
            tile_changed = state[zero0][zero1]
        elif (move == 'top_right_wrap'):
            state[zero0][zero1] = state[zero0][0]
            state[zero0][0] = '0'
            cost = 2
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_left_wrap'):
            state[zero0][zero1] = state[zero0][-1]
            state[zero0][-1] = '0'
            cost = 2
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_right_wrap'):
            state[zero0][zero1] = state[zero0][0]
            state[zero0][0] = '0'
            cost = 2
            tile_changed = state[zero0][zero1]
        elif (move == 'top_left_diagonal_wrap'):
            state[zero0][zero1] = state[-1][-1]
            state[-1][-1] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'top_right_diagonal_wrap'):
            state[zero0][zero1] = state[-1][0]
            state[-1][0] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_left_diagonal_wrap'):
            state[zero0][zero1] = state[0][-1]
            state[0][-1] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_right_diagonal_wrap'):
            state[zero0][zero1] = state[0][0]
            state[0][0] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'top_left_diagonal_adjacent'):
            state[zero0][zero1] = state[zero0+1][zero1+1]
            state[zero0+1][zero1+1] = '0' 
            cost = 3 
            tile_changed = state[zero0][zero1]
        elif (move == 'top_right_diagonal_adjacent'):
            state[zero0][zero1] = state[zero0+1][zero1-1]
            state[zero0+1][zero1-1] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_left_diagonal_adjacent'):
            state[zero0][zero1] = state[zero0-1][zero1+1]
            state[zero0-1][zero1+1] = '0'
            cost = 3
            tile_changed = state[zero0][zero1]
        elif (move == 'bottom_right_diagonal_adjacent'):
            state[zero0][zero1] = state[zero0-1][zero1-1]
            state[zero0-1][zero1-1] = '0' 
            cost = 3
            tile_changed = state[zero0][zero1]
        return state, cost, tile_changed

    def ensure_ignore(self, move):
        if (move == 'up'):
            self.ignore_move = 'down'
        elif (move == 'down'):
            self.ignore_move = 'up'
        elif (move == 'left'):
            self.ignore_move = 'right'
        elif (move == 'right'):
            self.ignore_move = 'left'
        elif (move == 'top_left_wrap'):
            self.ignore_move = 'top_right_wrap'
        elif (move == 'top_right_wrap'):
            self.ignore_move = 'top_left_wrap'
        elif (move == 'bottom_left_wrap'):
            self.ignore_move = 'bottom_right_wrap'
        elif (move == 'bottom_right_wrap'):
            self.ignore_move = 'bottom_left_wrap'
        elif (move == 'top_left_diagonal_wrap'):
            self.ignore_move = 'bottom_right_diagonal_wrap'
        elif (move == 'top_right_diagonal_wrap'):
            self.ignore_move = 'bottom_left_diagonal_wrap'
        elif (move == 'bottom_left_diagonal_wrap'):
            self.ignore_move = 'top_right_diagonal_wrap'
        elif (move == 'bottom_right_diagonal_wrap'):
            self.ignore_move = 'top_left_diagonal_wrap'

    def update_zero_position(self, chosen_state):
        s = np.array(chosen_state[1])
        s = np.where(s == '0')
        self.puzzle.zero_position = (s[0][0], s[1][0])

    #h0
    def get_h0(self, successor_state):
        return 0 if successor_state[-1][-1] == '0' else 1
    #h1
    def get_hamming_distance(self, successor_state):
        hamming_distances = []
        for index, goal_state in enumerate([self.goal_state1, self.goal_state2]):
            np_goal = np.asarray(goal_state).astype(np.int)
            np_succ = np.asarray(successor_state).astype(np.int)
            hamming_distances.append(np.count_nonzero(np_goal - np_succ))
        return min(hamming_distances)

    #h2
    def get_manhattan_distance(self, successor_state):
        manhattan_distances = []
        for index, goal_state in enumerate([self.goal_state1, self.goal_state2]):
            np_goal = np.asarray(goal_state)
            np_succ = np.asarray(successor_state)
            manhattan_distances.append(0)
            for i in range(self.puzzle.cols * self.puzzle.rows):
                beg = np.where(np_succ == str(i))
                beg_row = beg[0][0]
                beg_col = beg[1][0]

                dest = np.where(np_goal == str(i))
                dest_row = dest[0][0]
                dest_col = dest[1][0]

                dist = abs(dest_row - beg_row) + abs(dest_col - beg_col)
                manhattan_distances[index] += dist
        return min(manhattan_distances)
    
    def stringify_state(self, state):
        output = ""
        for row in state:
            output += " ".join(row) + " "
        return output
    
    def run_algo(self):
        for input_i, x in enumerate(self.inputs):
            for h in self.heuristics:
                print('Computing', str(x), h)
                self.reset(x)
                self.heuristic = h
                        
                start = time.time()
                chosen_state = self.initial_state
                if (chosen_state[1] == self.goal_state1 or chosen_state[1] == self.goal_state2):
                    self.is_goal_state = True
                i = 0
                
                is_no_solution = False
                while (not self.is_goal_state):
                    if (time.time() - start > 60):
                        is_no_solution = True
                        break
                    self.add_successors_to_open_list(chosen_state)
                    if (self.open_list.empty()):
                        break 
                    chosen_state = self.open_list.get()
                    self.update_zero_position(chosen_state)
                    self.ensure_ignore(chosen_state[2])
                    if (chosen_state[1] == self.goal_state1 or chosen_state[1] == self.goal_state2):
                        self.is_goal_state = True
                        break
                    self.close_list.put(copy.deepcopy(chosen_state))
                    i = i + 1

                #done
                end = time.time()

                #output solution and search
                nodes = []
                while(not chosen_state == None):
                    nodes.append(chosen_state)
                    chosen_state = chosen_state[6]
                nodes = nodes[::-1] #reverses list
                
                #output the search space
                with open(str(input_i) + "_astar-" + h + "_search.txt", 'w') as f:
                    for key, value in self.search_space.items():
                        f.write(value+"\n")

                #print the solution space
                with open(str(input_i) + "_astar-" + h + "_solution.txt", 'w') as f:
                    cost = 0
                    for node in nodes:
                        f.write(str(node[7]) + " " + str(node[3]) + " " + self.stringify_state(node[1]) + "\n")
                        cost += node[3]
                    f.write(str(cost) + " " +str(round((end - start),5)))

                #handle_no_solution
                if is_no_solution:
                    print("No solution")
                    self.analysis[h] = {'total cost': None, 'found_a_solution': self.is_goal_state, 'solution_path_length': len(list(nodes)), 'search_path_length': len(list(self.search_space.items())), 'execution_time': (end - start)}
                    with open(str(input_i) + "_astar-" + h + "_search.txt", 'w') as f:
                        f.write("no_solution\n")
                    with open(str(input_i) + "_astar-" + h + "_solution.txt", 'w') as f:
                        f.write("no_solution\n")
                else:
                    self.analysis[h] = {'total cost': cost, 'found_a_solution': self.is_goal_state, 'solution_path_length': len(list(nodes)), 'search_path_length': len(list(self.search_space.items())), 'execution_time': (end - start)}
                    print(self.analysis[h])
        return self.analysis

# algo = AStar("3 0 1 4 2 6 5 7", 2, 4)
# algo.run_algo()


#TODO: Optimize h_0 and print to files instead of console.