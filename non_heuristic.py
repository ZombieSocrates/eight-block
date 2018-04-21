from base_board import eightBlock
from base_solver import eightBlockSolver

class depthFirstSearchSolver(eightBlockSolver):
    
    def __init__(self, start_state = None, goal_state = None):
        '''Nothing to see here, folks
        '''
        super().__init__(start_state, goal_state)

    def insert_children(self, next_children):
        '''Inserts each object in next_children at the front of 
        self.children_list in reverse order. This is so that the first
        direction we can possibly move each time we generate children
        will always be the next feasible candidate 
        '''
        for child in next_children[::-1]:
            self.children_list.insert(0, child)

    def solve(self, verbose = False):
        '''The implementation of depth-first search treats children_list
        as a stack, where the last child state inserted is the first one
        to be checked next. In this method we

            * get the first item in children_list, exiting if it's empty
            * update the path_map with info from that board
            * check to see if we're at a goal state, returning the solution if we are
            * Otherwise, we pop that top item off the stack and get child boards
            * Then we add these children to the top of the stack and repeat
        '''
        while self.get_misplaced_values():
            curr_board = self.check_next_child()
            if curr_board is None:
                return curr_board
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution found!")
                return self.retrieve_solution_path()
            self.children_list.pop(0)
            stack_children = self.get_children(curr_board)
            self.insert_children(stack_children)
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

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

class iterativeDeepeningSolver(depthFirstSearchSolver):

    def __init__(self, start_state = None, goal_state = None):
        '''Basically the same as the init of depthFirstSearchSolver, as is the 
        case for most of these docstrings.

        The biggest difference here is that I'm calling the structure for
        storing child states the queue instead of the stack.
        '''
        super().__init__(start_state, goal_state)
        self.path_map = {}
        self.board_zero = {"child":self.board_state,
                           "parent":None,
                           "path_cost":0}
        self.board_stack = [self.board_zero]
        self.depth_limit = 0

    def dig_back_through_stack(self):
        '''If the board on the very top of the stack at any given point
        has path cost greater than self.depth_limit, we need to dig
        back through and make sure we find an appropriate board.

        This function will return the first board it finds in the stack
        with a cost less than or equal to the current depth limit and move
        it to the very top of the stack so that it becomes the next board to
        be visited. If no such board can be found, it will return None
        '''
        to_the_front = None
        for stack_index, stack_board in enumerate(self.board_stack):
            if stack_board["path_cost"] <= self.depth_limit:
                to_the_front = self.board_stack.pop(stack_index)
                self.board_stack.insert(0, to_the_front)
                break
        return to_the_front

    def deepen_and_restart(self, verbose = False):
        '''If the method above doesn't return a valid board from the stack, we
        know that we need to iteratively deepen. That means we:

            * reset the board_stack to what it was at the __init__ call
            * clear out the path map to be empty once again
            * increase the depth limit by one

        This allows us to restart the entire search, but just go deeper the
        next time.
        '''
        self.path_map = {}
        self.board_stack = [self.board_zero]
        self.depth_limit += 1
        if verbose:
            print("Checked up to depth {}".format(self.depth_limit - 1))
            print("Restarting with depth limit {}".format(self.depth_limit))

    def solve(self, verbose = False):
        '''Iterative deepening is basically just a modification of depth-first 
        search. 

            * look at the top of the stack, exiting if it's entirely empty
            * if the item at the top is at a depth above the depth limit, scan 
            the rest of the stack for things with an appropriate depth
            * if you don't find any thing, increment depth limit and restart
            * otherwise, pop that thing to the front of the stack and continue
            as normal
            * update the path_map with info from the top of the stack
            * check to see if we're at a goal state, returning the solution if we are
            * Otherwise, we pop that top item off the stack and get child boards
            * Then we add these children to the top of the stack and repeat
        '''
        while self.get_misplaced_values():
            curr_board = self.check_top_of_stack()
            if curr_board is None:
                return curr_board
            elif curr_board["path_cost"] > self.depth_limit:
                curr_board = self.dig_back_through_stack()
                if curr_board is None:
                    self.deepen_and_restart(verbose = verbose)
                    continue
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution found!")
                return self.retrieve_solution_path()
            self.board_stack.pop(0)
            stack_children = self.get_children(curr_board)
            self.children_to_stack(stack_children)
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))


if __name__ == "__main__":
    pass