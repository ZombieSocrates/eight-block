from base_board import eightBlock

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

    def solve(self, verbose = False):
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
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

    def display_solution_path(self, solution_path):
        '''Simply iterates over the tuples and prints out the solution 
        instructions line by line in the format "From [state], move [direction"
        '''
        for i, tup in enumerate(solution_path):
            print("{}. From {}, move {}".format(i + 1, tup[0], tup[1]))

class breadthFirstSearchSolver(eightBlock):
    
    def __init__(self, start_state = None, goal_state = None):
        '''Basically the same as the init of depthFirstSearchSolver, as is the 
        case for most of these docstrings.

        The biggest difference here is that I'm calling the structure for
        storing child states the queue instead of the stack.
        '''
        super().__init__(start_state, goal_state)
        self.path_map = {}
        self.board_queue = [{"child":self.board_state,
                             "parent":None,
                             "path_cost":0}]

    def check_queue(self):
        '''We always begin the solve method by looking at the first board
        dictionary in the board_queue. This method returns the first object 
        in the queue if it exists, and returns None otherwise
        '''
        try:
            top_board = self.board_queue[0]
        except IndexError:
            print("Initial board configuration not solveable")
            top_board = None
        return top_board

    def update_path_map(self, current_board):
        '''Once we have a board from the top of the queue, we update 
        the path_map. 
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
        '''After popping the current board off the queue, we then get its
        children, excluding any states that we've already visited. We 
        annotate unseen child states with their parent, the direction of
        the move to yield the child, and the new level in the search tree

        returns a list of queue dictionaries representing all possible moves
        '''
        child_queue_dicts = []
        poss_kids = self.get_next_boards()
        for poss_mv in poss_kids.keys():
            if self.board_to_state(poss_kids[poss_mv]) in self.path_map.keys():
                continue
            queue_dict = {"child":poss_kids[poss_mv],
                          "parent":self.board_to_state(self.board_state),
                          "mv_dir":poss_mv,
                          "path_cost":current_board["path_cost"] + 1}
            child_queue_dicts.append(queue_dict)
        return child_queue_dicts

    def children_to_queue(self, child_queue_dicts):
        '''Chucks children at the back of the queue. This is the big difference 
        between depth-first and breadth-first search 
        '''
        self.board_queue.extend(child_queue_dicts)

    def retrieve_solution_path(self):
        solution_path = []
        child_key = self.board_to_state(self.board_state)
        while self.path_map.get(child_key,""):
            solution_path.insert(0, self.path_map[child_key])
            child_key = self.path_map[child_key][0]
        return solution_path

    def solve(self, verbose = False):
        '''The implementation of breadth-first search basically just chains
        the last five functions together. 

            * look at the top of the queue, exiting if it's empty
            * update the path_map with info from the top of the queue
            * check to see if we're at a goal state, returning the solution if we are
            * Otherwise, we take that top item off the queue and get child boards
            * Then we add these children to the back of the queue and repeat
        '''
        while self.get_misplaced_values():
            curr_board = self.check_queue()
            if curr_board is None:
                return curr_board
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution found!")
                return self.retrieve_solution_path()
            self.board_queue.pop(0)
            queue_children = self.get_children(curr_board)
            self.children_to_queue(queue_children)
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

    def display_solution_path(self, solution_path):
        '''Simply iterates over the tuples and prints out the solution 
        instructions line by line in the format "From [state], move [direction"
        '''
        for i, tup in enumerate(solution_path):
            print("{}. From {}, move {}".format(i + 1, tup[0], tup[1]))

if __name__ == "__main__":
    pass 