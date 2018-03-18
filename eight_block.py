import random
import ipdb


class eightBlock():

	def __init__(self, positions = None):
		'''The most important step in this initial init is defining the initial 
		board configuration. Calling init with no positions will just randomly 
		shuffle valid_vals. Otherwise, we'll start with the positions given, 
		assuming it is a list containing only integers 0 through 8
		'''
		self.valid_vals = [i for i in range(9)]
		self.valid_inds = [i for i in range(3)]
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
			
	def display_board(self):
		'''shows the current board configuration
		'''
		for r in range(len(self.valid_inds)):
			print(self.board_config[3*r:3*(r + 1)])

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

	def get_misplaced_values(self):
		'''scans self.board_config and returns a list of misplaced values
		against the assumed goal state of [1,2,3,4,5,6,7,8,0].

		By extension, this will return an empty list if the board is solved
		'''
		misplaced = []
		for v in self.board_config:
			if (v == 0) and (self.board_config.index(v) != 8):
				misplaced.append(v)
			elif (v != 0) and (self.board_config.index(v) != (v - 1)):
				misplaced.append(v)
		return misplaced


if __name__ == "__main__":
    
    foo = eightBlock()
    # Try to display the board properly
    foo.display_board()

    # Check that you can index into things properly
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

    ipdb.set_trace()

    # Try to move the empty slot one space

    