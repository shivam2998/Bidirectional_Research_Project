'''
Name: Shivam Shah
UPI: ssha981
StudentID: 516637469
Research Project: Effective front-front Heuristic Bidirectional Search
Code_Name: B# Implementation with Manhattan distance and statistics
'''
#from networkx.classes.function import neighbors
from timeit import itertools
import itertools

# NODE CLASS 
glim_bw = 0
glim_fw = 0
flim = 1
nodes_ab = []

class Node: 
    def __init__(self, matrix, direction, gvalue, state):
        self.matrix = matrix
        self.direction = direction
        self.gvalue = gvalue
        self.state = state
        self.next = None
    
    def getmatrix(self):
        return self.matrix
    
    def setmatrix(self,new_matrix):
        self.matrix = new_matrix
        
    def getdirection(self):
        return self.direction
    
    def setdirection(self,new_direction):
        self.direction = new_direction
    
    def getvalue(self):
        return self.gvalue
    
    def setvalue(self,new_gvalue):
        self.gvalue = new_gvalue
        
    def getstate(self):
        return self.state
    
    def setstate(self,new_state):
        self.state = new_state
        
    def getnext(self):
        return self.next
    
    def setnext(self,new_next):
        self.next = new_next
        
'''
 
b_hash returns optimal path solution
@param: array $nodes_ab, array $initial_matrix, array $goal_matrix
@return: flim if puzzle is solvable else returns -1

'''      

def b_hash_abs(initial_matrix, goal_matrix):
    global glim_bw
    global glim_fw
    global flim
    global nodes_ab
    #print("HIIIIIIIIi")
    fw = 'fw' #forward direction
    bw = 'bw' #backward direction

    
    if(initial_matrix == goal_matrix): #trivial case that returns 0 if the input is solved
        return 0
    
    #adding initial nodes_ab to nodes_ab list
    nodes_ab.append(Node(initial_matrix, fw, 0 , 'open'))
    nodes_ab.append(Node(goal_matrix, bw, 0 , 'open')) 
    
    incremented_dir = bw #initially setting the direction to be incremented to backwards

    while(True):    
        
        #switching directions and incrementing flim and glim for that direction
        if(incremented_dir == bw):
            incremented_dir = fw
            glim_fw += 1
            if(expandlevel(initial_matrix,incremented_dir) == True):
                #resetting glims for another test case
                glim_bw = 0 
                glim_fw = 0
                nodes_ab[:] = []
                #print(flim)
                return flim
            
        elif(incremented_dir == fw):
            incremented_dir = bw  
            glim_bw += 1
            if(expandlevel(initial_matrix,incremented_dir) == True):
                #resetting glims for another test case
                glim_bw = 0 
                glim_fw = 0
                nodes_ab[:] = []
                #print(flim)
                return flim
            
        flim += 1
    return 0

'''
expandlevel returns true if we find optimal path at that level
@param array nodes_ab, string incremented_dir, int glim, int flim:
@return: true if solution is found 
'''   
 
def expandlevel(initial_matrix,incremented_dir):
    global glim_bw
    global glim_fw
    global flim
    global nodes_ab

    count = 0
    expandable_list = []
    #print("BROOOo")
    for node in nodes_ab:
        #print("ZZZZZZZZ")
        #print(node.getmatrix(),node.getstate(),node.getdirection())
        state = node.getstate()
        if(isexpandable(initial_matrix,node,state) == True ):
            expandable_list.append(node)
    
    while(len(expandable_list) != 0):
        #print("Hi")
        node = expandable_list[0]
        if(flim >= node.getvalue()):
            expandable_list.remove(node)
            node.setstate('closed')
            
            for neighbors_n in expand(node.getmatrix()): 
                #print("....................") 
                child = Node(neighbors_n, node.getdirection(), node.getvalue() + 1, 'open')
                temp_value, temp_node = checker_neighbor_node(neighbors_n) #checks if it already is inside nodes_ab list
                if(temp_value == True):           
                    if(node.getdirection() == temp_node.getdirection()):
                        
            ########################### This is where I for reopening #############################
            
                        if(child.getvalue() < temp_node.getvalue()):
                            nodes_ab.append(child)
                            nodes_ab.remove(temp_node) #removing node with higher gvalue that was expanded before
                            if(isexpandable(initial_matrix,child, child.getstate())):
                                expandable_list.append(child) 
                        #print("yes")   
                        continue
                    else:
                        #print("hee")
                        return True
                    
                nodes_ab.append(child)
                if(isexpandable(initial_matrix,child, child.getstate())):
                    expandable_list.append(child)       

    return False 


'''
checker_neighbor_node checks if the neighbor we expanded already exist in nodes_ab list
@param array nodes_ab, array neighbor:
@return: True and direction of node if found 
'''

        
def checker_neighbor_node(neighbors_n):
    global nodes_ab
    #print("HIiiiiiiiiiiiiiii")
    for node in nodes_ab:
        if(node.getmatrix() == neighbors_n):
            return True,node
    return False, -1

'''
isexpandable checks if can expand the node and put it into our expandable_list
@param Node n, int glim, int flim, string incremented_dir:
@return: True if its expandable 
'''

def isexpandable(initial_matrix,n,state):
    global glim_bw
    global glim_fw
    global flim
   
    if(n.getdirection() == 'bw'):
        hdir = 0
        fdir = n.getvalue() + hdir
        return(n.getvalue() < glim_bw and flim >= fdir and state == 'open')
    elif(n.getdirection() == 'fw'):
        hdir = 0
        fdir = n.getvalue() + hdir
        return(n.getvalue() < glim_fw and flim >= fdir and state == 'open')
        
'''
expand finds all possible neighbors of that node
@param array init_s
@return: array new_list(this contains all neighbors) 
'''
    
def expand(init_s):
    #print("HIII")
    flat_list = init_s
    i = init_s.index('0')
    new_board = []
    n_list = [] 
    if i in [3, 4, 5, 6, 7, 8]:
        new_board = init_s[:]
        new_board[i], new_board[i - 3] = new_board[i - 3], new_board[i]
        n_list.append(new_board)
     
    if i in [1, 2, 4, 5, 7, 8]:
        new_board = init_s[:]
        new_board[i], new_board[i - 1] = new_board[i - 1], new_board[i]
        n_list.append(new_board)
      
    if i in [0, 1, 3, 4, 6, 7]:
        new_board = init_s[:]
        new_board[i], new_board[i + 1] = new_board[i + 1], new_board[i]
        n_list.append(new_board)
      
    if i in [0, 1, 2, 3, 4, 5]:
        new_board = init_s[:]
        new_board[i], new_board[i + 3] = new_board[i + 3], new_board[i]
        n_list.append(new_board)
      
    return n_list
        