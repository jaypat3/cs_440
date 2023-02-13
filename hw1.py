import numpy as np
import random

ROWS = 5
COLS = 5
p = 0.3

class MinHeap:

    def __init__(self):
        self.heap = [0]
        self.size = 0

    def swim(self,i):
        stop = False
        while(i//2 > 0) and stop == False:
            if self.heap[i].getf() < self.heap[i//2].getf():
                self.heap[i], self.heap[i//2] = self.heap[i//2], self.heap[i]
            else:
                stop = True
            i = i//2
    
    def insert(self,i):
        self.heap.append(i)
        self.size += 1
        self.swim(self.size)

    def sink(self,i):
        while(i*2) <= self.size:
            min_child_index = self.min_child(i)
            if self.heap[i].getf() > self.heap[min_child_index].getf():
                self.heap[i], self.heap[min_child_index] = self.heap[min_child_index], self.heap[i]
            i = min_child_index
    
    def min_child(self,i):
        if(i*2)+1 > self.size:
            return i*2
        else:
            if self.heap[i*2].getf() < self.heap[(i*2)+1].getf():
                return i*2
            else: return i*2 + 1
    
    def delete(self):
        if len(self.heap) == 1:
            return 'empty'
        
        min_element = self.heap[1]
        self.heap[1] = self.heap[self.size]
        *self.heap, _ = self.heap
        self.size -= 1
        self.sink(1)
        return min_element
    
    def peek(self):
        return self.heap[1]


class graph:
    def __init__(self,id,blocked,neighbors,visited,display):
        self.id = id
        self.blocked = blocked
        self.neighbors = neighbors
        self.visited = visited
        self.display = display
        self.g = -1
        self.h = -1
        self.f = -1
    
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
    def getg(self):
        return self.g
    def geth(self):
        return self.h
    def getf(self):
        return self.f
    
    def setvisited(self,newvisited):
        self.visited = newvisited
    def setblocked(self,newblocked):
        self.blocked = newblocked
    def setdisplay(self,newdisplay):
        self.display = newdisplay
    def addneighbors(self,neighbors):
        self.neighbors = neighbors
    def setg(self,g):
        self.g = g
    def seth(self,h):
        self.h = h
    def setf(self,f):
        self.f = f
    


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

def DFS(cell,unblocked_array):
    cell.setvisited(True)
    cell.setblocked(perform_bernoulli_trial())
    if cell.getblocked() == True:
        cell.setdisplay("X")
    else: unblocked_array.append(cell)
    neighbors = cell.getneighbors().copy()
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor.getvisited == False:
            unblocked_array = DFS(cell,unblocked_array)
    return unblocked_array

def generate_blockages(cell_graph):
    main_graph = cell_graph.copy()
    random.shuffle(main_graph)
    unblocked_array = []
    for cell in main_graph:
        unblocked_array = DFS(cell,unblocked_array)
    return unblocked_array

def generate_target(cell_graph,unblocked_array):
    random.shuffle(unblocked_array)
    A = unblocked_array[0]
    T = unblocked_array[1]
    T_coords = T.getid()
    for cell in cell_graph:
        if cell == A:
            cell.setdisplay("A")
        if cell == T:
            cell.setdisplay("T")
    
    for cell in cell_graph:
        cell_coords = cell.getid()
        h = abs(cell_coords[0] - T_coords[0]) + abs(cell_coords[1] - T_coords[1])
        cell.seth(h)

        cell.setf(cell.getg()+cell.geth()) #COMMENT OUT SOON!

    return T_coords


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
        print(cell.getid(),cell.getblocked(),cell.getvisited(),cell.getdisplay(),cell.getg(),cell.geth(),cell.getf())
        for neighbor in cell.getneighbors():
            print(neighbor.getid())


#TESTING METHOD FOR HEAP
def test_heap(cell_graph,minheap):
    for cell in cell_graph:
        minheap.insert(cell)
    for i,cell in enumerate(cell_graph):
        print("The minimum element is: " + str(minheap.delete().getf()))


def main():
    arr = create_array()
    init_print_array(arr)
    # cell_graph = generate_graph()
    
    environments = []
    for _ in range(1):
        new_graph = generate_graph()
        unblocked_array = generate_blockages(new_graph.copy())
        target_coordinate = generate_target(new_graph.copy(),unblocked_array)
        environments.append(new_graph)
        print(target_coordinate)
        # print_contents(new_graph)
        # print_array(new_graph)
        minheap = MinHeap()
        # test_heap(new_graph,minheap)

    for environment in environments:
        print_array(environment)

if __name__ == '__main__':
    main()
