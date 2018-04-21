from base_board import eightBlock



class eightBlockSolver(eightBlock):

    def __init__(self, start_state = None, goal_state = None):
    	'''Initializes an eightBlock and then defines two additional
        class attributes needed to reach and keep track of solution
        paths

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
    	self.children_boards = [{"child":self.board_state,
    	                         "parent":None,
    	                         "path_cost":0}]





if __name__ == "__main__":
    pass 