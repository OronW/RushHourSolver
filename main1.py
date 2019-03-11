from Play_tools import Vehicle, Board
from State import State
from Astar1 import Astar
from Node1 import Node
import hashlib
from collections import defaultdict
from heapq import heappush as push
from heapq import heappop as pop
import FibonacciHeap1 as fh
from time import time

class Temp():


    def __init__(self, n, value):
        self.name = n
        self.key = value

    def print(self):
        print("Name: "+self.name)
        print("Key: ",self.key)


def solveAll(T=30, H=3, printSolution=False, printTime=True):
    if (H==1):
        heuristic="H1"
    elif (H==2):
        heuristic = "H2"
    else:
        heuristic = "H3"

    total_time = 0
    count = 0
    total_steps =0
    i=0
    with open("puzzles.txt") as fh:
        puzzle = fh.readline()
        while puzzle:
            p = Board(puzzle.rstrip('\n'))
            A = Astar(p, 200000)
            t = A.solveHeap(T, H, False)
            # SUCCESS: t = [ SOLN    ,    time   ]
            #                  0            1
            # FAIL: t=-1
            id = i+1

            if (t==None):
                print("Puzzle:",id," Failed")
            else:

                time =  t[2]
                soln = t[0]
                steps = t[1]

                if (printTime):
                    print("Puzzle: ", id, " solved in:", time, " seconds.")
                if (printSolution):
                    print("Puzzle: ", id, " solution:", soln)
                    print("Number of steps: ", steps)

                total_time+=time
                count+=1
                total_steps+=steps
                i+=1
                puzzle = fh.readline()
        fh.close()


    print("========================")
    print("Totals for: "+heuristic)
    print("Solved ", count, " puzzles in ", total_time, " seconds.")
    print("Average solve time: ",total_time/count, " Average solution length: ", total_steps/count)




def defaultTime():
    return 16

def getAverageTime(T=30, H=3):
    if (H==1):
        heuristic="H1"
    elif (H==2):
        heuristic = "H2"
    else:
        heuristic = "H3"

    print("Statistics for "+heuristic+" By Level:")
    print("")

    total = 0
    count = 0
    steps=0
    for i in range(0, 10):
        p = Puzzle(i)
        A = Astar(p, 200000)
        t = A.solveHeap(T, H, False, False, True)
        # SUCCESS: t =     depth , time
        #
        # FAIL: t=-1


        if (isinstance(t,list)):
            total += t[1]
            count += 1
            steps+=t[0]

    print("Beginner Stats:")
    print("Solved: ", count)
    print("Average time: ", total/count)
    print("Average steps: ",steps/count)
    print("=============================")
    total = 0
    count = 0
    steps = 0
    for i in range(10, 20):
        p = Puzzle(i)
        A = Astar(p, 200000)
        t = A.solveHeap(T, H, False, False, True)
        # SUCCESS: t =     time
        #
        # FAIL: t=-1

        if (isinstance(t,list)):
            total += t[1]
            count += 1
            steps+=t[0]

    print("Intermediate Stats:")
    print("Solved: ", count)
    print("Average time: ", total / count)
    print("Average steps: ", steps / count)
    print("=============================")
    total = 0
    count = 0
    steps = 0
    for i in range(20, 30):
        p = Puzzle(i)
        A = Astar(p, 200000)
        t = A.solveHeap(T, H, False, False, True)
        # SUCCESS: t =     time
        #
        # FAIL: t=-1

        if (isinstance(t,list)):
            total += t[1]
            count += 1
            steps+=t[0]

    print("Advanced Stats:")
    print("Solved: ", count)
    print("Average time: ", total / count)
    print("Average steps: ", steps / count)
    print("=============================")
    total = 0
    count = 0
    steps = 0
    for i in range(30, 40):
        p = Puzzle(i)
        A = Astar(p, 200000)
        t = A.solveHeap(T, H, False, False, True)
        # SUCCESS: t =     time
        #
        # FAIL: t=-1

        if (isinstance(t,list)):
            total += t[1]
            count += 1
            steps+=t[0]

    print("Expert Stats:")
    print("Solved: ", count)
    print("Average time: ", total / count)
    print("Average steps: ", steps / count)



def printAllStats(T=30, H=3):
    if (H == 1):
        heuristic = "H1"
    elif (H == 2):
        heuristic = "H2"
    else:
        heuristic = "H3"
    EBF=0
    depth_ratio=0
    avg_h = 0
    tree_depth = [0,0,0]
    puzzles=40
    avg_n=0
    for i in range(0, 40):
        p = Puzzle(i)
        A = Astar(p, 200000)
        S = A.solveHeap(T, H, True)
        # S:
        # [ebf, d/N ratio, average h, tree depth, N  time]
        #   0       1           2         3       4    5

        ebf = S[0]
        dN = S[1]
        h = S[2]
        depth = S[3]
        t = S[5]
        N = S[4]
        if (t>T):
            status='Failed'
        else:
            status='Solved'

        print("Statistics for puzzle:  ", i+1)
        print("Status: "+status)
        print("Time : ",t)
        print("EBF: ",ebf)
        print("Average Heuristic: ", h)
        print("depth ratio (d/N): ", dN)
        print("Number of nodes searched: ",N)
        print("Minimum depth: ",depth[0]," Average Depth: ",depth[1], "Max Depth: ",depth[2])
        EBF+=ebf
        depth_ratio+=dN
        avg_h += h
        avg_n+=N
        tree_depth[0] += depth[0]
        tree_depth[1] += depth[1]
        tree_depth[2] += depth[2]


    tree_depth[0] = tree_depth[0] / puzzles
    tree_depth[1] = tree_depth[1] / puzzles
    tree_depth[2] = tree_depth[2] / puzzles
    EBF = EBF/puzzles
    avg_h = avg_h / puzzles
    depth_ratio = depth_ratio / puzzles
    avg_n = avg_n/puzzles


    print("================================")
    print("Average Totals for: " + heuristic)
    print("Total EBF: ",EBF)
    print("Total Heuristic Average: ", avg_h)
    print("Total depth ratio (d/N): ", depth_ratio)
    print("Total Nodes (N): ", avg_n)
    print("Total Min search depth: ", tree_depth[0])
    print("Total Average search depth: ", tree_depth[1])
    print("Total Max search depth: ", tree_depth[2])


def run():
    print("Select an option:")
    print("1: Get solutions")
    print("2: Get solve times")
    print("3: Get solution statistics")
    # opt = input()
    # opt = int(opt)
    print("Choose an heuristic: (1/2/3)")
    # h = input()
    # h = int(h)
    t = defaultTime()
    # if (not isinstance(h, int)) or h < 0 or h > 3:
    #     print("Invalid heuristic input")
    #     return


    # if (opt==1):
        #Solutions:
    print("Solving with ",t," (default 16) Seconds limit...")
    solveAll(t,3,True,False)

    # elif (opt==2):
    #     #times
    #     print("Solving with ", t, " (default 16) Seconds limit...")
    #     solveAll(t, h, False, True)
    #
    # elif (opt==3):
    #     #statistics
    #     print("Solving with ", t, " (default 16) Seconds limit...")
    #     printAllStats(t, h)
    #
    # else:
    #     print("Invalid input")



def main():


    run()







if __name__ == "__main__": main()



