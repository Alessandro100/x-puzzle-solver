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
        self.goal_node = ()
        self.initial_state = initial_state

    def run(self):
        uniform_cost_search_file = open("0_ucs_search.txt", "w")
        uniform_cost_search_file.write("0 0 0 " + self.initial_state + "\n")
        uniform_cost_search_file.close()
        start = time.time()
        goal_state = "1 2 3 4 5 6 7 0"
        self.set_state_open_list(self.initial_state, 0) # nodes that need to be visited (priority queue or dictionairy)

        print('start loop')
        close_list = {}
        while not self.open_list.empty():
            # finds the smallest cost path and visits it
            current_node = self.open_list.get()
            current_node_prev_key = current_node[2]
            current_node_key = current_node[1]
            current_node_cost = current_node[0]

            if current_node_key not in close_list or close_list[current_node_key] > current_node_cost:
                close_list[current_node_key] = current_node_cost

                print("0 "+ str(current_node_cost)+ " 0 " + current_node_key)
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
        self.get_algorithm_stats()

    def normal_move_action_string(self, state, action):
        puzzle = XPuzzle(2,4, state)
        if( puzzle.regular_move(action) != -1):
            return puzzle.current_state_to_string()
        else:
            return -1

    def wrapping_move_action_string(self, state):
        puzzle = XPuzzle(2,4, state)
        if( puzzle.wrapping_move() != -1):
            return puzzle.current_state_to_string()
        else:
            return -1
    
    def diagonal_move_action_string(self, state, is_wrapping):
        puzzle = XPuzzle(2,4, state)
        if( puzzle.diagonal_move(is_wrapping) != -1):
            return puzzle.current_state_to_string()
        else:
            return -1
    
    def set_state_open_list(self, current_state, base_amount):
        # 1 cost actions: up, down, left, right
        # 2 cost actions: wrapping_move
        # 3 cost actions: diagonal_move, diagonal_move(wrap)
        # total of 7 actions

        up_action = self.normal_move_action_string(current_state, "up")
        if(up_action != -1): self.open_list.put(((1 + base_amount), up_action, current_state))

        down_action = self.normal_move_action_string(current_state, "down")
        if(down_action != -1): self.open_list.put(((1 + base_amount), down_action,current_state))

        left_action = self.normal_move_action_string(current_state, "left")
        if(left_action != -1): self.open_list.put(((1 + base_amount), left_action, current_state))

        right_action = self.normal_move_action_string(current_state, "right")
        if(right_action != -1): self.open_list.put(((1 + base_amount), right_action, current_state))

        wrapping_action = self.wrapping_move_action_string(current_state)
        if(wrapping_action != -1): self.open_list.put(((2 + base_amount), wrapping_action, current_state))

        diagonal_action = self.diagonal_move_action_string(current_state, False)
        if(diagonal_action != -1): self.open_list.put(((3 + base_amount), diagonal_action, current_state)) 

        diagonal_action_wrap = self.diagonal_move_action_string(current_state, True)
        if(diagonal_action_wrap != -1): self.open_list.put(((3 + base_amount), diagonal_action_wrap, current_state)) 

    def get_algorithm_stats(self):
        if(not self.goal_node):
            print("No goal node")
        else:
            print("COST: " + str(self.goal_node[0]))
            print("KEY: " + str(self.goal_node[1]))
            print("PREV: " + str(self.goal_node[2]))
            print("This is the path it took")
            prev = self.goal_node[2]
            # while(prev != self.initial_state):
            #     print(prev)
            #     prev = self.open_list.get

#1 0 3 6 5 2 7 4
#6 3 4 7 1 2 5 0
#algo = UniformCost("1 0 3 6 5 2 7 4")
algo = UniformCost("6 3 4 7 1 2 5 0")

algo.run()