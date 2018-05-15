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
nodes = []
temp_nodes = [] #Just to get count of nodes for csv file
f_level_nodes = {}

class Node: 
    def __init__(self, matrix, direction, gvalue,hvalue, state):
        self.matrix = matrix
        self.direction = direction
        self.gvalue = gvalue
        self.state = state
        self.next = None
        self.hvalue = hvalue
    
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
    
    def sethvalue(self,new_hvalue):
        self.hvalue = new_hvalue
    
    def gethvalue(self):
        return self.hvalue
    
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
@param: array $nodes, array $initial_matrix, array $goal_matrix
@return: flim if puzzle is solvable else returns -1

'''      

def b_hash(initial_matrix, goal_matrix):
    global glim_bw
    global glim_fw
    global flim
    global nodes
    global temp_nodes
    fw = 'fw' #forward direction
    bw = 'bw' #backward direction

    
    if(initial_matrix == goal_matrix): #trivial case that returns 0 if the input is solved
        return 0
    
    #adding initial nodes to Nodes list
    nodes.append(Node(initial_matrix, fw, 0 , 0, 'open'))
    nodes.append(Node(goal_matrix, bw, 0 ,0, 'open')) 
    
    incremented_dir = bw #initially setting the direction to be incremented to backwards

    while(solvable(initial_matrix)):    
        #switching directions and incrementing flim and glim for that direction
        if(incremented_dir == bw):
            incremented_dir = fw
            glim_fw += 1
            if(expandlevel(initial_matrix,incremented_dir) == True):
                #resetting glims for another test case
                glim_bw = 0 
                glim_fw = 0
                for node in nodes:
                    if node.getstate() == 'closed':
                        temp_nodes.append(node)
                nodes[:] = []
                return flim,temp_nodes
            
        elif(incremented_dir == fw):
            incremented_dir = bw  
            glim_bw += 1
            if(expandlevel(initial_matrix,incremented_dir) == True):
                #resetting glims for another test case
                glim_bw = 0
                glim_fw = 0
                for node in nodes:
                    if node.getstate() == 'closed':
                        temp_nodes.append(node)
                nodes[:] = []
                return flim,temp_nodes
        
        flim += 1
    return -1 

'''
expandlevel returns true if we find optimal path at that level
@param array nodes, string incremented_dir, int glim, int flim:
@return: true if solution is found 
'''   
 
def expandlevel(initial_matrix,incremented_dir):
    global glim_bw
    global glim_fw
    global flim
    global nodes
    global f_level_nodes
    nodes_at_this_level = []
    count = 0
    expandable_list = []
    #open_list = []
    
    for node in nodes:
        #print(node.getmatrix(),node.getstate(),node.getdirection())
        if(isexpandable(initial_matrix,node,node.getstate()) == True ):
            expandable_list.append(node)
            
            #print("hi")
    #print(flim)
    while(len(expandable_list) != 0):
        #print("JO")
        node = expandable_list[0]
        #print(node.getmatrix(),node.getdirection(),node.getvalue(), h(initial_matrix,node.getmatrix(),node.getdirection()))
        if(isexpandable(initial_matrix,node,node.getstate()) == False ):
            expandable_list.remove(node)
        if(flim >= h(initial_matrix,node.getmatrix(),node.getdirection()) + node.getvalue()):
            expandable_list.remove(node)
            nodes_at_this_level.append(node)
            node.setstate('closed')
            node.sethvalue(h(initial_matrix,node.getmatrix(),node.getdirection()))
            #print(node.gethvalue())
            
            for neighbors_n in expand(node.getmatrix()):  
                #print("hi")
                child = Node(neighbors_n, node.getdirection(), node.getvalue() + 1,0, 'open')
                temp_value, temp_node = checker_neighbor_node(neighbors_n) #checks if it already is inside nodes list
                if(temp_value == True):           
                    if(node.getdirection() == temp_node.getdirection()):
                        
            ########################### This is where I for reopening #############################
            
                        if(child.getvalue() < temp_node.getvalue()):
                            #print("Hii")
                            nodes.append(child)
                            nodes.remove(temp_node) #removing node with higher gvalue that was expanded before
                            if(isexpandable(initial_matrix,child, child.getstate())):
                                expandable_list.insert(0, child)    
                        continue
                    else:
                        f_level_nodes[str(flim)] = len(nodes_at_this_level)
                        return True
                
                nodes.append(child)
                if(isexpandable(initial_matrix,child, child.getstate())):
                    #print("hi")
                    expandable_list.insert(0, child)
        
    f_level_nodes[str(flim)] = len(nodes_at_this_level)
             
        #print("jo")    
    return False 


'''
checker_neighbor_node checks if the neighbor we expanded already exist in Nodes list
@param array nodes, array neighbor:
@return: True and direction of node if found 
'''

        
def checker_neighbor_node(neighbors_n):
    global nodes
    for node in nodes:
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
    global nodes
   
    if(n.getdirection() == 'bw'):
        #print(n.getstate())
    
        hdir = h(initial_matrix,n.getmatrix(),n.getdirection())
        fdir = n.getvalue() + hdir
        return(n.getvalue() < glim_bw and flim >= fdir and state == 'open')
    elif(n.getdirection() == 'fw'):
        #print(n.getstate())
        hdir = h(initial_matrix,n.getmatrix(),n.getdirection())
        fdir = n.getvalue() + hdir
        return(n.getvalue() < glim_fw and flim >= fdir and state == 'open')
        
'''
expand finds all possible neighbors of that node
@param array init_s
@return: array new_list(this contains all neighbors) 
'''
    
def expand(init_s):
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

'''
Initially checks if the input is solvable or not
@param array s2:
@return: True if s2 is solvable
'''
    
def solvable(s2):
    s1 = s2[:]
    s1.remove('0')
    s = ''.join(str(r) for v in s1 for r in v)
    count = 0
    for i in range(len(s)-1):
        for j in range(i+1,len(s)):
            if s[i] > s[j]:
                count +=  1
                        
    if count % 2 == 0:
        return True
    else:
        return False
        
def h(initial_matrix,current_matrix,dir):
    global nodes
    opp_open_list = []
    hmin_list = []
    for node in nodes:
        if node.getdirection() != dir and node.getstate() == 'open':
            opp_open_list.append(node)
            #print(node.getmatrix(),node.getstate(),node.getdirection())
    current_state = [current_matrix[i:i+3] for i in range(0, len(current_matrix), 3)] #Converting 1d to 2d array/list
    for node in opp_open_list:
        goal_state = [node.getmatrix()[i:i+3] for i in range(0, len(current_matrix), 3)]
        hmin = h_cal(current_state, goal_state) + node.getvalue()
        #print(current_matrix,node.getmatrix(),hmin)
        hmin_list.append(hmin)
    #print("HMIN:",min(hmin_list),current_matrix)
    return min(hmin_list)



def h_cal(initial_state,goal_state):
    if(True):
        mandist = 0
        for c in '12345678':
            x1,y1 = getting_index(initial_state, c)
            x2,y2 = getting_index(goal_state, c)
            mandist += abs(x1-x2) + abs(y1-y2)
        return mandist
    return 0

def getting_index(state,c):
    for i,i_list in enumerate(state):
        for j,j_list in enumerate(i_list):
            if j_list == c:
                return i, j
            
            
def csv_format(initial_matrix):
    global nodes
    global temp_nodes
    new_list = []
    zero_list = []
    dir_values = ['fw','bw']
    g_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    f_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    #print("h")
    for node in temp_nodes:
        #print("hi")
        if(node.getstate() == 'closed'):
            hdir = node.gethvalue()
            #print(hdir)
            fdir = node.getvalue() + hdir
            new_list.append((node.getdirection(), node.getvalue(), fdir ))
    
    prod_list = list(itertools.product(dir_values,g_values,f_values))
    #zero_list = set(new_list).intersection(set(prod_list))
    for i in prod_list:
        if i not in new_list:
            zero_list.append(i)
    #print(zero_list)

    return new_list,zero_list
            
    #print(f_values)
        