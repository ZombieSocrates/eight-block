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

        TKTK First check here could be a `validate_child` method that returns
        nothing. Arguably it could belong to the "base solver" class
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

    def get_priority(self, candidate_child):
        '''This method will be implemented in child classes. How you define 
        "priority" is the only thing separating A* from Best First
        '''
        pass

    def tag_and_sort(self, list_of_children):
        '''Given the output of self.get_children, this method will simply
        add the heuristic tag to each item and then sort them so that the
        one with the lowest heuristic value goes first
        '''
        for child in list_of_children:
            self.add_heuristic_tag(child)
        return sorted(list_of_children, key = lambda v: self.get_priority(v))

    def scan_priority_queue(self, new_children):
        '''Given a sorted list of candidate new children, this method will
        sift those children into the existing children_list in priority
        order, terminating once every object in new_children has been
        integrated within children_list
        '''
        for i, child_dict in enumerate(self.children_list):
            try:
                candidate = new_children[0]
            except IndexError:
                return
            if self.get_priority(candidate) <= self.get_priority(child_dict):
                insert_child = new_children.pop(0)
                self.children_list.insert(i, insert_child)
        self.children_list.extend(new_children)

    def binary_search_tree_insertion(self, child, lwr = None, \
        upr = None):
        '''Uses a binary search tree method to find the best place to 
        insert child into list_of_children. Does so recursively and
        will modify list_of_children in place

        Ideally, this will help me implement a quicker method of ordering
        the priority queue than relying solely on the scanning method above
        '''
        lwr = 0 if lwr is None else lwr
        upr = len(self.children_list) if upr is None else upr
        if (upr - lwr) <= 1:
            comp_val = self.get_priority(self.children_list[lwr])
            loc = lwr if self.get_priority(child) <= comp_val else upr
            self.children_list.insert(loc, child)
        else:
            mid = int((lwr + upr)/2)
            comp_val = self.get_priority(self.children_list[mid])
            if self.get_priority(child) <= comp_val:
                self.binary_search_tree_insertion(child, lwr = lwr, upr = mid)
            else:
                self.binary_search_tree_insertion(child, lwr = mid, upr = upr)

    def bst_priority_queue(self, new_children):
        '''Given a sorted list of candidate new children, this method will 
        place them into the existing children_list using the binary search
        driven method above
        '''
        if not self.children_list:
            self.children_list.extend(new_children)
            return
        for child_dict in new_children:
            self.binary_search_tree_insertion(child_dict)

class bestFirstSearchSolver(baseHeuristicSolver):

    def get_priority(self, candidate_child):
        '''For best first search, we're only prioritizing based on
        the value of what the heuristic is. Given any child_dict, this helper
        method returns that value
        '''
        return candidate_child["heuristic"]

    def solve(self, verbose = False):
        '''TKTK document me
        '''
        while self.get_misplaced_values():
            curr_board = self.check_next_child()
            if curr_board is None:
                return curr_board
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution Found")
                return self.retrieve_solution_path()
            self.children_list.pop(0) 
            ranked_kids = self.tag_and_sort(self.get_children(curr_board))
            self.scan_priority_queue(ranked_kids)
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

class aStarSearchSolver(baseHeuristicSolver):

    def get_priority(self, candidate_child):
        '''For A-Star, we're prioritizing based on the sum of current cost plus
        the value of the heuristic. Given any child_dict, this helper
        method returns that value
        '''
        return candidate_child["heuristic"] + candidate_child["path_cost"]

    def solve(self, verbose = False):
        '''TKTK document me
        '''
        while self.get_misplaced_values():
            curr_board = self.check_next_child()
            if curr_board is None:
                return curr_board
            self.update_path_map(curr_board)
            if not self.get_misplaced_values():
                print("Solution Found")
                return self.retrieve_solution_path()
            self.children_list.pop(0) 
            ranked_kids = self.tag_and_sort(self.get_children(curr_board))
            self.scan_priority_queue(ranked_kids)
            if verbose and len(self.path_map) % 1000 == 0:
                print("Checked {} states".format(len(self.path_map)))

if __name__ == "__main__":
    pass