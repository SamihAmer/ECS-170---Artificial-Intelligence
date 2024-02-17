import streamlit as st
from typing import List, Tuple, Dict, Callable
from copy import deepcopy

####
# Code from Module 1
####

MOVES = [(0,-1), (1,0), (0,1), (-1,0)]
COSTS = { '🌾': 1, '🌲': 3, '⛰': 5, '🐊': 7, '🗻': 99999}

full_world = [
['🌾', '🌾', '🌾', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🗻', '🗻', '🗻', '🗻', '🗻', '🗻', '🗻', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🗻', '🗻', '🗻', '⛰', '⛰', '⛰', '🗻', '🗻', '⛰', '⛰'],
['🌾', '🌾', '🌾', '🌾', '⛰', '🗻', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🐊', '🐊', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '⛰', '🌾'],
['🌾', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '🌲', '🌲', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '⛰', '🗻', '🗻', '🗻', '⛰', '🌾'],
['🌾', '⛰', '⛰', '⛰', '🗻', '🗻', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🗻', '⛰', '🌾', '🌾'],
['🌾', '⛰', '⛰', '🗻', '🗻', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '⛰', '🗻', '🗻', '🗻', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🗻', '🗻', '🗻', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾'],
['⛰', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '🌾', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾'],
['⛰', '⛰', '🌾', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '⛰', '🗻', '🗻', '🗻', '🗻', '🌾', '🌾', '🌾', '🐊', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '⛰', '⛰', '🗻', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '🗻', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🌾', '🌾', '⛰', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾'],
['🐊', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '⛰', '🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '🌾', '⛰', '🗻', '⛰', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌲', '🌲', '⛰', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🗻', '🌾', '🌾', '🌲', '🌲', '🌲', '🌲', '⛰', '⛰', '⛰', '⛰', '🌾', '🐊', '🐊', '🐊', '🌾', '🌾', '⛰', '🗻', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🗻', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🗻', '🗻', '🗻', '⛰', '⛰', '🌾', '🐊', '🌾', '⛰', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🗻', '🗻', '🗻', '🌾', '🌾', '🗻', '🗻', '🗻', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🗻', '🗻', '🗻', '🗻', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🗻', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾'],
['🌾', '🌾', '🌾', '🌾', '🗻', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '🗻', '🗻', '🌲', '🌲', '🌲', '🌲', '🌲', '🌾', '🗻', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🗻', '🗻', '🗻', '🌲', '🌲', '🗻', '🗻', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🗻', '🗻', '🗻', '🗻', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🌾', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊', '🐊'],
['🌾', '⛰', '⛰', '🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '⛰', '⛰', '🌾', '🐊', '🐊', '🐊', '🐊', '🐊'],
['⛰', '🗻', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🗻', '🗻', '🗻', '⛰', '⛰', '🗻', '🗻', '🌾', '🗻', '🗻', '⛰', '⛰', '🐊', '🐊', '🐊', '🐊'],
['⛰', '🗻', '🗻', '🗻', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '🗻', '🗻', '🗻', '🗻', '⛰', '⛰', '⛰', '⛰', '🗻', '🗻', '🗻', '🐊', '🐊', '🐊', '🐊'],
['⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾', '🌾', '⛰', '⛰', '⛰', '🌾', '🌾', '🌾']
]

def find_successors(point: Tuple[int,int], world: List[List[str]], moves: List[Tuple[int,int]]):
    successors = []
    for move in moves:
        new_point = (point[0] + move[0], point[1] + move[1])
        if new_point[0] < 0 or new_point[1] < 0:
            continue
        elif new_point[0] >= len(world) or new_point[1] >= len(world[0]):
            continue
        successors.append(new_point)
    return successors

def heuristic(start: Tuple[int,int], goal: Tuple[int,int]): # you can add formal parameters
    return round(pow(pow(abs(start[0] - goal[0]),2) + pow(abs(start[1] - goal[1]),2), 1/2),0)

def get_complex_cost_from_path(path: List[Tuple[int,int]], costs: Dict[str, int], world: List[List[str]], goal: Tuple[int, int]):
    return sum([costs[world[point[0]][point[1]]] + heuristic(point, goal) for point in path])

def get_cost_from_path(path: List[Tuple[int,int]], costs: Dict[str, int], world: List[List[str]], goal: Tuple[int, int]):
    return sum([costs[world[point[0]][point[1]]] for point in path])

def get_cheapest_point_index(points: List[Tuple[int,int]], costs: Dict[str, int], world: List[List[str]], goal: Tuple[int, int]):
    min = 99999
    min_index = -1
    for i in range(len(points)):
        complex_cost = get_complex_cost_from_path([points[i]], costs, world, goal)
        if complex_cost < min:
            min = complex_cost
            min_index = i
    return min_index

def get_cleaned_sorted_path(path: List[Tuple[int,int]], start: Tuple[int, int], goal: Tuple[int, int], moves: List[Tuple[int, int]]):
    final = [goal]
    start_found = False
    previous_current = [goal]
    current = goal
    working_path = deepcopy(path)
    checked = []
    while (start_found == False and len(working_path) > 0):
        if current == start:
            start_found = True
        moves_accepted = False
        for move in moves:
            new_point = (current[0] + move[0], current[1] + move[1])
            if not new_point in working_path or new_point in final or new_point in checked:
                continue
            moves_accepted = True
            previous_current.append(current)
            current = new_point
            checked.append(current)
            final.append(current)
            working_path.remove(current)
        if moves_accepted == False:
            if current in final:
                final.remove(current)
            current = previous_current.pop()
    final.append(start)
    return final[::-1]

def a_star_search(world: List[List[str]], start: Tuple[int, int], goal: Tuple[int, int], costs: Dict[str, int], moves: List[Tuple[int, int]], heuristic: Callable) -> List[Tuple[int, int]]:
    explored = [start]
    frontier = find_successors(start, world, moves)
    goal_found = False
    while len(frontier) > 0 and goal_found == False:
        cheapest_point = frontier.pop(get_cheapest_point_index(frontier, costs, world, goal))
        for s in find_successors(cheapest_point, world, moves):
            if s[0] == goal[0] and s[1] == goal[1]:
                goal_found = True
                explored.append(s)
                break
            if s in explored:
                continue
            frontier.append(s)
        if cheapest_point in explored:
            continue
        explored.append(cheapest_point)
    return get_cleaned_sorted_path(explored, start, goal, moves)

def pretty_print_path(world: List[List[str]], path: List[Tuple[int, int]], start: Tuple[int, int], goal: Tuple[int, int], cost: Dict[str, int]) -> int:
    directions = { (0,1):'⏩', (0,-1):'⏪', (-1,0):'⏫', (1,0):'⏬' }
    finish = '🎁'
    p_world = deepcopy(world)
    previous_point = None
    for point in path:
        if point == start:
            previous_point = point
            continue
        diff = (point[0] - previous_point[0], point[1] - previous_point[1])
        p_world[previous_point[0]][previous_point[1]] = directions[diff]
        previous_point = point
        if point == goal:
            p_world[goal[0]][goal[1]] = finish
            break
    return p_world

####
# Begin new code
####

# title and state info
st.title('A* Search')
state_info = st.text('The world to traverse:')

# basic world traversal setup
full_start = (0, 0)
full_goal = (len(full_world[0]) - 1, len(full_world) - 1)
full_path = []

# default world
final_map_row_list = pretty_print_path(full_world, [], full_start, full_goal, COSTS)

# controls in a sidebar
with st.sidebar:
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'max' not in st.session_state:
        st.session_state.max = 0
    if 'start' not in st.session_state:
        st.session_state.start = (0,0)
    if 'goal' not in st.session_state:
        st.session_state.goal = (len(full_world[0]) - 1, len(full_world) - 1)
    ### buttons and values for interacting
    # user input start and goal:
    start_r = st.number_input('Start row', min_value=0, max_value=(len(full_world[0]) - 1), value=0)
    start_c = st.number_input('Start column', min_value=0, max_value=(len(full_world) - 1), value=0)
    goal_r = st.number_input('Goal row', min_value=0, max_value=(len(full_world[0]) - 1), value=(len(full_world[0]) - 1))
    goal_c = st.number_input('Goal column', min_value=0, max_value=(len(full_world) - 1), value=(len(full_world) - 1))
    full_start = (start_r, start_c)
    full_goal = (goal_r, goal_c)
    # buttons to move the solution along
    solve = st.button('Solve it')
    reset = st.button('Reset')
    decrement = st.button('Previous Step')
    increment = st.button('Next Step')
    # reset if reset button pressed or we change the start or goal
    if reset or not st.session_state.start == full_start or not st.session_state.goal == full_goal:
        st.session_state.step = 0
        st.session_state.max = 0
    if increment and not st.session_state.step + 1 == st.session_state.max:
        st.session_state.step += 1
    if decrement and not st.session_state.step == 0:
        st.session_state.step -= 1
    # run the actual path finding algorithm
    full_path = a_star_search(full_world, full_start, full_goal, COSTS, MOVES, heuristic)
    st.session_state.max = len(full_path)
    # this if else shows the full solution or shows the incremental solution
    if solve:
        adjusted_path = full_path
        st.session_state.step = st.session_state.max - 1
    else:
        adjusted_path = [full_path[x] for x in range(int(st.session_state.step + 1))]
    # show what step count we have for the solution
    st.write('Step = ', st.session_state.step)
    # find the path given all the parameters leading up to this
    final_map_row_list = pretty_print_path(full_world, adjusted_path, full_start, full_goal, COSTS)

# print the world - with whatever traversal steps applied
for line in final_map_row_list:
    st.text("".join(line) + "\n")
