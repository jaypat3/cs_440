import numpy as np
import random

ROWS = 5
COLS = 5
p = 0.3

class graph:
    def __init__(self,id,blocked,neighbors,visited,display):
        self.id = id
        self.blocked = blocked
        self.neighbors = neighbors
        self.visited = visited
        self.display = display
    
    def getid(self):
        return self.id
    def getblocked(self):
        return self.blocked
    def getneighbors(self):
        return self.neighbors
    def getvisited(self):
        return self.visited
    def getdisplay(self):
        return self.display
    
    def setvisited(self,newvisited):
        self.visited = newvisited
    def setblocked(self,newblocked):
        self.blocked = newblocked
    def setdisplay(self,newdisplay):
        self.display = newdisplay
    def addneighbors(self,neighbors):
        self.neighbors = neighbors
    


def create_array():
    arr = [[" " for i in range(COLS)] for j in range(ROWS)]
    return arr

def init_print_array(arr):
    arr[0][1] = "."
    header = ["-" for i in range(COLS+1)]
    footer = ["-" for i in range(COLS+1)]
    print(' '.join(header))
    for row in arr:
        print('|', end = "")
        print(' '.join(row), end = "")
        print('|')
    print(' '.join(footer))


def generate_neighbors(cell_graph,coordinate):
    neighbors = []
    x = coordinate[0]
    y = coordinate[1]
    if y+1 < COLS: 
        neighbors.append(cell_graph[x*ROWS + y+1])
    if y-1 >= 0: 
        neighbors.append(cell_graph[x*ROWS + y-1])
    if x+1 < ROWS: 
        neighbors.append(cell_graph[(x+1)*ROWS + y])
    if x-1 >= 0: 
        neighbors.append(cell_graph[(x-1)*ROWS + y])
    
    return neighbors

def convert(list):
    return tuple(list)

def generate_graph():
    a = np.arange(0,ROWS,dtype = int)
    b = np.arange(0,ROWS,dtype=int)

    coordinates = [(a0, b0) for a0 in a for b0 in b]
    # print(coordinates)

    cell_graph = []
    for coordinate in coordinates:
        new_cell = graph(coordinate,False,[],False," ")
        cell_graph.append(new_cell)
    
    for cell in cell_graph:
        neighbors = generate_neighbors(cell_graph,cell.getid())
        cell.addneighbors(neighbors)
    
    # for item in [0,4,20,24]:
        # testcell = cell_graph[item]
        # for neighbor in testcell.getneighbors():
            # print(neighbor.getid())
    
    return cell_graph


def perform_bernoulli_trial():
    random_number = np.random.random()
    if(random_number < p):
        return True
    else: return False

def DFS(cell):
    cell.setvisited(True)
    cell.setblocked(perform_bernoulli_trial())
    if cell.getblocked() == True:
        cell.setdisplay("X")
    neighbors = cell.getneighbors().copy()
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor.getvisited == False:
            DFS(cell)

def generate_blockages(cell_graph):
    main_graph = cell_graph.copy()
    for cell in main_graph:
        DFS(cell)

def print_array(cell_graph):
    header = ["-" for i in range(COLS+1)]
    footer = ["-" for i in range(COLS+1)]
    print(' '.join(header))
    for i in range(ROWS):
        print('|', end = "")
        for j in range(COLS):
            end_string = " "
            if(j+1 == COLS):
                end_string = ""
            print(cell_graph[i*ROWS+j].getdisplay(),end = end_string)
        print('|')
    print(' '.join(footer))

def print_contents(cell_graph):
    for cell in cell_graph:
        print(cell.getid(),cell.getblocked(),cell.getvisited(),cell.getdisplay())
        for neighbor in cell.getneighbors():
            print(neighbor.getid())

def main():
    arr = create_array()
    init_print_array(arr)
    cell_graph = generate_graph()

    environments = []
    for _ in range(50):
        new_graph = generate_graph()
        generate_blockages(new_graph.copy())
        environments.append(new_graph)
        # print_contents(new_graph)
        # print_array(new_graph)

    for environment in environments:
        print_array(environment)

if __name__ == '__main__':
    main()