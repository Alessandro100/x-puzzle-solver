class XPuzzle:
    #sample input: 1 0 3 7 5 2 6 4 
    def __init__(self, rows, cols, input):
        self.rows = rows
        self.cols = cols
        self.arr = []
        # we keep track of the 0 position to increase the performance of our algorithm
        self.zero_position = (0,0) #row, column
        self.__initialize_data_strcuture(input)
        print('Input: ' + input)
        self.pretty_print_array()

    # takes the input and formats it to the wanted data structure
    def __initialize_data_strcuture(self, input):
        input_arr = input.split(" ")
        count = 0
        for i in range(self.rows): 
            col = [] 
            for j in range(self.cols): 
                value = input_arr[count]
                if(value == '0'):
                    self.zero_position = (i,j)
                col.append(value)
                count += 1
            self.arr.append(col)

    # prints the data structure in a nice format for the console
    def pretty_print_array(self):
        for row in self.arr:
            print(*row)


    # moves the empty tile: up, down, left, right and will print invalid if the move is not correct while returning -1
    def regular_move(self, move_direction_of_empty_tile):
        zero_row = self.zero_position[0]
        zero_col = self.zero_position[1]
        is_up_move_valid = (move_direction_of_empty_tile == 'up' and self.zero_position[0] != 0)
        is_down_move_valid = (move_direction_of_empty_tile == 'down' and self.zero_position[0] != str(self.rows - 1))
        is_right_move_valid = (move_direction_of_empty_tile == 'right' and self.zero_position[1] != str(self.cols - 1))
        is_left_move_valid = (move_direction_of_empty_tile == 'left' and self.zero_position[1] != 0)

        if(is_up_move_valid):
            return self.__swap(zero_row - 1, zero_col)
        
        if(is_down_move_valid):
            return self.__swap(zero_row + 1, zero_col)
        
        if(is_right_move_valid):
            return self.__swap(zero_row, zero_col + 1)
        
        if(is_left_move_valid):
            return self.__swap(zero_row, zero_col - 1)

        print('Invalid Regular Move')
        return -1

    # takes care of the swapping logic and handles new zero position
    def __swap(self, row_swap, col_swap):
        value_swap = self.arr[row_swap][col_swap]
        self.arr[self.zero_position[0]][self.zero_position[1]] = value_swap
        self.arr[row_swap][col_swap] = 0
        self.zero_position = (row_swap, col_swap)
        return 0

    # wrapping move will auto detect if possible and will do it if it is
    # NOTE: THERE IS NEW LOGIC IF IT'S NOT 2X4 AND CAN WRAP WITH COLUMNS
    def wrapping_move(self):
        diagonal_info = self.__corner_position_information()

        if(diagonal_info['is_zero_top_left']):
            return self.__swap(0, self.cols - 1)

        if(diagonal_info['is_zero_top_right']):
            return self.__swap(0, 0)

        if(diagonal_info['is_zero_bottom_left']):
            return self.__swap(self.rows - 1, self.cols - 1)

        if(diagonal_info['is_zero_bottom_right']):
            return self.__swap(self.rows - 1, 0)

        print('Invalid Wrapping Move')
        return -1

    def __corner_position_information(self):
            zero_row = self.zero_position[0]
            zero_col = self.zero_position[1]
            diagonal_dict = {
                'is_zero_top_left': (zero_row == 0 and zero_col == 0),
                'is_zero_top_right': (zero_row == 0 and zero_col == self.cols - 1),
                'is_zero_bottom_left': (zero_row == self.rows - 1 and zero_col == 0),
                'is_zero_bottom_right': (zero_row == self.rows - 1 and zero_col == self.cols - 1)
            }
            return diagonal_dict

    # if the 0 is in a corner, it can wrap and swap there, or it can move diagonally within
    def diagonal_move(self, is_wrap_move):
        diagonal_info = self.__corner_position_information()

        if(diagonal_info['is_zero_top_left']):
            if(is_wrap_move):
                return self.__swap(self.rows - 1, self.cols - 1)
            else:
                return self.__swap(1, 1)
        
        if(diagonal_info['is_zero_top_right']):
            if(is_wrap_move):
                return self.__swap(self.rows - 1, 0)
            else:
                return self.__swap(1, self.cols - 2)

        if(diagonal_info['is_zero_bottom_left']):
            if(is_wrap_move):
                return self.__swap(0, self.cols - 1)
            else:
                return self.__swap(self.rows - 2, 1)

        if(diagonal_info['is_zero_bottom_right']):
            if(is_wrap_move):
                return self.__swap(0, 0)
            else:
                return self.__swap(self.rows - 2, self.cols - 2)
        
        print("Invalid Diagonal Move")
        return -1
        

        


puzzle = XPuzzle(2, 4, '1 0 3 7 5 2 6 4')
#puzzle2 = XPuzzle(3, 8, '3 0 1 4 2 6 5 7 6 3 4 7 1 2 5 0 1 0 3 6 5 2 7 4')