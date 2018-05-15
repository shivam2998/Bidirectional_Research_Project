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
from enum import unique
import heapq
import copy
from plotly.api.v2.users import current
from cmath import phase

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
    
    for node in nodes:
        if(isexpandable(initial_matrix,node,node.getstate()) == True ):
            expandable_list.append(node)
        
    while(len(expandable_list) != 0):
        node = expandable_list[0]
        if(isexpandable(initial_matrix,node,node.getstate()) == False ):
            expandable_list.remove(node)
        
        elif(flim >= h_abstraction(initial_matrix,node.getmatrix(),node.getdirection()) + node.getvalue()):
            expandable_list.remove(node)
            nodes_at_this_level.append(node)
            node.setstate('closed')
            node.sethvalue(h_abstraction(initial_matrix,node.getmatrix(),node.getdirection()))
            
            for neighbors_n in expand(node.getmatrix()):  
                child = Node(neighbors_n, node.getdirection(), node.getvalue() + 1,0, 'open')
                temp_value, temp_node = checker_neighbor_node(neighbors_n) #checks if it already is inside nodes list
                if(temp_value == True):           
                    if(node.getdirection() == temp_node.getdirection()):
                        
            ########################### This is where I for reopening #############################
            
                        if(child.getvalue() < temp_node.getvalue()):
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
        hdir = h_abstraction(initial_matrix,n.getmatrix(),n.getdirection())
        fdir = n.getvalue() + hdir
        return(n.getvalue() < glim_bw and flim >= fdir and state == 'open')
    elif(n.getdirection() == 'fw'):
        hdir = h_abstraction(initial_matrix,n.getmatrix(),n.getdirection())
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
    
def h_abstraction(initial_matrix, current_matrix,dir):
    global nodes
    unique_list_of_list = []
    unique_list_of_nodes = []
    opp_open_list = []
    sorted_opp_open_list = []
    if(True):
        for node in nodes:
            if node.getdirection() != dir and node.getstate() == 'open':
                node_temp_1 = copy.deepcopy(node)
                opp_open_list.append(node_temp_1)
    
        initial_matrix_temp = initial_matrix[:]
        current_matrix_temp = current_matrix[:]
        goal_matrix = ['1', '1', '1', '1', '5', '6', '7', '8', '0']
        
        #This is where I map my base space nodes to abstract space nodes (Here tiles 1,2,3,4 == 1)
        for n,i in enumerate(initial_matrix_temp):
            if i in ['1','2','3','4']:
                initial_matrix_temp[n]= '1'
        for n,i in enumerate(current_matrix_temp):
            if i in ['1','2','3','4']:
                current_matrix_temp[n]= '1'
        
        for node in opp_open_list:
            for n,i in enumerate(node.getmatrix()):
                if i in ['1','2','3','4']:
                    node.getmatrix()[n]= '1'
      
        sorted_opp_open_list = sorted(opp_open_list, key=lambda x: x.getvalue(), reverse=False)
        
        #This is where I check for duplicates in abstract space, ie nodes from base space mapped to same node in the abstract space
        
        for node in sorted_opp_open_list:
            if node.getmatrix() not in unique_list_of_list:
                unique_list_of_list.append(node.getmatrix())
                unique_list_of_nodes.append(node)
  
        phase_1_return = phase_1_abs(current_matrix_temp,unique_list_of_nodes,dir)
        return phase_1_return  
    else:
        return 0

def abstract_isexpandable(node,dir,high_lim,state):
    return (node.getvalue() < high_lim and state == 'open')

def phase_1_abs(current_matrix,nodes_list, current_dir):
    high_lim = nodes_list[-1].getvalue()
    expandable_list = []
    for node in nodes_list:
        if abstract_isexpandable(node, node.getdirection(),high_lim, node.getstate()):
            heapq.heappush(expandable_list, (node.getvalue(),node))
            
    while(len(expandable_list)!= 0):
        node_temp = heapq.heappop(expandable_list)
        node = node_temp[1]
        n_value = node.getvalue()
        if abstract_isexpandable(node, node.getdirection(), high_lim, node.getstate()): 
            node.setstate('closed')
            
            for neighbors_n in expand(node.getmatrix()):
                bool = False
                child = Node(neighbors_n, node.getdirection(), n_value + 1, 0, 'open')
                if neighbors_n == current_matrix:
                    return child.getvalue()
                
                for node in nodes_list:
                    if(node.getmatrix() == child.getmatrix() and child.getvalue() <= node.getvalue()):
                        bool = True
                        nodes_list.append(child)
                        nodes_list.remove(node)
                        if(abstract_isexpandable(child, dir, high_lim,child.getstate())):
                            heapq.heappush(expandable_list,(child.getvalue(),child))
                            
                    elif(node.getmatrix() == child.getmatrix() and child.getvalue() > node.getvalue()):
                        bool = True
                
                if(bool != True):
                    nodes_list.append(child)
                    if(abstract_isexpandable(child, child.getdirection(), high_lim,child.getstate())):
                        heapq.heappush(expandable_list,(child.getvalue(),child))
    
    return phase_2_abs(current_matrix,nodes_list,high_lim,current_dir)

def phase_2_abs(current_matrix,nodes_list,high_lim,current_dir):
    nodes_list_opp = []
    expandable_list_opp = []
    current_node = Node(current_matrix, current_dir, 0, 0, 'open')
    nodes_list_opp.append(current_node)
    if(abstract_isexpandable(current_node, current_node.getdirection(), high_lim, current_node.getstate())):
        heapq.heappush(expandable_list_opp, (current_node.getvalue(),current_node))
    while(len(expandable_list_opp) != 0):
        node_temp = heapq.heappop(expandable_list_opp)
        node = node_temp[1]
        n_value = node.getvalue()
        if abstract_isexpandable(node, node.getdirection(), high_lim, node.getstate()): 
            node.setstate('closed')
            
            for neighbors_n in expand(node.getmatrix()):
                bool = False
                child = Node(neighbors_n, node.getdirection(), n_value + 1, 0, 'open')
                for node in nodes_list:
                    if(node.getmatrix() == child.getmatrix()):
                        return node.getvalue() + child.getvalue()
                
                for node in nodes_list_opp:
                    if(node.getmatrix() == child.getmatrix() and child.getvalue() <= node.getvalue()):
                        bool = True
                        nodes_list_opp.append(child)
                        nodes_list_opp.remove(node)
        
                        if(abstract_isexpandable(child, child.getdirection(), high_lim,child.getstate())):
                            heapq.heappush(expandable_list_opp,(child.getvalue(),child))
                        
                    elif(node.getmatrix() == child.getmatrix() and child.getvalue() > node.getvalue()):
                        bool = True   
                    
                if(bool != True):
                    nodes_list_opp.append(child)
                    if(abstract_isexpandable(child, dir, high_lim,child.getstate())):
                            heapq.heappush(expandable_list_opp,(child.getvalue(),child))
                     
    switcher = 0
    high_lim_front = high_lim
    high_lim_back = high_lim
    while(True):
        if switcher == 0:
            switcher = 1
            temp = phase_3_abs(nodes_list,nodes_list_opp,high_lim_back)
            high_lim_back += 1
            if(temp == True):
                return high_lim_back + high_lim_front
            
        elif switcher == 1:
            switcher = 0
            temp_1 = phase_3_abs(nodes_list_opp,nodes_list,high_lim_front)
            high_lim_front += 1
            if(temp_1 == True):
                return high_lim_back + high_lim_front
            
def phase_3_abs(nodes_list,nodes_list_opp, high_lim):
    expandable_list = []
    for node in nodes_list:
        if node.getvalue() == high_lim:
            expandable_list.append(node)
            
    while(len(expandable_list) != 0):
        node = expandable_list[0]
        expandable_list.remove(node)
        node.setstate('closed')
        n_value = node.getvalue()
        for neighbors_n in expand(node.getmatrix()):
            bool = False
            child = Node(neighbors_n, node.getdirection(), n_value + 1,0,'open')
            for node in nodes_list_opp:
                if(node.getmatrix() == child.getmatrix()):
                    return True
            for node in nodes_list:
                if(node.getmatrix() == child.getmatrix() and child.getvalue() <= node.getvalue()):
                    bool = True
                    nodes_list.append(child)
                    nodes_list.remove(node)
                    
                elif(node.getmatrix() == child.getmatrix() and child.getvalue() > node.getvalue()):
                    bool = True
                    
            if(bool != True):
                nodes_list.append(child)

            
def csv_format(initial_matrix):
    global nodes
    global temp_nodes
    new_list = []
    zero_list = []
    dir_values = ['fw','bw']
    g_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    f_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
   
    for node in temp_nodes:  
        if(node.getstate() == 'closed'):
            hdir = node.gethvalue()
            fdir = node.getvalue() + hdir
            new_list.append((node.getdirection(), node.getvalue(), fdir ))
    
    prod_list = list(itertools.product(dir_values,g_values,f_values))
    for i in prod_list:
        if i not in new_list:
            zero_list.append(i)

    return new_list,zero_list

        