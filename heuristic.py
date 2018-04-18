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
        self.h_dict = {"hamming": self.hamming_distance,
                       "manhattan": self.manhattan_distance}
        if heuristic not in self.h_dict.keys():
            h_tried = "Tried to use heuristic {}.".format(heuristic)
            valids = ", ".join([v for v in self.h_dict.keys()])
            h_valid = "Must be one of {}.".format(valids)
            e_msg = " ".join([h_tried, h_valid])
            raise NotImplementedError(e_msg)
        self.calculate_heuristic = self.h_dict[heuristic]

    def hamming_distance(self, board = None):
        return len(self.get_misplaced_values(board))

    
            


if __name__ == "__main__":
    foo = baseHeuristicSolver("hamming")
    ipdb.set_trace()