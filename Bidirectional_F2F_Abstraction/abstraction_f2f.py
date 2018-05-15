from Queue import PriorityQueue
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
        


child = Node(['1','2','3'], 'fw', 1, 0, 'open')
child2 =  Node(['1','2','3'], 'fw', 1, 0, 'open')
q = PriorityQueue()
q.put((child.getvalue(),child))
q.put((child2.getvalue(),child2))
print(q.queue)
for node in q.queue:
    print(node[1])