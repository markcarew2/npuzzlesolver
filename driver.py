"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
"""

import sys

import queue as Q

import time

import sys

import math

from dataclasses import dataclass, field

from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

### Students need to change the method to have the corresponding parameters


def writeOutput(solvedPuzzleNode, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    cost = str(solvedPuzzleNode.cost)
    print(cost)
    actions = []

    while(solvedPuzzleNode.parent!=None):
        actions.append(solvedPuzzleNode.action)
        solvedPuzzleNode = solvedPuzzleNode.parent
    actions.reverse()

    actions = str(actions)

    with open("output.txt",'w') as f:
        print("path_to_goal: " + actions + "\n" + "cost_of_path: " + cost + "\n" + "nodes_expanded: " + str(nodes_expanded) + "\n" + "search_depth: " + str(search_depth) + "\n" + "max_search_depth: " + str(max_search_depth) + "\nrunning_time: " + str(running_time) + "\nmax_ram_usage: " + str(max_ram_usage))

        f.write("path_to_goal: " + actions + "\n" + "cost_of_path: " + cost + "\n" + "nodes_expanded: " + str(nodes_expanded) + "\n" + "search_depth: " + str(search_depth) + "\n" + "max_search_depth: " + str(max_search_depth) + "\nrunning_time: " + str(running_time) + "\nmax_ram_usage: " + str(max_ram_usage))

def bfs_search(initial_state):

    """BFS search"""
    startTime = time.time()

    
    frontier= Q.Queue()
    frontier.put(initial_state)

    explored = set()
    explored.add(initial_state.config)
    nodes_expanded = 0
    max_search_depth = 0

    while(frontier!=None):
        target = frontier.get()

        if (test_goal(target)):
            search_depth = target.cost
            runningTime = time.time() - startTime
            
            if sys.platform == "win32":
                import psutil
                max_ram_usage = psutil.Process().memory_info().rss/1048576
            #else:
                #import resource
                #max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            writeOutput(target, nodes_expanded, search_depth,max_search_depth,runningTime,max_ram_usage)
            break

        target.expand()
        nodes_expanded += 1

        for child in target.children:
            if (child.config in explored):
                pass
            else:
                if (max_search_depth < child.cost):
                    max_search_depth = child.cost
                frontier.put(child)
                explored.add(child.config)



def dfs_search(initial_state):

    """DFS search"""

    startTime = time.time()

    
    frontier= Q.LifoQueue()
    frontier.put(initial_state)

    explored = set()
    explored.add(initial_state.config)
    nodes_expanded = 0
    max_search_depth = 0

    while(frontier!=None):
        target = frontier.get()
        
        if (test_goal(target)):
            search_depth = target.cost
            runningTime = time.time() - startTime
            
            if sys.platform == "win32":
                import psutil
                max_ram_usage = psutil.Process().memory_info().rss/1048576
            #else:
                #import resource
                #max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            writeOutput(target, nodes_expanded, search_depth,max_search_depth,runningTime,max_ram_usage)
            break

        target.expand()
        nodes_expanded += 1
        target.children.reverse()

        for child in target.children:
            if (child.config in explored):
                pass
            else:
                if (max_search_depth < child.cost):
                    max_search_depth = child.cost
                frontier.put(child)
                explored.add(child.config)

def A_star_search(initial_state):

    """A * search"""

    startTime = time.time()

    childmd = 0
    for idx, value in enumerate(initial_state.config):
        md = calculate_manhattan_dist(idx,value,initial_state.n)
        childmd += md
    
    initial_state.fcost = childmd
    
    frontier = Q.PriorityQueue()
    pnode = PrioritizedItem(initial_state.fcost, initial_state)
    frontier.put(pnode)

    explored = set()
    frontierstates = set()
    frontierstates.add(initial_state.config)
    nodes_expanded = 0
    max_search_depth = 0

    while(frontier!=None):
        targetItem = frontier.get()
        target = targetItem.item
        frontierstates.remove(target.config)
        explored.add(target.config)

        if (test_goal(target)):
            search_depth = target.cost
            runningTime = time.time() - startTime
            
            if sys.platform == "win32":
                import psutil
                max_ram_usage = psutil.Process().memory_info().rss/1048576
            #else:
                #import resource
                #max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            writeOutput(target, nodes_expanded, search_depth,max_search_depth,runningTime,max_ram_usage)
            break

        target.expand()
        nodes_expanded += 1

        for child in target.children:
            if (child.config in frontierstates):

                for idx, value in enumerate(child.config):
                    md = calculate_manhattan_dist(idx,value,child.n)
                    childmd += md
                child.fcost = child.cost + childmd

                for ch in frontier.queue:
                    if(ch.item.config==child.config and ch.item.fcost<child.fcost):
                        ch.priority = math.inf
                        pnode = PrioritizedItem(child.fcost, child)
                        frontier.put(pnode)

            elif(child.config in explored):
                pass

            else:
                if (max_search_depth < child.cost):
                    max_search_depth = child.cost
                childmd = 0

                for idx, value in enumerate(child.config):
                    md = calculate_manhattan_dist(idx,value,child.n)
                    childmd += md

                child.fcost = child.cost + childmd
                pnode = PrioritizedItem(child.fcost, child)
                frontier.put(pnode)
                frontierstates.add(child.config)
                
def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""
    cost = 0
    while(state.parent != None):
        cost += 1
        state = state.parent
    
    return cost
    
def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""
    if (value!=0):
        idxcol = idx % n
        idxrow = idx // n

        valuecol = value % n
        valuerow = value // n

        distance = abs(idxcol - valuecol) + abs(idxrow - valuerow)

        return distance
    else:
        return 0


def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    if puzzle_state.config == tuple(range(puzzle_state.n**2)):
        return True

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    
    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")
    


if __name__ == '__main__':

    main()