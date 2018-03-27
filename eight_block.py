import random
import ipdb


class eightBlock():

    def __init__(self, positions = None):
        '''The most important step in this initial init is defining the initial 
        board configuration. Calling init with no positions will just randomly 
        shuffle valid_vals. Otherwise, we'll start with the positions given, 
        assuming it is a list containing only integers 0 through 8


        TKTK Might want to initialize each of these with a goal state, too. Just
        to be explicit about it
        '''
        self.valid_vals = [i for i in range(9)]
        self.valid_dims = [i for i in range(3)]
        self.valid_dirs = ["left","right","up","down"]
        # UNCERTAIN IF THIS IS ACTUALLY NECESSARY
        self.opposites = {"left":"right","right":"left","down":"up","up":"down"}
        # DELETE IF NEVER USED
        if positions is None:
            random.shuffle(self.valid_vals)
            self.board_config = self.valid_vals
        elif isinstance(positions, list):
            if sorted(positions) == self.valid_vals:
                self.board_config = positions
            else:
                v_msg = "positions must be a permutation of integers 0-8"
                raise ValueError(v_msg)
        else:
            inpt_tp = type(positions).__name__
            t_msg = "positions must be a list, not {}".format(inpt_tp)
            raise TypeError(t_msg)
            
    def display_board(self, board = None):
        '''Will display a given board configuration in 3 X 3 form.

        If called with board = None, we'll simply display whatever the current 
        value of self.board_config is. You can also pass in a possible child
        configuration like those output from the move left, right, up, and down 
        functions. If given an empty list, this will simply print out a message 
        about the move being invalid.
        '''
        if isinstance(board, list) and not board:
            print("Invalid move...cannot display")
        else:
            if board is None:
                board = self.board_config
            for r in self.valid_dims:
                print(board[3*r:3*(r + 1)])

    def get_misplaced_values(self):
        '''scans self.board_config and returns a list of misplaced values
        against the assumed goal state of [1,2,3,4,5,6,7,8,0].

        By extension, this will return an empty list if the board is solved

        TKTK: RIGHT NOW THIS ASSUMES A GOAL STATE. This would need to change
        if goal_state was ever defined as a part of the class itself
        '''
        misplaced = []
        for v in self.board_config:
            if (v == 0) and (self.board_config.index(v) != 8):
                misplaced.append(v)
            elif (v != 0) and (self.board_config.index(v) != (v - 1)):
                misplaced.append(v)
        return misplaced

    def get_row(self, board_val):
        '''Given a value 0-8, this function will return the row where that 
        value currently is
        '''
        curr_ind = self.board_config.index(board_val)
        return int(curr_ind/3)

    def get_col(self, board_val):
        '''Given a value 0-8, this function will return the column where that 
        value currently is
        '''
        curr_ind = self.board_config.index(board_val)
        return curr_ind % 3

    def make_move(self, mv_dir):
        '''Moves the zero in the current board configuration in the direction 
        specified by mv_dir. Will return the updated configuration if that 
        direction is valid. Returns an empty list otherwise
        '''
        if mv_dir not in self.valid_dirs:
            d_msg = "direction must be {}".format(", ".join(self.valid_dirs))
            raise ValueError(d_msg)
        next_board = []
        dim_chk = self.get_row(0) if mv_dir in ["up","down"] else self.get_col(0)
        chk_val = -1 if mv_dir in ["left","up"] else 1
        if (dim_chk + chk_val) in self.valid_dims:
            next_board.extend(self.board_config)
            z_ind = next_board.index(0)
            mv_amt = 3 * chk_val if mv_dir in ["up","down"] else chk_val
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

    def board_to_state(self, board):
        '''The list form of a board configuration will be helpful for making
        moves and calculating distances. In terms of repeated state checking, 
        I'm converting everything to strings
        '''
        return ''.join([str(v) for v in board])

class depthFirstSearchSolver(eightBlock):
    '''Notes from Tori. Use a stack. Last In, First Out
    '''
    def __init__(self, positions = None):
        '''Calls the initialization function of eightBlock (with option to 
        specify initial board configuration) and then defines two additional
        class level attributes

            * path_map (dict): a dictionary that keeps track of child:parent 
            relationships visited by the solve() method. Initializes as
            empty
            * board_stack (list): the data structure used to implement
            depth-first search. The first thing on the stack is a dictionary 
            representation of the initial board configuration, along with
            a marker indicating we're at depth 0 in the search tree
        '''
        super().__init__(positions)
        self.path_map = {}
        self.board_stack = [{"child":self.board_config, 
                             "parent":None,
                             "path_cost":0}]

    def check_top_of_stack(self):
        '''We always begin the solve method by looking at the first stack
        dictionary in the board_stack. There are cases (non-solveable boards) 
        where the stack can be empty.

        This method returns the first object in the stack if it exists, and 
        returns None otherwise
        '''
        try:
            top_board = self.board_stack[0]
        except IndexError:
            print("Initial board configuration not solveable")
            top_board = None
        return top_board

    def update_path_map(self, current_board):
        '''Once we have a board from the top of the stack, we need to update 
        the path_map, which keeps track of visited states and allows us to
        return a solution when the goal state is found
        '''
        pass

    def solve(self):
        '''Docstring in with code for now...
        '''

        # Create the first dictionary in your stack of boards (MOVE TO INIT)
        # Each of these dictionaries has the current board_config,
        # its parent, the direction from that parent to the current config
        # and the cost accrued to get there 
        while self.get_misplaced_values():
            curr_board = self.check_top_of_stack()
            if curr_board is None:
                return curr_board
            self.board_config = curr_board["child"]
            curr_state = self.board_to_state(self.board_config)
            self.path_map[curr_state] = (curr_board["parent"], curr_board["mv_dir"]) if curr_board["parent"] else None
            if not self.get_misplaced_values():
                print("WE SOLVED IT!!!")
                break
            self.board_stack.pop(0)
            next_boards = self.get_next_boards()
            # Generate a list of new dictionaries to go on the stack,
            # so long as they are unseen states
            to_stack = []
            for poss_move in next_boards.keys():
                if self.board_to_state(next_boards[poss_move]) in self.path_map.keys():
                    continue
                stack_dict = {"child":next_boards[poss_move],
                              "parent":curr_state,
                              "mv_dir":poss_move,
                              "path_cost":curr_board["path_cost"] + 1}
                to_stack.append(stack_dict)
            # Now, append the items in to_stack to board_stack in
            # reverse, so that we're always moving in the same direction
            # first, if possible
            for stack_dict in to_stack[::-1]:
                self.board_stack.insert(0,stack_dict)
            print(len(self.path_map)) 

        # Still need to think about what the proper way to return something is...
        # Unwinding the path dictionary is basically getting values and using those
        # as keys until you hit the key that gives you a value None

        # This should return a list that is equivalent to board["path_cost"]
        # For the test case [1,2,3,4,5,6,7,0,8], that should be 433

        # MAKE ME A FUNCTION
        solution_path = []
        path_key = self.board_to_state(self.board_config)
        while self.path_map.get(path_key,""):
            solution_path.insert(0,self.path_map[path_key])
            path_key = self.path_map[path_key][0]

        return solution_path


class breadthFirstSearch(eightBlock):
    '''Notes from tori: use a queue. First in, first out
    '''
    pass



if __name__ == "__main__":
    
    foo = depthFirstSearchSolver([1,2,3,4,5,6,7,0,8])
    # Display the board properly
    foo.display_board()

    # Index into things properly
    for v in range(len(foo.valid_vals)):
        r = foo.get_row(v)
        c = foo.get_col(v)
        print("{} located at position ({},{})".format(v, r, c))

    # Test whether the board is solved
    wrongs = foo.get_misplaced_values()
    if not wrongs:
        print("Board is solved!")
    else:
        print("These are out of place: {}".format(wrongs))

    # print("Making possible moves")
    # for mv_dir, new_brd in foo.get_next_boards().items():
    #     print(mv_dir)
    #     foo.display_board(new_brd)
    #     print()
    foo.solve()
    ipdb.set_trace()




    