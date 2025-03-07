# ILP MIN (artículo "greedy heuristics")
import networkx as nx
import math
from gurobipy import *
import numpy as np
import time

# Cargar grafo
def loadGraph(input_file):
    global d
    global G
    G = nx.Graph()
    for j in range(0,n):
        G.add_node(j)

    f = open(input_file, "r")
    string = f.readline()
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
    
def ILP(U,w):
    global d
    global G
    m = Model("mip1")
    m.Params.outputFlag = 0  # 0 - Off  //  1 - On
    m.setParam("MIPGap", 0.0);
    m.setParam("Presolve", -1); # -1 - Automatic // 0 - Off // 1 - Conservative // 2 - Aggresive 
    m.setParam("TimeLimit", 2*3600000)

    # Definir variables
    b  = [ [0] * n for i in range(U)] # b_{i,j}
    s  = [ [0] * n for i in range(U)] # s_{i,j}
    c = [0] * U

    for j in range(U):
        for i in range(n):
            b[j][i] = m.addVar(vtype=GRB.BINARY, name="b,%s" % str(j+1) + "," + str(i+1))
    for j in range(U):
        for i in range(n):
            s[j][i] = m.addVar(vtype=GRB.BINARY, name="s,%s" % str(j+1) + "," + str(i+1))
    for j in range(U):
        c[j] = m.addVar(vtype=GRB.BINARY, name="c,%s" % str(j+1))

    # Función objetivo
    # (1)
    m.setObjective(sum(c), GRB.MINIMIZE)#------------------------(1)--

    # Restricciones

    # (2)
    for j in range(U):
        suma = 0
        for i in range(n):
            suma += s[j][i]
        m.addConstr(suma == w)

    # (3)
    for j in range(U):
        for i in range(n):
            suma = 0
            closed_neighbors = [u for u in G.neighbors(i)]
            closed_neighbors.append(i)
            for k in closed_neighbors:
                if j == 0:
                    suma += 0
                else:
                    suma += b[j-1][k]
            m.addConstr(b[j][i] <= s[j][i] + suma)
    
    # (4)
    for j in range(U):
        for i in range(n):
            m.addConstr(c[j] >= 1-b[j][i])

    # Solve
    m.optimize()
    runtime = m.Runtime
    print("Obj:", m.objVal)
    burning_number = int(m.objVal)+1
    s_out = [[0] * n for i in range(U)]
    for v in m.getVars():
        varName = v.varName
        varNameSplit = varName.split(',')
        if varNameSplit[0] == 's':
            s_out[int(varNameSplit[1])-1][int(varNameSplit[2])-1] = (v.x)
    # Sequence
    s = []
    for i in range(w):
        s.append([])
    for j in range(burning_number):
        p = 0
        for i in range(n):
            if s_out[j][i] == 1:
                s[p].append(i)
                p += 1

    # Report results
    
    print("Solution: " + str(s[:int(m.objVal)+1]))
    print("The run time is %f" % runtime)
    #print("Final MIP gap value: %f" % m.MIPGap)

    return s

def main(ni, mi, input_file, Ui):
    n = ni
    m = mi
    w = 1
    U = Ui
    loadGraph(input_file)
    start_time = time.time()
    s = ILP(U,w)

if __name__ == "__main__":
    bs = []
    n = 0
    m = 0
    d = {}
    bs_size = float("inf")
    folder_dataset = 'C:/Users/perro/Documents/GBP/cpp/dataset/'
    dataset = [
        ['grid5x5.mtx',25,40,3,5],
        ['grid6x6.mtx',36,60,3,6],
        ['grid7x7.mtx',49,84,3,6],
        ['grid8x8.mtx',64,112,3,7],
        ['grid9x9.mtx',81,144,4,7],
        ['grid10x10.mtx',100,180,3,8],
        #['grid20x20.mtx',400,760,5,13],
        #['grid30x30.mtx',900,1740,6,17],
        #['grid40x40.mtx',1600,3120,7,20],
        #['grid50x50.mtx',2500,4900,8,23],
        #['path4_2.mtx',8,6,1,4],
        #['path9_3.mtx',27,24,1,5],
        #['karate.mtx',34,78,2,4], # instance, n, m, l, h=U
        #['chesapeake.mtx',39,170,1,3], # instance, n, m, l, h=U
        #['dolphins.mtx',62,159,2,6],
        #['rt-retweet.mtx',96,117,2,6],
        #['polbooks.mtx',105,441,2,5],
        #['adjnoun.mtx',112,425,2,5],
        #['ia-infect-hyper.mtx',113,2196,1,3],
        #['C125-9.mtx',125,6963,1,3],
        #['ia-enron-only.mtx',143,623,2,5],
        #['c-fat200-1.mtx',200,1534,3,7],
        #['c-fat200-2.mtx',200,3235,2,5],
        #['c-fat200-5.mtx',200,8473,1,3],
        #['sphere.mtx',258,1026,3,9],
        #['DD244.mtx',291,822,4,11],
        #['ca-netscience.mtx',379,914,3,8],
        #['infect-dublin.mtx',410,2765,2,6],
        #['c-fat500-1.mtx',500,4459,4,11],
        #['c-fat500-2.mtx',500,9139,3,8],
        #['c-fat500-5.mtx',500,23191,2,5],
        #['bio-diseasome.mtx',516,1188,5,13],
        #['web-polblogs.mtx',643,2280,3,8],
        #['DD687.mtx',725,2600,4,10],
        #['rt-twitter-copen.mtx',761,1029,3,9],
        #['DD68.mtx',775,2093,5,14],
        #['ia-crime-moreno.mtx',829,1475,3,8],
        #['DD199.mtx',841,1902,6,16],
        #['soc-wiki-Vote.mtx',889,2914,3,8],
        #['DD349.mtx',897,2087,6,18],
        #['DD497.mtx',903,2453,6,16],
        #['socfb-Reed98.mtx',962,18812,2,5],
        #['lattice3D.mtx',1000,2700,4,12],
        #['bal_bin_tree_9.mtx',1023,1022,4,10],
        #['delaunay_n10.mtx',1024,3056,4,11],
        #['stufe.mtx',1036,1868,5,15],
        #['lattice2D.mtx',1089,2112,7,19],
        #['bal_ter_tree_6.mtx',1093,1092,3,7],
        #['email-univ.mtx',1133,5451,2,6],
        #['econ-mahindas.mtx',1258,7513,2,6],
        #['ia-fb-messages.mtx',1266,6451,2,6],
        #['bio-yeast.mtx',1458,1948,4,11]
        ]
    for i in range(len(dataset)):
        print("________________________________________________")
        instance = dataset[i][0]
        print("instance: " + instance)
        n = dataset[i][1]
        m = dataset[i][2]
        U = dataset[i][4]
        #loadGraph(folder_dataset + dataset[i][0])
        main(n, m, folder_dataset + dataset[i][0], U)
