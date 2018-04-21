from base_board import eightBlock
import ipdb

class baseHeuristicSolver(eightBlock):

    def __init__(self, heuristic, start_state = None, goal_state = None):
        '''
        This class only contains the methods for calculating any possible 
        heuristic that we might want to use. Each of these heuristic methods 
        will be bound to the attribute `calculate_heuristic` via a string.

        The only rule for heuristics that I see right now is that they need
        to support a board = None default like get_misplaced_values() and
        get_row()
        '''
        super().__init__(start_state, goal_state)
        #TKTK COULD BE A VALID METHOD
        self.h_dict = {"hamming": self.hamming_distance,
                       "manhattan": self.manhattan_distance}
        #TKTK COULD BE A VALIDATE HEURISTIC METHOD
        if heuristic not in self.h_dict.keys():
            h_tried = "Tried to use heuristic {}.".format(heuristic)
            valids = ", ".join([v for v in self.h_dict.keys()])
            h_valid = "Must be one of {}.".format(valids)
            e_msg = " ".join([h_tried, h_valid])
            raise NotImplementedError(e_msg)
        self.calculate_heuristic = self.h_dict[heuristic]

    def hamming_distance(self, board = None):
        '''Compares a given board state to the goal state and returns the
        number of misplaced tiles, excluding zero. If no board state is 
        given, we simply compare with the current board state
        '''
        return len(self.get_misplaced_values(board))

    def manhattan_distance(self, board = None):
        '''Compares a given board state to the goal state and returns the
        sum of manhattan distances for each misplaced tile. If no board state 
        is given, we simply compare with the current board state
        '''
        m_dist = 0
        for v in self.get_misplaced_values(board):
            m_dist += abs(self.get_row(v, board) - self.get_row(v, self.goal_state))
            m_dist += abs(self.get_col(v, board) - self.get_col(v, self.goal_state))
        return m_dist

class bestFirstSolver(baseHeuristicSolver):

    def __init__(self, heuristic, start_state = None, goal_state = None):
        '''
        '''
        super().__init__(heuristic, start_state, goal_state)
        self.path_map = {}
        self.prty_queue = [{"child":self.board_state,
                            "parent":None,
                            "path_cost":0,
                            "heuristic":self.calculate_heuristic()}]

    



if __name__ == "__main__":
    herp = [3,2,1,4,5,6,7,0,8]
    derp = [1,2,3,4,5,6,7,8,0]
    foo = baseHeuristicSolver("hamming", herp, derp)
    ipdb.set_trace()