from base_board import eightBlock
import ipdb

'''
each of these can be initialized from an eight block
class, but we might also want to reserve the right to
call different heuristics as well
'''

class baseHeuristicSolver(eightBlock):

	def __init__(self, heuristic, start_state = None, goal_state = None):

		super().__init__(start_state, goal_state)
		self.h_dict = {"misplaced_tiles": self.get_misplaced_values,
					   "manhattan_distance": self.manhattan_distance}
		if heuristic not in self.h_dict.keys():
			h_tried = "Tried to use heuristic {}.".format(heuristic)
			valids = ", ".join([v for v in self.h_dict.keys()])
			h_valid = "Must be one of {}.".format(valids)
			e_msg = " ".join([h_tried, h_valid])
			raise NotImplementedError(e_msg)



	def manhattan_distance(self):
		pass


if __name__ == "__main__":
	print("shoop-a-doop")
	foo = baseHeuristicSolver("misplaced_tiles")
	ipdb.set_trace()