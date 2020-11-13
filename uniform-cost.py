import time
from queue import PriorityQueue
from xpuzzle import XPuzzle

class UniformCost:
    def __init__(self):
        print("class init")
        self.close_list = PriorityQueue()
        self.open_list = PriorityQueue()

    def run(self):
        start = time.time()
        initial_state = "6 3 4 7 1 2 5 0"
        goal_state = "1 2 3 4 5 6 7 0"
        self.set_state_open_list(initial_state, 0) # nodes that need to be visited (priority queue or dictionairy)

        print('start loop')
        while not self.open_list.empty():
            # finds the smallest cost path and visits it
            current_node = self.open_list.get()
            current_node_prev_key = current_node[2]
            current_node_key = current_node[1]
            current_node_cost = current_node[0]
            print("0 0 " + current_node_key)
            
            # checks if goal state was reached
            if(current_node_key == goal_state):
                print("I reached the goal state!")
                print("COST: " + str(current_node_cost))
                break

            # we need to add this key to the closed list
            self.close_list.put((current_node))

            # now we need to add the new nodes to the open list
            open_list = self.set_state_open_list(current_node_key, current_node_cost)

        end = time.time()
        print('I finished running in: ' + str(end - start) + " seconds")

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

        # wrapping_action = self.wrapping_move_action_string(current_state)
        # if(wrapping_action != -1 and not (wrapping_action in self.close_list)): open_list[wrapping_action] = (2 + base_amount)

        # diagonal_action = self.diagonal_move_action_string(current_state, False)
        # if(diagonal_action != -1 and not (diagonal_action in self.close_list)): open_list[diagonal_action] = (3 + base_amount)

        # diagonal_action_wrap = self.diagonal_move_action_string(current_state, True)
        # if(diagonal_action_wrap != -1 and not (diagonal_action_wrap in self.close_list)): open_list[diagonal_action_wrap] = (3 + base_amount)

algo = UniformCost()
algo.run() 