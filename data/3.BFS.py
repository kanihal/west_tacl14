import networkx as nx
import random

G = nx.read_edgelist('wiki/wiki_trusts.txt', nodetype=int, data=(('weight',float),) ,create_using=nx.DiGraph())
# G = nx.DiGraph(G.edges())
N=len(G.nodes())

def get_bfs_nodes(G,seed):
    # S=dict(nx.bfs_successors(G,seed))
    if seed not in list(G.nodes()):
        return False
    bfs_nodes=[seed]
    hold=[seed]

    while(len(bfs_nodes)< 360 and len(hold)>0 ):
         neigh=list(G.neighbors(seed))
         if(len(neigh)==0):
             return False
         else:
             bfs_nodes.extend(neigh)
             hold.extend(neigh)
             hold.remove(seed)
             # print("###hold-",hold)
             seed = hold[0]
    return list(set(bfs_nodes))

seeds=[]
n=10
while n>0:
    seed = random.randint(1,N)
    if seed not in seeds:
        seeds.append(seed)
        n=n-1
    else:
        continue
    print("\n BFS with seed value - ", seed)
    sub_nodes = get_bfs_nodes(G,seed)
    if(sub_nodes):
        H = G.subgraph(sub_nodes)
        nx.write_edgelist(H,'wiki/wiki_fold.txt.'+str(n),data=['weight'],delimiter='\t')
    else:
        n=n+1







