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
			if set(positions) == set(self.valid_vals):
				self.board_config = positions
			else:
				v_msg = "positions must only contain 0 through 8"
				raise ValueError(v_msg)
		else:
			t_msg = "positions must be a list, not {}".format(type(positions))
			raise TypeError(t_msg)
			
	def display_board(self):
		'''shows the current board configuration
		'''
		for r in range(len(self.valid_inds)):
			print(self.board_config[3*r:3*(r+1)])


if __name__ == "__main__":
	ipdb.set_trace()
    # Try to display the board properly


    # Try to move the empty slot one space

    # Boolean to test whether the board is solved