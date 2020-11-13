def __init__(self):
    self.l = 1
    self.m = 2
    
def add_more_attributes(self):
    self.n = 3  
     
def bad_add_more_attributes(self):
    self.private_o = 4 # should raise exception
     
def bump(self):
    self.l += 1
    self.m += 1
    self.n += 1
    
def __str__(self):
    return 'l='+str(self.l)+',m='+str(self.m)+',n='+str(self.n)+',o='+str(self.o)

def extra_bump(self):
    self.a += 1     
