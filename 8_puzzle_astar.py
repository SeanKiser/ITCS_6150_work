import random
from heapdict import heapdict
from collections import defaultdict

#this is a global variable for the goal state of the problem Used for testing
"""goal_state = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        

#global variable for checking the goal state used for testing
goal_state_tuple = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

# Creates a randomized 3x3 grid with numbers 0-8 where 0 is an empty space. used for testing
def create_initial_state():
    random_matrix = []
    numbers = list(range(9))
    random.shuffle(numbers)
    for i in range(3):   
        row = numbers[i*3:(i+1)*3]
        random_matrix.append(row)
    return random_matrix
"""



#calculate the heuristic for manhattan distance
def calculate_manhattan_h(matrix, goal):
    total_distance = 0 
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != 0:
                index_total = get_manhattan_distance(matrix[i][j], goal, i, j)
                total_distance += index_total
    
    return total_distance

#calculates manhattan distance
def get_manhattan_distance(num, goal, x, y):
    return abs(x - goal[num][0]) + abs(y - goal[num][1])


    

# Calculates the heuristic using number of misplaced tiles 
def calculate_misplaced_h(matrix, goal):
    total_misplaced = 0
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != 0:
                diff = matrix[i][j] - goal[i][j]
                if diff != 0:
                    total_misplaced += 1
    return total_misplaced 

#finds all of the neighbors for a given state
def get_neighbors(node):

    neighbors = []

    x, y = get_empty_position(node)

    moves = []

    if x > 0:
        moves.append((-1, 0))
    
    if x < 2: 
        moves.append((1, 0)) 
    
    if y > 0: 
        moves.append((0, -1))
    
    if y < 2:
        moves.append((0, 1))
        

    for move_x, move_y in moves:  
        new_x, new_y = x + move_x, y + move_y

        if isinstance(node, tuple):
            new_state = [list(row) for row in node]  # Convert each row from tuple to list
        else:
            new_state = [row[:] for row in node]

        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]

        
        new_state_tuple = tuple(tuple(state_row) for state_row in new_state)
        neighbors.append(new_state_tuple)
    
    return neighbors
                

#reconstructs the path from the a* search algorithm
def reconstruct_path(came_from, current_node, nodes_expanded, nodes_generated):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    path = path[::-1]

    print("initial state: \n")
    
    for i in path:
        for j in range(3):
            for k in range(3):
                print(i[j][k], end = "  ")
            print("\n", end = "")
        print("\n", end = "")
        print("   =>\n")

    print(f"Solution found!")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Nodes generated: {nodes_generated}")

    return path


#finds the coordinates of the empty space
def get_empty_position(node):
    for i in range(3):
        for j in range(3):
            if node[i][j] == 0:
                return (i, j)
    return None

#finds a specific tile
def find_tile(node, tile):
    for i in range(3):
        for j in range(3):
            if node[i][j] == tile:
                return (i, j)
    return None

#A* search algorithm 
def a_search(start, goal, heuristic):
    start = tuple(tuple(row) for row in start)


    open_set = heapdict()
    closed_set = set()
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    f_score = {}
    nodes_generated = 0
    nodes_expanded = 0

    g_score[start] = 0
    f_score[start] = heuristic(start, goal)
    open_set[start] =  f_score[start]

    while open_set:
        current_node = open_set.popitem()[0]
        goal_tuple = ()

        if isinstance(goal, dict):
            goal_tuple = tuple(tuple(list(goal.keys())[i*3:(i+1)*3]) for i in range(3))

        if current_node == goal or current_node == goal_tuple:
            return reconstruct_path(came_from, current_node, nodes_expanded, nodes_generated)
        
        closed_set.add(current_node)

        nodes_expanded += 1

        for neighbor in get_neighbors(current_node):

            nodes_generated += 1

            if neighbor in closed_set:
                continue

            g = g_score[current_node] + 1

            if g < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = g
                f_score = g + heuristic(neighbor, goal)

                open_set[neighbor] = f_score

    print("No solution found.")       
    return None 

def get_init_state():
    print(f"\nEnter the initial state:")
    print("Enter 9 numbers (0-8) separated by spaces")

    while True:
        try:
            num_input = input("Numbers: ").strip()
            numbers = [int(char) for char in num_input if char.isdigit()]

            if len(numbers) != 9:
                print("Please enter exactly 9 numbers")
                continue

            for n in numbers:
                if not (0 <= n <= 8):
                    print("Number must be 0-8")
                    continue

            if set(numbers) != set(range(9)):
                print("Must use each number 0-8 exactly once")
                continue

            state = []
            for i in range(3):
                row = numbers[i*3:(i+1)*3]
                state.append(row)
            
            return state
        
        except ValueError:
            print("Please enter only integers separated by spaces")

def get_goal_state():
    print(f"\nEnter the goal state:")
    print("Enter 9 numbers (0-8)")

    while True:
        try:
            num_input = input("Numbers: ").strip()
            numbers = [int(char) for char in num_input if char.isdigit()]

            if len(numbers) != 9:
                print("Please enter exactly 9 numbers")
                continue

            for n in numbers:
                if not (0 <= n <= 8):
                    print("Number must be 0-8")
                    continue

            if set(numbers) != set(range(9)):
                print("Must use each number 0-8 exactly once")
                continue

            goal_state = {}
            for i, n in enumerate(numbers):          
                i, j = divmod(i, 3)
                goal_state[n] = (i, j)

            goal_state_tuple=[]

            for i in range(3):
                row = tuple(numbers[i*3:(i+1)*3])
                goal_state_tuple.append(row)
            goal_state_tuple = tuple(goal_state_tuple)


            
            return goal_state, goal_state_tuple
        
        except ValueError:
            print("Please enter only integers separated by spaces")


new_matrix =  get_init_state()

goal_state, goal_state_tuple = get_goal_state()


print("\n\nA* search using misplaced numbers heuristic\n")
a_search(new_matrix, goal_state_tuple, calculate_misplaced_h)
print("\n\n")

print("A* search using manhattan distance heuristic\n")
a_search(new_matrix, goal_state, calculate_manhattan_h)