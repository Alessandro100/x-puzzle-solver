import time
from xpuzzle import XPuzzle

class UniformCost:
    def __init__(self):
        print("class init")
        self.close_list = {}

    def run(self):
        start = time.time()
        initial_state = "1 0 3 6 5 2 7 4"
        goal_state = "1 2 3 4 5 6 7 0"
        open_list = self.set_state_open_list(initial_state, 0, {}) # nodes that need to be visited (priority queue or dictionairy)

        print('start loop')
        while(len(open_list) > 0):
            # finds the smallest cost path and visits it
            current_node_key = min(open_list, key=open_list.get)
            print("0 0 " + current_node_key)
            
            # checks if goal state was reached
            if(current_node_key == goal_state):
                print("I reached the goal state!")
                print("COST: " + str(open_list[current_node_key]))
                break

            # we need to add this key to the closed list
            self.close_list[current_node_key] = open_list[current_node_key]

            # now we need to add the new nodes to the open list
            open_list = self.set_state_open_list(current_node_key, self.close_list[current_node_key], open_list)

            # removes the visited node from the open list
            open_list.pop(current_node_key)

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
    
    def set_state_open_list(self, current_state, base_amount, current_open_list):
        open_list = current_open_list
        # 1 cost actions: up, down, left, right
        # 2 cost actions: wrapping_move
        # 3 cost actions: diagonal_move, diagonal_move(wrap)
        # total of 7 actions

        up_action = self.normal_move_action_string(current_state, "up")
        if(up_action != -1 and not (up_action in self.close_list)): open_list[up_action] = (1 + base_amount)

        down_action = self.normal_move_action_string(current_state, "down")
        if(down_action != -1 and not (down_action in self.close_list)): open_list[down_action] = (1 + base_amount)

        left_action = self.normal_move_action_string(current_state, "left")
        if(left_action != -1 and not (left_action in self.close_list)): open_list[left_action] = (1 + base_amount)

        right_action = self.normal_move_action_string(current_state, "right")
        if(right_action != -1 and not (right_action in self.close_list)): open_list[right_action] = (1 + base_amount)

        wrapping_action = self.wrapping_move_action_string(current_state)
        if(wrapping_action != -1 and not (wrapping_action in self.close_list)): open_list[wrapping_action] = (2 + base_amount)

        diagonal_action = self.diagonal_move_action_string(current_state, False)
        if(diagonal_action != -1 and not (diagonal_action in self.close_list)): open_list[diagonal_action] = (3 + base_amount)

        diagonal_action_wrap = self.diagonal_move_action_string(current_state, True)
        if(diagonal_action_wrap != -1 and not (diagonal_action_wrap in self.close_list)): open_list[diagonal_action_wrap] = (3 + base_amount)

        return open_list

algo = UniformCost()
algo.run() 