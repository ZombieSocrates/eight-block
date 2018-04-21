from base_board import eightBlock
from base_solver import eightBlockSolver

class depthFirstSearchSolver(eightBlockSolver):
    
    def __init__(self, start_state = None, goal_state = None):
        '''Nothing to see here, folks
        '''
        super().__init__(start_state, goal_state)

    def stack_children(self, next_children):
        '''Inserts each object in next_children at the front of 
        self.children_list in reverse order. This is so that the first
        direction we can possibly move each time we generate children
        will always be the next feasible candidate 
        '''
        for child in next_children[::-1]:
            self.children_list.insert(0, child)

    def solve(self, verbose = False):
        '''In depth-first search, we treat children_list as a stack, where the 
        last child state inserted is the first one to be checked next. In this 
        method we...

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
            self.stack_children(self.get_children(curr_board))
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

class breadthFirstSearchSolver(eightBlockSolver):
    
    def __init__(self, start_state = None, goal_state = None):
        '''Just run eightBlockSolver's __init__() method...
        '''
        super().__init__(start_state, goal_state)

    def queue_children(self, next_children):
        '''Chucks children at the back of children_list. This is the key 
        difference between depth-first and breadth-first search 
        '''
        self.children_list.extend(next_children)

    def solve(self, verbose = False):
        '''In breadth-first search, we treat children_list as a queue, where the 
        first child state inserted is the first one to be checked next. In this 
        method we...

            * get the first item in children_list, exiting if it's empty
            * update the path_map with info from that board
            * check to see if we're at a goal state, returning the solution if we are
            * Otherwise, we take that top item off the queue and get child boards
            * Then we add these children to the back of the queue and repeat
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
            self.queue_children(self.get_children(curr_board))
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

class iterativeDeepeningSolver(depthFirstSearchSolver):

    def __init__(self, start_state = None, goal_state = None):
        '''With iterative deepening, we need to modify this method
        slightly by adding two attributes to each class instance.

            * depth_limit: Sets the upper bound for how far down we'll go.
            We need to increment this every time we restart the search
            * board_zero: Since we're going to be retracing the same path for 
            many different depth_limits, I need to store the starting point so 
            we can always re-expand the search tree.
        '''
        super().__init__(start_state, goal_state)
        self.board_zero = self.children_list[0]
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
        for stack_index, stack_board in enumerate(self.children_list):
            if stack_board["path_cost"] <= self.depth_limit:
                to_the_front = self.children_list.pop(stack_index)
                self.children_list.insert(0, to_the_front)
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
        self.children_list = [self.board_zero]
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
            curr_board = self.check_next_child()
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
            self.children_list.pop(0)
            self.stack_children(self.get_children(curr_board))
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

if __name__ == "__main__":
    pass