import random
import ipdb


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

    def get_misplaced_values(self):
        '''Compares self.board_state against self.goal_state, returning an
        array of the actual values that are misplaced. By extension, this 
        returns an empty list if the board is solved.
        '''
        misplaced = []
        for i, v in enumerate(self.board_state):
            if self.board_state[i] != self.goal_state[i]:
                misplaced.append(v)
        return misplaced

    def get_row(self, board_val):
        '''Given a value 0-8, this function will return the row where that 
        value currently is
        '''
        curr_ind = self.board_state.index(board_val)
        return int(curr_ind/3)

    def get_col(self, board_val):
        '''Given a value 0-8, this function will return the column where that 
        value currently is
        '''
        curr_ind = self.board_state.index(board_val)
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
            next_board.extend(self.board_state)
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

    def board_to_state(self, board_list):
        '''The list form of a board configuration will be helpful for making
        moves and calculating distances. In terms of repeated state checking, 
        I'm converting everything to strings
        '''
        return ''.join([str(v) for v in board_list])

    def state_to_board(self, state_string):
        '''Simply the inverse of the above function. I'm honestly not sure
        how useful this will be.
        '''
        return [int(v) for v in state_string]

class depthFirstSearchSolver(eightBlock):
    
    def __init__(self, start_state = None, goal_state = None):
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
        super().__init__(start_state, goal_state)
        self.path_map = {}
        self.board_stack = [{"child":self.board_state, 
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
        the path_map, which keeps track of visited states and all of the 
        parent-to-child relationships between those states. After setting 
        self.board_state as the `child` attribute of current_board, we then 
        use current_board to make this update.

        The path_map dictionary being updated has strings representing every 
        child state visited in the solution so far as keys. The values are 
        tuples in the form of (parent state, direction). Thus we can say: 
        "to get to [child_state], I moved [direction] from [parent_state]"

        The only exception to this dictionary structure is that the initial 
        state key will have a value of None, since it has no parent.
        '''
        self.board_state = current_board["child"]
        current_state = self.board_to_state(self.board_state)
        parent_state = current_board["parent"]
        if parent_state is None:
            self.path_map[current_state] = None
        else:
            parent_to_child_dir = current_board["mv_dir"]
            self.path_map[current_state] = (parent_state, parent_to_child_dir)

    def get_children(self, current_board):
        '''After popping the current board off the stack, we then get its
        children. All this consists of is looking up all possible moves we 
        can make, excluding any states that we've already visited, and 
        annotating remaining states with their parent, the direction of
        the move to yield the child, and the new level in the search tree

        returns a list of stack dictionaries representing all possible moves
        '''
        child_stack_dicts = []
        poss_kids = self.get_next_boards()
        for poss_mv in poss_kids.keys():
            if self.board_to_state(poss_kids[poss_mv]) in self.path_map.keys():
                continue
            stack_dict = {"child":poss_kids[poss_mv],
                          "parent":self.board_to_state(self.board_state),
                          "mv_dir":poss_mv,
                          "path_cost":current_board["path_cost"] + 1}
            child_stack_dicts.append(stack_dict)
        return child_stack_dicts

    def children_to_stack(self, child_stack_dicts):
        '''Inserts each object in child_stack_dicts at the front of 
        self.board_stack in reverse order. This is so that the first
        direction we can possibly move each time we generate children
        will always be the next feasible candidate 
        '''
        for stack_dict in child_stack_dicts[::-1]:
            self.board_stack.insert(0, stack_dict)

    def retrieve_solution_path(self):
        '''Once we find the solution state, we use it as a key in path_map
        to look up the parent state and the direction we took to get there.
        We then repeatedly look up the parent of the parent state until we
        reach the initial state with no parent.

        Returns a list of (parent_state, direction) tuples from path_map that 
        spell out the solution found. The length of this solution_path is the 
        number of levels deep in the tree we had to go to find this solution
        '''
        solution_path = []
        child_key = self.board_to_state(self.board_state)
        while self.path_map.get(child_key,""):
            solution_path.insert(0, self.path_map[child_key])
            child_key = self.path_map[child_key][0]
        return solution_path

    def solve(self):
        '''The implementation of depth-first search basically just chains
        the last five functions together. 

            * look at the top of the stack, exiting if it's empty
            * update the path_map with info from the top of the stack
            * check to see if we're at a goal state, returning the solution if we are
            * Otherwise, we pop that top item off the stack and get child boards
            * Then we add these children to the top of the stack and repeat
        '''
        while self.get_misplaced_values():
            curr_board = self.check_top_of_stack()
            if curr_board is None:
                return curr_board
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution found!")
                return self.retrieve_solution_path()
            self.board_stack.pop(0)
            stack_children = self.get_children(curr_board)
            self.children_to_stack(stack_children)

    def display_solution_path(self, solution_path):
        '''Simply iterates over the tuples and prints out the solution 
        instructions line by line in the format "From [state], move [direction"
        '''
        for i, tup in enumerate(solution_path):
            print("{}. From {}, move {}".format(i + 1, tup[0], tup[1])) 


class breadthFirstSearchSolver(eightBlock):
    
    def __init__(self, start_state = None, goal_state = None):
        '''Basically the same as
        '''
        super().__init__(start_state, goal_state)
        self.path_map = {}
        self.board_queue = [{"child":self.board_state,
                             "parent":None,
                             "path_cost":0}]



if __name__ == "__main__":
    
    in_board = [1,2,3,4,5,6,7,0,8]
    goal_board = None # defaults to [1,2,3,4,5,6,7,8,0]
    foo = depthFirstSearchSolver(in_board, goal_board)
    # Display the board properly
    foo.display_board()
    # ipdb.set_trace()

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
    merp = foo.solve()
    print("Cost of solution found: {}".format(len(merp)))
    ipdb.set_trace()




    