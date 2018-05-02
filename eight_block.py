import random
import ipdb

from non_heuristic import depthFirstSearchSolver, breadthFirstSearchSolver, \
iterativeDeepeningSolver
from heuristic import bestFirstSearchSolver, aStarSearchSolver


if __name__ == "__main__":

    # TKTK look at Tori's assignment and copy the EASY, MEDIUM, HARD, and 
    # GOAL states
    
    #1: Create initial board and goal board
    in_board = [1,3,4,8,6,2,7,0,5]
    goal_board = [1,2,3,8,0,4,7,6,5]

    #2. Initialize solver for each algorithm
    DFS = depthFirstSearchSolver(in_board, goal_board)
    BFS = breadthFirstSearchSolver(in_board, goal_board)
    IDS = iterativeDeepeningSolver(in_board, goal_board)
    GREEDY_hm = bestFirstSearchSolver("hamming", in_board, goal_board)
    GREEDY_mn = bestFirstSearchSolver("manhattan", in_board, goal_board)
    ASTAR_hm = aStarSearchSolver("hamming", in_board, goal_board)
    ASTAR_mn = aStarSearchSolver("manhattan", in_board, goal_board)

    ipdb.set_trace()
    solvers = [DFS, BFS, IDS, GREEDY_hm, GREEDY_mn, ASTAR_hm, ASTAR_mn]
    
    #3. Display, index, and goal-state check
    foo = random.choice(solvers)
    foo.display_board()
    for v in range(len(foo.valid_vals)):
        r = foo.get_row(v)
        c = foo.get_col(v)
        print("{} located at position ({},{})".format(v, r, c))
    wrongs = foo.get_misplaced_values()
    if not wrongs:
        print("Board is solved!")
    else:
        print("These are out of place: {}".format(wrongs))
    print("Getting ready to test each solver...")
    
    # Get solution for each and compare cost
    for solver in solvers:
        sln = solver.solve(verbose = True)
        nm = type(solver).__name__
        cst = len(sln) if sln else "N/A"
        print("Solution cost for {}: {}".format(nm, cst))
        ipdb.set_trace()




    