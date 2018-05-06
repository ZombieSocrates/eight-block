import random
import ipdb
import time

from non_heuristic import depthFirstSearchSolver, breadthFirstSearchSolver, \
iterativeDeepeningSolver
from heuristic import bestFirstSearchSolver, aStarSearchSolver


if __name__ == "__main__":

    # TKTK look at Tori's assignment and copy the EASY, MEDIUM, HARD, and 
    # GOAL states
    
    #1: Create initial board and goal board
    case_dict = {
                "easy":
                    {
                    "start":[1,3,4,8,6,2,7,0,5],
                    "goal": [1,2,3,8,0,4,7,6,5]
                    },
                "medium":
                    {
                    "start":[2,8,1,0,4,3,7,6,5],
                    "goal": [1,2,3,8,0,4,7,6,5]
                    },
                "hard":
                    {
                    "start":[5,6,7,4,0,8,3,2,1],
                    "goal": [1,2,3,8,0,4,7,6,5]
                    },        
                "unsolveable":
                    {
                    "start":[3,2,1,8,0,4,7,6,5],
                    "goal": [1,2,3,8,0,4,7,6,5]
                    }
                }

    #2. Initialize solver for each algorithm
    for k in case_dict.keys():
        DFS = depthFirstSearchSolver(case_dict[k]["start"], \
            case_dict[k]["goal"])
        BFS = breadthFirstSearchSolver(case_dict[k]["start"], \
            case_dict[k]["goal"])
        IDS = iterativeDeepeningSolver(case_dict[k]["start"], \
            case_dict[k]["goal"])
        GREEDY_hm = bestFirstSearchSolver("hamming", case_dict[k]["start"], \
            case_dict[k]["goal"])
        GREEDY_mn = bestFirstSearchSolver("manhattan", case_dict[k]["start"], \
            case_dict[k]["goal"])
        ASTAR_hm = aStarSearchSolver("hamming", case_dict[k]["start"], \
            case_dict[k]["goal"])
        ASTAR_mn = aStarSearchSolver("manhattan", case_dict[k]["start"], \
            case_dict[k]["goal"])
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
            t0 = time.time()
            sln = solver.solve(verbose = True)
            t1 = time.time()
            print("{} case end state reached in {:.2f} seconds".format(\
                k.title(),t1-t0))
            nm = type(solver).__name__
            if hasattr(solver, "heuristic"):
                nm += "_{}".format(solver.heuristic)
            cst = len(sln) if sln else "N/A"
            print("Solution cost for {}: {}".format(nm, cst))
            print("---"*15)

        ipdb.set_trace()




    