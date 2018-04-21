from base_board import eightBlock



class eightBlockSolver(eightBlock):

    def __init__(self, start_state = None, goal_state = None):
    	'''Initializes an eightBlock and then defines two additional
        class attributes needed to reach and keep track of solution
        paths

            * path_map (dict): a dictionary that keeps track of child:parent 
            relationships visited by the solve() method. Initializes as
            empty
            * children_list: the data structure used to implement
            any search. The first thing on this list is a dictionary 
            representation of the initial board configuration, along with
            a marker indicating we're at depth 0 in the search tree. As the
            search proceeds, we'll add more of these dictionaries that track
            what the board configuration is, what parent state we came from, 
            what direction we moved in, and the depth in the search tree.
        '''
    	super().__init__(start_state, goal_state)
    	self.path_map = {}
    	self.children_list = [{"child":self.board_state,
    	                       "parent":None,
    	                       "path_cost":0}]

    def check_next_child(self):
    	'''We begin any solve method by looking at the first child board 
    	dictionary available. There are cases (non-solveable boards) 
        where this list will run out and be empty.

        This method returns the first object in self.children_list if it 
        exists, and returns None otherwise.
        '''
    	try:
    		next_child = self.children_list[0]
    	except IndexError:
    		print("Initial board state not solveable")
    		next_child = None
    	return next_child

    def update_path_map(self, current_board):
    	'''Once we have a board from children_list, we need to update 
        the path_map, which keeps track of parent-to-child relationships 
        between those states. After setting self.board_state as the `child` 
        attribute of current_board, we use current_board to make this update.

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
    		self.path_map[current_state] = parent_state
    	else:
    		move_to_get_to_child = current_board["mv_dir"]
    		self.path_map[current_state] = (parent_state, move_to_get_to_child)

    def get_children(self, current_board):
    	'''After retrieving a board, we then get its children. This consists of 
    	looking up all possible moves we can make, excluding any states we've 
    	already visited, and annotating the result states with their parent, 
    	the direction of the move to yield the child, and the new level in the 
    	search tree.

        Returns a list of board dictionaries that needs to be integrated into
        children_list. 
        '''
    	child_board_dicts = []
    	poss_kids = self.get_next_boards()
        for poss_mv in poss_kids.keys():
            if self.board_to_state(poss_kids[poss_mv]) in self.path_map.keys():
                continue
            child_board = {"child":poss_kids[poss_mv],
                           "parent":self.board_to_state(self.board_state),
                           "mv_dir":poss_mv,
                           "path_cost":current_board["path_cost"] + 1}
            child_board_dicts.append(child_board)
        return child_board_dicts







if __name__ == "__main__":
    pass 