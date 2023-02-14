import numpy as np
import random

ROWS = 10
COLS = 10
p = 0.3
tie_break = 'b'

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
    
    def swap(self,i):
        self.heap[i], self.heap[1] = self.heap[1], self.heap[i]

    def contains(self,cell):
        for i in range(1,self.size+1):
            if self.heap[i] == cell:
                return i
        return -1
    
    def getsize(self):
        return self.size

    def print_heap(self):
        for i in range(1, (self.size//2)):
            print(" PARENT : "+ str(self.heap[i].getf())+" LEFT CHILD : "+ str(self.heap[2 * i].getf())+" RIGHT CHILD : "+ str(self.heap[2 * i + 1].getf()))


class graph:
    def __init__(self,id,blocked,neighbors,visited,display):
        self.id = id
        self.blocked = blocked
        self.neighbors = neighbors
        self.visited = visited
        self.display = display
        self.g = None
        self.h = None
        self.f = None
        self.search = 0
        self.tree = self
        self.cost = 1
    
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
    def getsearch(self):
        return self.search
    def gettree(self):
        return self.tree
    def getcost(self):
        return self.cost
    
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
    def setsearch(self,search):
        self.search = search
    def settree(self,tree_ptr):
        self.tree = tree_ptr
    def setcost(self,cost):
        self.cost = cost
    


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

def set_h_values(cell_graph,T):
    for cell in cell_graph:
        cell_coords = cell.getid()
        h = abs(cell_coords[0] - T.getid()[0]) + abs(cell_coords[1] - T.getid()[1])
        cell.seth(h)

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
    
    set_h_values(cell_graph,T)

    return T,A


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
"""
def test_heap(cell_graph,minheap):
    for cell in cell_graph:
        minheap.insert(cell)
    for i,cell in enumerate(cell_graph):
        print("The minimum element is: " + str(minheap.delete().getf()))
"""
def test_heap_2(minheap):
    print("range: " + str(minheap.size))
    for i in range(1,minheap.size):
        print("element: " + str(minheap.heap[i].getid()))


def findMin(minheap):
    # test_heap_2(minheap)
    top = minheap.heap[1]
    top_f = top.getf()
    top_g = top.getg()
    trueindex = 1
    g_arr = [top_g]
    g_index = [1]
    if minheap.getsize() > 0:
        for i in range(2,minheap.size+1):
            if (minheap.heap[i].getf() == top_f):
                g_arr.append(minheap.heap[i].getg())
                g_index.append(i)
            else: break
    
    if tie_break == 'b':
        indices = [index for index, item in enumerate(g_arr) if item == max(g_arr)]
        random.shuffle(indices)
        main_index = indices[0]
        return g_index[main_index]
    if tie_break == 'l':
        indices = [index for index, item in enumerate(g_arr) if item == min(g_arr)]
        random.shuffle(indices)
        main_index = indices[0]
        return g_index[main_index]
    
    # print("FINDMIN DONE")

    return trueindex
            

def compute_path(OPEN_list,target_cell,counter):
    while (not (OPEN_list.getsize() == 0)) and (target_cell.getg() > findMin(OPEN_list)):
        # test_heap_2(OPEN_list)
        # print("Min: " + str(findMin(OPEN_list)))
        OPEN_list.swap(findMin(OPEN_list))
        s = OPEN_list.delete()
        if s.getid() == target_cell.getid():
            return
        # print("SELECTED: " + str(s.getid()))
        for cell in s.getneighbors():
            if cell.getsearch() < counter:
                cell.setg(np.inf)
                cell.setsearch(counter)
            if cell.getg() > (s.getg() + cell.getcost()):
                cell.setg(s.getg() + cell.getcost())
                cell.settree(s)
                # print("set tree of " + str(cell.getid()) + " to " + str(s.getid()))
                if not OPEN_list.contains(cell) == -1:
                    OPEN_list.swap(OPEN_list.contains(cell))
                    OPEN_list.delete()
                cell.setf(cell.getg() + cell.geth())
                OPEN_list.insert(cell)
            # print("cell id: " + str(cell.getid()))
    
    # print("COMPUTE PATH DONE")
    # print(OPEN_list.getsize())


def follow_tree(target_cell,start_cell):
    path = [target_cell]
    ptr = target_cell
    while not ptr.gettree() == start_cell:
        path.append(ptr.gettree())
        ptr = ptr.gettree()
    path.append(start_cell)
    path.reverse()
    
    initialize_costs(path[0])
    for i in range(len(path)):
        initialize_costs(path[i])
        if path[i] == target_cell:
            path[i].setdisplay("A")
            return path[i]
        if not path[i+1].getcost() == np.inf:
            path[i].setdisplay(".")
            path[i+1].setdisplay("A")
        else:
            return path[i]
    return path[len(path)-1]

def follow_tree_backward(target_cell,start_cell):
    path = [target_cell]
    ptr = target_cell
    while not ptr.gettree() == start_cell:
        path.append(ptr.gettree())
        ptr = ptr.gettree()
    path.append(start_cell)
    
    # path.reverse()
    
    initialize_costs(path[0])
    for i in range(len(path)):
        initialize_costs(path[i])
        if path[i] == start_cell:
            path[i].setdisplay("A")
            return path[i]
        if not path[i+1].getcost() == np.inf:
            path[i].setdisplay(".")
            path[i+1].setdisplay("A")
        else:
            return path[i]
    return path[len(path)-1]
    

def repeated_forward_a(cell_graph,target_cell,start_cell):
    counter = 0
    for cell in cell_graph:
        cell.setsearch(0)
    
    ptr_cell = start_cell
    while not ptr_cell.getid() == target_cell.getid():
        counter += 1
        initialize_costs(ptr_cell)
        ptr_cell.setg(0)
        ptr_cell.setsearch(counter)
        target_cell.setg(np.inf)
        target_cell.setsearch(counter)
        OPEN_list = MinHeap()
        ptr_cell.setf(ptr_cell.getg() + ptr_cell.geth())
        OPEN_list.insert(ptr_cell)
        # test_heap(cell_graph,OPEN_list)
        print_array(cell_graph)
        ptr_cell.setf(ptr_cell.getg() + ptr_cell.geth())
        compute_path(OPEN_list,target_cell,counter)
        # test_heap_2(OPEN_list)
        if OPEN_list.getsize() == 0:
            print('I cannot reach the target.')
            return
        ptr_cell = follow_tree(target_cell,ptr_cell)
        print_array(cell_graph)
        # print("ITERATION DONE")
    print("I reached the path")
    return

def repeated_backward_a(cell_graph,target_cell,start_cell):
    counter = 0
    for cell in cell_graph:
        cell.setsearch(0)
    
    ptr_cell = target_cell
    while not ptr_cell.getid() == start_cell.getid():
        counter += 1
        initialize_costs(ptr_cell)
        ptr_cell.setg(0)
        ptr_cell.setsearch(counter)
        start_cell.setg(np.inf)
        start_cell.setsearch(counter)
        OPEN_list = MinHeap()
        ptr_cell.setf(ptr_cell.getg() + ptr_cell.geth())
        OPEN_list.insert(ptr_cell)
        # test_heap(cell_graph,OPEN_list)
        print_array(cell_graph)
        ptr_cell.setf(ptr_cell.getg() + ptr_cell.geth())
        compute_path(OPEN_list,start_cell,counter)
        # test_heap_2(OPEN_list)
        if OPEN_list.getsize() == 0:
            print('I cannot reach the start.')
            return
        start_cell = follow_tree_backward(start_cell,ptr_cell)
        print_array(cell_graph)
        # print("ITERATION DONE")
    print("I reached the path backwards")
    return

        
def initialize_costs(start_cell):
    for cell in start_cell.getneighbors():
        if cell.getdisplay() == "X":
            cell.setcost(np.inf)



def main():
    # cell_graph = generate_graph()
    
    environments = []
    for _ in range(1):
        new_graph = generate_graph()
        unblocked_array = generate_blockages(new_graph.copy())
        target_cell,start_cell = generate_target(new_graph.copy(),unblocked_array)
        environments.append(new_graph)
        print(target_cell.getid())
        print(start_cell.getid())
        # repeated_forward_a(new_graph,target_cell,start_cell)
        set_h_values(new_graph,start_cell)
        repeated_backward_a(new_graph,target_cell,start_cell)

    # for environment in environments:
        # print_array(environment)

if __name__ == '__main__':
    main()
