"""
This is a test implementation of the Frenemy model. Implements 2 rules:

Friend of a friend is my friend
Enemy of my friend is my enemy

"""

from multimode import MultimodeGraph
from random import randint

mm=MultimodeGraph()
numagents=20

def init():
    """
    Create an empty graph with /numagents/ nodes and no edges
    """
    for i in range(numagent):
        mm.add_node(i,type="person")
        
def random_edge():
    mm.add_edge(randint(0,numagents),randint(0,numagents),weight=1,utype="person",vtype="person",key="friend")
    
    
def friend_of_a_friend():
    mm.add_subgraph(mm.infer(mm,mm,key="friend"))
    

def flip_edge(u,v):
    if mm.has_edge(u,v,key="friend"):
        mm.remove_edge(u,v,key='friend')
        mm.add_edge(u,v,weight=1,utype="person",vtype="person",key="enemy")    

def random_enemy():
    u=randint(0,numagents)
    v=randint(0,numagents)
    flip_edge(u,v)

def enemy_of_a_friend(): 
    friends=mm.subgraph("person","person",key="friend")
    enemies=mm.subgraph("person","person",key="enemy")
    
    if len(enemies) == 0 or len(friends) == 0: return len(friends),len(enemies)
    
    for f,t in mm.infer(friends,enemies,key="enemy").edges():
        flip_edge(f,t)

    return len(friends.edges()),len(enemies.edges())

def step():
    mm.discount_edges()
    random_edge()
    friend_of_a_friend()
    random_enemy()
    return enemy_of_a_friend()
    

import numpy
ne=[]
for x in range(100):
    f,e = step()
    ne.append((f,e))
    
