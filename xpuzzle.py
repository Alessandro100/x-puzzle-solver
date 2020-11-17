class XPuzzle:
    #sample input: 1 0 3 7 5 2 6 4 
    def __init__(self, rows, cols, input):
        self.rows = rows
        self.cols = cols
        self.arr = []
        # we keep track of the 0 position to increase the performance of our algorithm
        self.zero_position = (0,0) #row, column
        self.__initialize_data_strcuture(input)

    # takes the input and formats it to the wanted data structure
    def __initialize_data_strcuture(self, input):
        input_arr = input.split(" ")
        count = 0
        for i in range(self.rows): 
            row = [] 
            for j in range(self.cols): 
                value = input_arr[count]
                if(value == '0'):
                    self.zero_position = (i,j)
                row.append(value)
                count += 1
            self.arr.append(row)

    # prints the data structure in a nice format for the console
    def pretty_print_array(self):
        for row in self.arr:
            print(*row)

    def find_valid_moves(self):
        valid_moves = []
        if (self.zero_position[0] != 0):
            valid_moves.append('up')
        if (self.zero_position[0] != self.rows - 1):
            valid_moves.append('down')
        if (self.zero_position[1] != 0):
            valid_moves.append('left')
        if (self.zero_position[1] != self.cols - 1):
            valid_moves.append('right')

        if (self.zero_position[0] == 0 and self.zero_position[1] == 0):
            valid_moves.append('top_left_wrap')
            valid_moves.append('top_left_diagonal_wrap')
            valid_moves.append('top_left_diagonal_adjacent')
        elif (self.zero_position[0] == 0 and self.zero_position[1] == (self.cols - 1)):
            valid_moves.append('top_right_wrap')
            valid_moves.append('top_right_diagonal_wrap')
            valid_moves.append('top_right_diagonal_adjacent')
        elif (self.zero_position[0] == (self.rows - 1) and self.zero_position[1] == 0):
            valid_moves.append('bottom_left_wrap')
            valid_moves.append('bottom_left_diagonal_wrap')
            valid_moves.append('bottom_left_diagonal_adjacent')
        elif (self.zero_position[0] == (self.rows - 1) and self.zero_position[1] == (self.cols - 1)):
            valid_moves.append('bottom_right_wrap')
            valid_moves.append('bottom_right_diagonal_wrap')
            valid_moves.append('bottom_right_diagonal_adjacent')
        return valid_moves 

    # moves the empty tile: up, down, left, right and will print invalid if the move is not correct while returning -1
    def regular_move(self, move_direction_of_empty_tile):
        zero_row = self.zero_position[0]
        zero_col = self.zero_position[1]
        is_up_move_valid = (move_direction_of_empty_tile == 'up' and self.zero_position[0] != 0)
        is_down_move_valid = (move_direction_of_empty_tile == 'down' and self.zero_position[0] != self.rows - 1)
        is_right_move_valid = (move_direction_of_empty_tile == 'right' and self.zero_position[1] != self.cols - 1)
        is_left_move_valid = (move_direction_of_empty_tile == 'left' and self.zero_position[1] != 0)

        if(is_up_move_valid):
            return self.__swap(zero_row - 1, zero_col)
        
        if(is_down_move_valid):
            return self.__swap(zero_row + 1, zero_col)
        
        if(is_right_move_valid):
            return self.__swap(zero_row, zero_col + 1)
        
        if(is_left_move_valid):
            return self.__swap(zero_row, zero_col - 1)

        return -1

    # takes care of the swapping logic and handles new zero position
    def __swap(self, row_swap, col_swap):
        value_swap = self.arr[row_swap][col_swap]
        self.arr[self.zero_position[0]][self.zero_position[1]] = value_swap
        self.arr[row_swap][col_swap] = 0
        self.zero_position = (row_swap, col_swap)
        return 0

    # wrapping move will auto detect if possible and will do it if it is
    def wrapping_move(self, column = False):
        if(column and self.rows > 2):
            return self.__wrapping_move_with_column()

        diagonal_info = self.__corner_position_information()

        if(diagonal_info['is_zero_top_left']):
            return self.__swap(0, self.cols - 1)

        if(diagonal_info['is_zero_top_right']):
            return self.__swap(0, 0)

        if(diagonal_info['is_zero_bottom_left']):
            return self.__swap(self.rows - 1, self.cols - 1)

        if(diagonal_info['is_zero_bottom_right']):
            return self.__swap(self.rows - 1, 0)

        return -1
    
    # This is only possible if requested and more than 2 rows
    def __wrapping_move_with_column(self):
        diagonal_info = self.__corner_position_information()

        if(diagonal_info['is_zero_top_left']):
            return self.__swap(self.row - 1, 0)

        if(diagonal_info['is_zero_top_right']):
            return self.__swap(self.rows - 1, self.cols - 1)

        if(diagonal_info['is_zero_bottom_left']):
            return self.__swap(0, 0)

        if(diagonal_info['is_zero_bottom_right']):
            return self.__swap(0, self.cols - 1)

        return -1

    def __corner_position_information(self):
            zero_row = self.zero_position[0]
            zero_col = self.zero_position[1]
            diagonal_info = {
                'is_zero_top_left': (zero_row == 0 and zero_col == 0),
                'is_zero_top_right': (zero_row == 0 and zero_col == self.cols - 1),
                'is_zero_bottom_left': (zero_row == self.rows - 1 and zero_col == 0),
                'is_zero_bottom_right': (zero_row == self.rows - 1 and zero_col == self.cols - 1)
            }
            return diagonal_info

    # if the 0 is in a corner, it can wrap and swap there, or it can move diagonally within
    def diagonal_move(self, is_move):
        diagonal_info = self.__corner_position_information()

        if(diagonal_info['is_zero_top_left']):
            if(is_move):
                return self.__swap(self.rows - 1, self.cols - 1)
            else:
                return self.__swap(1, 1)
        
        if(diagonal_info['is_zero_top_right']):
            if(is_move):
                return self.__swap(self.rows - 1, 0)
            else:
                return self.__swap(1, self.cols - 2)

        if(diagonal_info['is_zero_bottom_left']):
            if(is_move):
                return self.__swap(0, self.cols - 1)
            else:
                return self.__swap(self.rows - 2, 1)

        if(diagonal_info['is_zero_bottom_right']):
            if(is_move):
                return self.__swap(0, 0)
            else:
                return self.__swap(self.rows - 2, self.cols - 2)
        
        return -1

    def is_goal_state(self):
        goal_string = ''
        for i in range((self.cols * self.rows) - 1):
            goal_string += str(i + 1) + ' '
        goal_string += '0'

        return goal_string == self.current_state_to_string()

    def current_state_to_string(self):
        return ' '.join(map(str, [ y for x in self.arr for y in x]))

# Examples
#puzzle = XPuzzle(2, 4, '1 2 3 4 5 6 0 7')
#puzzle.pretty_print_array()
#puzzle.regular_move('down')
#puzzle.regular_move('left')
#puzzle.diagonal_move(False)
#puzzle.diagonal_move(True)
#puzzle.wrapping_move()
#puzzle.regular_move('right')
#puzzle.regular_move('left')
#puzzle.regular_move('up')
#puzzle.regular_move('down')
#puzzle.pretty_print_array()
#print('goal state? ' + str(puzzle.is_goal_state()))

#puzzleGoal = XPuzzle(2, 4, '1 2 3 4 5 6 7 0')
#puzzleGoal.is_goal_state()

#puzzleBig = XPuzzle(3, 8, '1 2 3 4 0 6 7 8 9 10 11 12 13 14 15 16 17 5')