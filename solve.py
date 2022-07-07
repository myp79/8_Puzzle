from math import sqrt

from time import perf_counter

from functools import wraps

import tracemalloc


def time_and_memory(func):
    '''
    Measurment of time and memory space
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        tracemalloc.start()
        ret = func(*args, **kwargs)
        space = tracemalloc.get_tracemalloc_memory()
        tracemalloc.stop()
        return ret, perf_counter() - start, space/(1024)
    return wrapper


class Node:
    '''
    Nodes of problem that produce from a state
    '''

    def __init__(self, state: list, move: str, cost: int, path_cost: int, depth: int, parent):
        self.state = state
        self.move = move
        self.cost = cost
        self.path_cost = path_cost
        self.depth = depth
        self.parent = parent

    def print_move(self):
        moves = []
        while self.parent != None:
            moves.append(self.move)
            self = self.parent
        return moves[::-1]


class EightPuzzleProblem:
    def __init__(self, start_pos, goal_pos=[0, 1, 2, 3, 4, 5, 6, 7, 8]):
        '''
        Given start and goal position for solve problem.
        '''
        self.start_pos = Node(start_pos, None, 0, 0, 0, None)
        self.goal_pos = goal_pos

    def is_goal(self, state):
        '''
        Return the proble is solve or not
        '''
        return self.goal_pos == state

    def find_empty(self, state):
        '''
        Return empty index (position of 0) in our list for each step
        '''
        return state.index(0)

    def swap(self, current_pos: Node, move: int):
        '''
        Swap the zero
        '''
        state = current_pos.state
        empty = self.find_empty(state)
        new_state = state.copy()
        new_state[empty], new_state[empty +
                                    move] = new_state[empty + move], new_state[empty]
        return (new_state, new_state[empty])

    def get_actions(self, current_pos: Node):
        '''
        Return the list of avilable actions for current position
        '''
        avilable_actions = ['U', 'D', 'R', 'L']
        empty = self.find_empty(current_pos.state)
        if empty in [0, 1, 2]:
            avilable_actions.remove('U')

        if empty in [6, 7, 8]:
            avilable_actions.remove('D')

        if empty in [2, 5, 8]:
            avilable_actions.remove('R')

        if empty in [0, 3, 6]:
            avilable_actions.remove('L')

        return avilable_actions

    def generate_node(self, current_pos: Node, move):
        '''
        Generate nodes of problem for avilable actions
        '''
        moves = {'U': -3, 'D': 3, 'R': 1, 'L': -1}  # index swap for list
        new_state, cost = self.swap(current_pos, moves[move])
        new_node = Node(new_state, move, cost, cost +
                        current_pos.path_cost, current_pos.depth+1, current_pos)

        return new_node

    def get_nodes(self, current_pos: Node):
        '''
        Get all nodes that make
        '''
        nodes = []
        for move in self.get_actions(current_pos):
            new_node = self.generate_node(current_pos, move)
            if move == 'U':
                nodes.append(new_node)
            if move == 'D':
                nodes.append(new_node)
            if move == 'R':
                nodes.append(new_node)
            if move == 'L':
                nodes.append(new_node)
        return nodes


class Heuristic:
    def manhattan(self, state):
        '''
        Calculate Manhattan distance for state
        '''
        goal = self.goal_pos

        return sum(abs(goal[i]//3-state[i]//3) +
                   abs(goal[i] % 3-state[i] % 3) for i in range(0, 9) if goal[i] != state[i])

    def misplace(self, state):
        '''
        Return sum of misplace items in current position from goal_position
        '''
        return sum([1 for i in range(0, 9) if state[i] != self.goal_pos[i]])

    def euclidean(self, state):
        '''
        Return Euclidean from of distance for items in current position from goal_position
        '''
        goal = self.goal_pos
        return sum([sqrt((goal[i]//3 - state[i]//3)**2 + (goal[i] % 3 - state[i] % 3)**2)
                    for i in range(0, 9) if goal[i] != state[i]])


class IDAstar(EightPuzzleProblem, Heuristic):
    def __init__(self, start_pos, heuristic):
        super().__init__(start_pos)
        self.h = heuristic

    @time_and_memory
    def solve(self):
        '''
        Solving problem and return false if not possible
        '''
        prev_states = [self.start_pos.state]
        queue = [self.start_pos]
        nodes_pop = 0
        max_queue = 0

        while len(queue) > 0:
            max_queue = max(max_queue, len(queue))
            current_node = queue.pop()
            nodes_pop += 1

            if self.is_goal(current_node.state):
                return True, nodes_pop, max_queue, current_node.depth, current_node

            next_state = self.get_nodes(current_node)
            for node in next_state:
                if node.state not in prev_states:
                    prev_states.append(node.state)
                    queue.append(node)
            if self.h == 'manhatan':
                queue.sort(key=lambda node: node.depth +
                           self.manhattan(node.state), reverse=True)
            elif self.h == 'misplace':
                queue.sort(key=lambda node: node.depth +
                           self.misplace(node.state), reverse=True)
            else:
                queue.sort(key=lambda node: node.depth +
                           self.euclidean(node.state), reverse=True)

        return False


class Astart(EightPuzzleProblem, Heuristic):
    def __init__(self, start_pos, heuristic):
        super().__init__(start_pos)
        self.h = heuristic

    @time_and_memory
    def solve(self):
        prev_states = [self.start_pos.state]
        queue = [self.start_pos]
        nodes_pop = 0
        max_queue = 0

        while len(queue) > 0:
            max_queue = max(max_queue, len(queue))
            current_node = queue.pop()
            nodes_pop += 1

            if self.is_goal(current_node.state):
                return True, nodes_pop, max_queue, current_node.depth, current_node

            next_state = self.get_nodes(current_node)
            for node in next_state:
                if node.state not in prev_states:
                    prev_states.append(node.state)
                    queue.append(node)
            if self.h == 'manhattan':
                queue.sort(key=lambda node: node.path_cost +
                           self.manhattan(node.state), reverse=True)
            elif self.h == 'misplace':
                queue.sort(key=lambda node: node.path_cost +
                           self.misplace(node.state), reverse=True)
            else:
                queue.sort(key=lambda node: node.path_cost +
                           self.euclidean(node.state), reverse=True)

        return False


class UCS(EightPuzzleProblem):
    def __init__(self, start_pos):
        super().__init__(start_pos)

    @time_and_memory
    def solve(self):
        prev_states = [self.start_pos.state]
        queue = [self.start_pos]
        nodes_pop = 0
        max_queue = 0

        while len(queue) > 0:
            max_queue = max(max_queue, len(queue))
            current_node = queue.pop()
            nodes_pop += 1

            if self.is_goal(current_node.state):
                return True, nodes_pop, max_queue, current_node.depth, current_node

            next_state = self.get_nodes(current_node)
            for node in next_state:
                if node.state not in prev_states:
                    prev_states.append(node.state)
                    queue.append(node)
            queue.sort(key=lambda node: node.path_cost, reverse=True)

        return False


class IDS(EightPuzzleProblem):
    def __init__(self, start_pos):
        super().__init__(start_pos)

    @time_and_memory
    def solve(self):
        max_depth = 50
        nodes_pop = 0
        max_stack = 0

        for depth in range(0, max_depth):
            prev_states = [self.start_pos.state]
            stack = [self.start_pos]
            while len(stack) > 0:
                max_stack = max(max_stack, len(stack))
                current_node = stack.pop()
                nodes_pop += 1

                if self.is_goal(current_node.state):
                    return True, nodes_pop, max_stack, current_node.depth, current_node

                next_state = self.get_nodes(current_node)
                for node in next_state:
                    if node.depth < depth:
                        if node.state not in prev_states:
                            prev_states.append(node.state)
                            stack.append(node)

        return False
