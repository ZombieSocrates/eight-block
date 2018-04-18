import random

'''This file contains the base class that all of the eight block solvers 
inherit from. The methods in this class generally handle moving and displaying 
different configurations of the board, retrieving positions of specific values, 
and checking to see whether input boards

'''


class eightBlock():

    def __init__(self, start_state = None, goal_state = None):
        '''Declares the valid tile values, row and column indices, and 
        movement directions applicable to any board. Then uses the optional 
        arguments start_state and goal_state to declare the initial positions 
        of the puzzle (`board_state`) and the `goal_state` we're aiming for, 
        respectively.

        Assuming they meet the conditions in the `validate` method, both 
        start_state and goal_state can be user configured. Otherwise, defaults 
        will be supplied by the `get_default` method.
        '''
        self.valid_vals = [i for i in range(9)]
        self.valid_dims = [i for i in range(3)]
        self.valid_dirs = ["left","right","up","down"]
        if start_state:
            self.board_state = self.validate(start_state)
        else:
            self.board_state = self.get_default("start")
        if goal_state:
            self.goal_state = self.validate(goal_state)
        else:
            self.goal_state = self.get_default("goal") 

    def get_default(self, default_type):
        '''Running this with the argument `start` returns a shuffling of 0-8 as
        the initial board configuration. Otherwise, this method returns the 
        default goal configuration of [1,2,3,4,5,6,7,8,0]
        '''
        if default_type == "start":
            dflt_board = self.valid_vals.copy()
            random.shuffle(dflt_board)
        else:
            dflt_board = self.valid_vals[1:] + [0]
        return dflt_board

    def validate(self, given_board):
        '''Throws errors if you try to pass in a board configuration that isn't 
        a permutation of [0,1,2,3,4,5,6,7,8]. Otherwise, returns the board that 
        you pass in.
        '''
        if not isinstance(given_board, list):
            inpt_tp = type(given_board).__name__
            raise TypeError("Expected list, not {}".format(inpt_tp))
        elif sorted(given_board) != self.valid_vals:
            raise ValueError("Board must be a permutation of integers 0-8")
        return given_board
         
    def display_board(self, board = None):
        '''Will display a given board configuration in 3 X 3 form.

        If called with board = None, we'll simply display whatever the current 
        value of self.board_state is. You can also pass in a possible child
        configuration like those output from the move left, right, up, and down 
        functions. If given an empty list, this will simply print out a message 
        about the move being invalid.
        '''
        if isinstance(board, list) and not board:
            print("Invalid move...cannot display")
        else:
            if board is None:
                board = self.board_state
            for r in self.valid_dims:
                print(board[3*r:3*(r + 1)])

    def get_misplaced_values(self, board = None):
        '''Compares a given board against self.goal_state, returning an
        array of the actual values that are misplaced. By extension, this 
        returns an empty list if the board is solved. If not explicitly given 
        a board, it will make the comparison with the current board_state.

        For the purposes of using this in calculating heuristics, 0 is not
        counted as a misplaced value. It's a blank tile, and there's no way 
        it can be the only wrong value anyway. 
        '''
        misplaced = []
        if board is None:
            board = self.board_state
        for i, v in enumerate(self.validate(board)):
            if self.validate(board)[i] != self.goal_state[i] and v!= 0:
                misplaced.append(v)
        return misplaced

    def get_row(self, board_val, board = None):
        '''Given a value 0-8, this function will return the row where that 
        value currently is. If not explicitly given a board, it will search
        in the current board_state. 
        '''
        if board is None:
            board = self.board_state
        curr_ind = self.validate(board).index(board_val)
        return int(curr_ind/3)

    def get_col(self, board_val, board = None):
        '''Given a value 0-8, this function will return the column where that 
        value currently is
        '''
        if board is None:
            board = self.board_state
        curr_ind = self.validate(board).index(board_val)
        return curr_ind % 3

    def make_move(self, mv_dir):
        '''Moves a tile in the current board configuration in the direction 
        specified by mv_dir. Will return the updated configuration if that 
        direction is valid move. Returns an empty list otherwise
        '''
        if mv_dir not in self.valid_dirs:
            d_msg = "direction must be {}".format(", ".join(self.valid_dirs))
            raise ValueError(d_msg)
        next_board = []
        dim_chk = self.get_row(0) if mv_dir in ["down","up"] else self.get_col(0)
        chk_val = -1 if mv_dir in ["right","down"] else 1
        if (dim_chk + chk_val) in self.valid_dims:
            next_board.extend(self.board_state)
            z_ind = next_board.index(0)
            mv_amt = 3 * chk_val if mv_dir in ["down","up"] else chk_val
            swap_v = next_board[z_ind + mv_amt]
            next_board[z_ind + mv_amt] = 0
            next_board[z_ind] = swap_v
        return next_board

    def get_next_boards(self):
        '''Will attempt to move the zero of the current board configuration in 
        all possible directions: left, right, up, and down.

        Returns a dictionary representing the possible next states, where the
        key is the direction and the value is the child board. We automatically
        exclude invalid board states.

        TKTK: To be absolutely sure about order, I could use an OrderedDict...
        '''
        next_boards_dict = {}
        for mv_dir in self.valid_dirs:
            if self.make_move(mv_dir):
                next_boards_dict[mv_dir] = self.make_move(mv_dir)
        return next_boards_dict

    def board_to_state(self, board_list):
        '''The list form of a board configuration will be helpful for making
        moves and calculating distances. In terms of repeated state checking, 
        I'm converting everything to strings
        '''
        return ''.join([str(v) for v in board_list])

    def state_to_board(self, state_string):
        '''Simply the inverse of the above function. I'm honestly not sure
        how useful this will be.

        TKTK: Might be helpful to return which tile is moved when given a
        state string and a direction? 
        '''
        return [int(v) for v in state_string]

if __name__ == "__main__":
	pass