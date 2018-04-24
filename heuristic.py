from base_solver import eightBlockSolver
import ipdb

class baseHeuristicSolver(eightBlockSolver):

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
        for child in self.children_list:
            self.add_heuristic_tag(child)

    def add_heuristic_tag(self, child):
        '''Given a dictionary in self.children_list, will simply add the
        agreed upon heuristic value to that dictionary, based on whatever the
        board configuration of that dictionary is.
        '''
        if not isinstance(child, dict) or "child" not in child.keys():
            raise NotImplementedError
        child["heuristic"] = self.calculate_heuristic(child["child"])

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

    def get_priority(self, candidate_child):
        '''For best first search, we're only prioritizing based on
        the value of what the heuristic is. Given any child_dict, this helper
        method returns that value
        '''
        return candidate_child["heuristic"]

    def tag_and_sort_children(self, list_of_children):
        '''Given the output of self.get_children, this method will simply
        add the heuristic tag to each item and then sort them so that the
        one with the lowest heuristic value goes first
        '''
        for child in list_of_children:
            self.add_heuristic_tag(child)
        return sorted(list_of_children, key = lambda v: self.get_priority(v))

    def place_in_priority_queue(self, new_children):
        '''Given a sorted list of candidate new children, this method will
        sift those children into the existing children_list in priority
        order, terminating once every object in new_children has been
        integrated within children_list

        TKTK: If this is horribly slow, Tori suggested trying to implement
        binary search for find the proper place
        '''
        for i, child_dict in enumerate(self.children_list):
            if new_children[0]["heuristic"] <= self.get_priority(child_dict):
                insert_child = new_children.pop(0)
                self.children_list.insert(i, insert_child)
                if not new_children:
                    return
        self.children_list.extend(new_children)



if __name__ == "__main__":
    herp = [3,2,1,4,5,6,7,0,8]
    derp = [1,2,3,4,5,6,7,8,0]
    foo = bestFirstSolver("hamming", herp, derp)
    ipdb.set_trace()
    print("Continue on to test of heuristic methods")
    print("existing")
    print(foo.children_list)
    bar = foo.get_children(foo.children_list[0])
    bar = foo.tag_and_sort_children(bar)
    print("to_add")
    print(bar)
    foo.place_in_priority_queue(bar)
    print("result")
    print(foo.children_list)