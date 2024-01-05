# ILP CMCP (artículo "greedy heuristics")
import networkx as nx
import math
from gurobipy import *
import numpy as np
import time

# Cargar grafo
def loadGraph(input_file):
    global d
    G = nx.Graph()
    for j in range(0,n):
        G.add_node(j)

    f = open(input_file, "r")
    string = f.readline()
    string = f.readline()
    for i in range(0, m):
        string = f.readline()
        string = string.split()
        j = int(string[0])-1
        k = int(string[1])-1
        G.add_edge(j, k)
    f.close()
    # All-pairs' shortest path
    #d = dict(nx.all_pairs_shortest_path_length(G))
    #d = [[float("inf")]*n for i in range(n)]
    d = []
    j = 1
    for i in range(n):
        d.append([float("inf")]*(j))
        j+=1
    for i in range(G.number_of_nodes()):
        ds = nx.single_source_shortest_path_length(G, i)
        for key in ds:
            if i >= key:
                d[i][key] = ds[key]
            else:
                d[key][i] = ds[key]
    print("n: " + str(G.number_of_nodes()))
    print("m: " + str(G.number_of_edges()))
    print("ncc: " + str(nx.number_connected_components(G)))

       
def coversAllVertices(s,k,n):
    vertices = []
    for i in range(n):
        covered = False
        for j in range(len(s)):
            try:
                try:
                    if i >= s[j]:
                        if d[i][s[j]] <= k - (s.index(s[j]) + 1):
                            covered = True
                    else:
                        if d[s[j]][i] <= k - (s.index(s[j]) + 1):
                            covered = True
                except:
                    covered = False
            except:
                pass
        if covered:
            vertices.append(i)
    #print(len(vertices))
    #print(s)
    if len(vertices) == n:
        return True
    else:
        return False
    
def ILP(k):
    global d
    m = Model("mip1")
    m.Params.outputFlag = 0  # 0 - Off  //  1 - On
    m.setParam("MIPGap", 0.0);
    m.setParam("Presolve", 2); # -1 - Automatic // 0 - Off // 1 - Conservative // 2 - Aggresive 
    m.setParam("TimeLimit", 2*3600000)

    # Definir variables
    b  = [0] * n # b_{j}
    x  = [ [0] * n for i in range(k)] # x_{r,j}

    for j in range(n):
        b[j] = m.addVar(vtype=GRB.BINARY, name="b,%s" % str(j+1))

    for r in range(k):
        for i in range(n):
            x[r][i] = m.addVar(vtype=GRB.BINARY, name="x,%s" % str(r+1) + "," + str(i+1))

    # Función objetivo
    # (1)
    m.setObjective(sum(b), GRB.MAXIMIZE)#------------------------(1)--

    # Restricciones
    # (2)
    for r in range(k):
        suma = 0
        for i in range(n):
            suma += x[r][i]
        m.addConstr(suma == 1)
    
    # (3)
    for j in range(n):
        suma = 0
        for r in range(k):
            for i in range(n):
                if i >= j:
                    if d[i][j] <= r:
                        suma += x[r][i]
                else:
                    if d[j][i] <= r:
                        suma += x[r][i]
        m.addConstr(b[j] <= suma)
    
    # Solve
    m.optimize()
    runtime = m.Runtime
    #print("Obj:", m.objVal)
    x_out = [[0]*n for i in range(int(m.objVal))]
    for v in m.getVars():
        varName = v.varName
        varNameSplit = varName.split(',')
        if varNameSplit[0] == 'x':
            x_out[int(varNameSplit[1])-1][int(varNameSplit[2])-1] = (v.x)
    # Sequence
    s = []
    for r in reversed(range(k)):
        # Construct burning sequence
        i = 0
        for e in x_out[r]:
            if e == 1:
                s.append(i)
                break
            i += 1
    # Report results
    #print("OPT: " + str(s))
    #print("Max. coverage: " + str(m.objVal))
    #print("The run time is %f" % runtime)
    #print("Final MIP gap value: %f" % m.MIPGap)

    return s

# Binary search
def main(ni, mi, input_file, l, h):
    n = ni
    m = mi
    loadGraph(input_file)
    start_time = time.time()
    while l <= h:
        k = math.floor((l + h) /2)
        #print("--------------------")
        #print("k: " + str(k))
        s = ILP(k)
        if coversAllVertices(s,k,n):
            h = k - 1
            bs = s.copy()
            bs_size = k
        else:
            l = k + 1
    # Best solution
    print("Best solution: ")
    print(bs)
    print("b(G): " + str(len(bs)))
    print("Total time: " + str(time.time()-start_time))

if __name__ == "__main__":
    bs = []
    n = 0
    m = 0
    d = {}
    bs_size = float("inf")
    folder_dataset = 'C:/Users/perro/Documents/GBP/cpp/dataset/'
    dataset = [
        ['karate.mtx',34,78,3,4], # instance, n, m, l, h
        ['chesapeake.mtx',39,170,1,3], # instance, n, m, l, h
        ['dolphins.mtx',62,159,2,6],
        ['rt-retweet.mtx',96,117,2,6],
        ['polbooks.mtx',105,441,2,5],
        ['adjnoun.mtx',112,425,2,5],
        ['ia-infect-hyper.mtx',113,2196,1,3],
        ['C125-9.mtx',125,6963,1,3],
        ['ia-enron-only.mtx',143,623,2,5],
        ['c-fat200-1.mtx',200,1534,3,7],
        ['c-fat200-2.mtx',200,3235,2,5],
        ['c-fat200-5.mtx',200,8473,1,3],
        ['sphere.mtx',258,1026,3,9],
        ['DD244.mtx',291,822,4,11],
        ['ca-netscience.mtx',379,914,3,8],
        ['infect-dublin.mtx',410,2765,2,6],
        ['c-fat500-1.mtx',500,4459,4,11],
        ['c-fat500-2.mtx',500,9139,3,8],
        ['c-fat500-5.mtx',500,23191,2,5],
        ['bio-diseasome.mtx',516,1188,5,13],
        ['web-polblogs.mtx',643,2280,3,8],
        ['DD687.mtx',725,2600,4,10],
        ['rt-twitter-copen.mtx',761,1029,3,9],
        ['DD68.mtx',775,2093,5,14],
        ['ia-crime-moreno.mtx',829,1475,3,8],
        ['DD199.mtx',841,1902,6,16],
        ['soc-wiki-Vote.mtx',889,2914,3,8],
        ['DD349.mtx',897,2087,6,18],
        ['DD497.mtx',903,2453,6,16],
        ['socfb-Reed98.mtx',962,18812,2,5],
        ['lattice3D.mtx',1000,2700,4,12],
        ['bal_bin_tree_9.mtx',1023,1022,4,10],
        ['delaunay_n10.mtx',1024,3056,4,11],
        ['stufe.mtx',1036,1868,5,15],
        ['lattice2D.mtx',1089,2112,7,19],
        ['bal_ter_tree_6.mtx',1093,1092,3,7],
        ['email-univ.mtx',1133,5451,2,6],
        ['econ-mahindas.mtx',1258,7513,2,6],
        ['ia-fb-messages.mtx',1266,6451,2,6],
        ['bio-yeast.mtx',1458,1948,4,11]
        ]
    for i in range(len(dataset)):
        print("________________________________________________")
        instance = dataset[i][0]
        print("instance: " + instance)
        n = dataset[i][1]
        m = dataset[i][2]
        l = dataset[i][3]
        h = dataset[i][4]
        #loadGraph(folder_dataset + dataset[i][0])
        main(n, m, folder_dataset + dataset[i][0], l, h)
