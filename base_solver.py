from base_board import eightBlock



class eightBlockSolver(eightBlock):

    def __init__(self, start_state = None, goal_state = None):
    	'''Initializes an eightBlock and then defines two additional
        class attributes needed to reach and keep track of solution
        paths

            * path_map (dict): a dictionary that keeps track of child:parent 
            relationships visited by the solve() method. Initializes as
            empty
            * children_boards (list): the data structure used to implement
            any search. The first thing on the stack is a dictionary 
            representation of the initial board configuration, along with
            a marker indicating we're at depth 0 in the search tree. As the
            search proceeds, we'll add more of these dictionaries that track
            where we are and how we got there.
        '''
    	super().__init__(start_state, goal_state)
    	self.path_map = {}
    	self.children_boards = [{"child":self.board_state,
    	                         "parent":None,
    	                         "path_cost":0}]

    def check_next_child(self):
    	'''We begin any solve method by looking at the first child board 
    	dictionary available. There are cases (non-solveable boards) 
        where this list will run out and be empty.

        This method returns the first object in self.children_boards if it 
        exists, and returns None otherwise.
        '''
    	try:
    		next_child = self.children_boards[0]
    	except IndexError:
    		print("Initial board state not solveable")
    		next_child = None
    	return next_child






if __name__ == "__main__":
    pass 