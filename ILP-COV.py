# ILP-COV
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
    string = f.readline()
    for i in range(0, m):
        string = f.readline()
        string = string.split()
        j = int(string[0])-1
        k = int(string[1])-1
        G.add_edge(j, k)
    f.close()
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
    
def ILP(L,k):
    global d
    m = Model("mip1")
    m.Params.outputFlag = 0  # 0 - Off  //  1 - On
    m.setParam("MIPGap", 0.0);
    m.setParam("Presolve", -1); # -1 - Automatic // 0 - Off // 1 - Conservative // 2 - Aggresive 
    m.setParam("TimeLimit", 2*3600000)
    #m.setParam("Heuristics", 0.1)

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
    s1 = 0
    for i in range(k):
        for j in range(n):
            s1 += x[i][j]
    m.setObjective(s1, GRB.MINIMIZE)#------------------------(1)--

    # Restricciones
    # (14)
    for i in range(k):
        suma = 0
        for j in range(n):
            suma += x[i][j]
        m.addConstr(suma <= 1)
    
    # (15)
    for j in range(n):
        suma = 0
        for i in range(k):
            for kk in range(n):
                if kk >= j:
                    if d[kk][j] <= i:
                        suma += x[i][kk]
                else:
                    if d[j][kk] <= i:
                        suma += x[i][kk]
        m.addConstr(b[j] <= suma)

    # (13)
    for i in range(k):
        sum2 = 0
        if i == 0:
            sum1 = 1
        else:
            sum1 = 0
        for j in range(n):
            sum2 += x[i][j]
            if i >= 1:
                sum1 += x[i-1][j]
        m.addConstr(sum2 <= sum1)

    # (16)
    m.addConstr(sum(b) == n)
    
    # Solve
    m.optimize()
    runtime = m.Runtime
    print("Obj:", m.objVal)
    x_out = [[0]*n for i in range(k)]
    for v in m.getVars():
        varName = v.varName
        varNameSplit = varName.split(',')
        if varNameSplit[0] == 'x':
            x_out[int(varNameSplit[1])-1][int(varNameSplit[2])-1] = (v.x)
    # Sequence
    s = []
    #for r in range(int(m.objVal)):
    for r in range(k):
        # Construct burning sequence
        i = 0
        for e in x_out[r]:
            if e == 1:
                s.append(i)
                break
            i += 1
    # Report results
    s.reverse()
    print("OPT: " + str(s))
    print("The run time is %f" % runtime)
    #print("Final MIP gap value: %f" % m.MIPGap)

    return s

# 
def main(ni, mi, input_file, Li, Ui):
    n = ni
    m = mi
    U = Ui
    L = Li
    loadGraph(input_file)
    start_time = time.time()
    s = ILP(L,U)

if __name__ == "__main__":
    bs = []
    n = 0
    m = 0
    d = {}
    bs_size = float("inf")
    folder_dataset = 'C:/Users/perro/Documents/GBP/cpp/dataset/'
    dataset = [
        #['path9.mtx',9,8,1,7],
        #['karate.mtx',34,78,2,3], # instance, n, m, l, h
        #['chesapeake.mtx',39,170,1,3], # instance, n, m, l, h
        #['dolphins.mtx',62,159,2,4],
        #['rt-retweet.mtx',96,117,2,5],
        #['polbooks.mtx',105,441,2,4],
        #['adjnoun.mtx',112,425,2,4],
        #['ia-infect-hyper.mtx',113,2196,1,3],
        #['C125-9.mtx',125,6963,1,3],
        #['ia-enron-only.mtx',143,623,2,4],
        #['c-fat200-1.mtx',200,1534,3,7],
        #['c-fat200-2.mtx',200,3235,2,5],
        #['c-fat200-5.mtx',200,8473,1,3],
        #['sphere.mtx',258,1026,3,7],
        #['DD244.mtx',291,822,4,7],
        #['ca-netscience.mtx',379,914,3,6],
        #['infect-dublin.mtx',410,2765,2,5],
        #['c-fat500-1.mtx',500,4459,4,9],
        #['c-fat500-2.mtx',500,9139,3,7],
        #['c-fat500-5.mtx',500,23191,2,5],
        #['bio-diseasome.mtx',516,1188,5,7],
        #['web-polblogs.mtx',643,2280,3,5],
        #['DD687.mtx',725,2600,4,8],
        #['rt-twitter-copen.mtx',761,1029,3,7],
        #['DD68.mtx',775,2093,5,9],
        #['ia-crime-moreno.mtx',829,1475,3,7],
        #['DD199.mtx',841,1902,6,12],
        #['soc-wiki-Vote.mtx',889,2914,3,6],
        #['DD349.mtx',897,2087,6,12],
        #['DD497.mtx',903,2453,6,11],
        #['socfb-Reed98.mtx',962,18812,2,4],
        #['lattice3D.mtx',1000,2700,4,10],
        #['bal_bin_tree_9.mtx',1023,1022,4,10],
        #['delaunay_n10.mtx',1024,3056,4,9],
        #['stufe.mtx',1036,1868,5,12],
        #['lattice2D.mtx',1089,2112,7,13],
        #['bal_ter_tree_6.mtx',1093,1092,3,7],
        #['email-univ.mtx',1133,5451,2,5],
        #['econ-mahindas.mtx',1258,7513,2,5],
        #['ia-fb-messages.mtx',1266,6451,2,5],
        #['bio-yeast.mtx',1458,1948,4,9],
        #['tech-routers-rf.mtx',2113,6632,3,6],
        #['chameleon.mtx',2277,36101,3,6],
        #['tvshow.mtx',3892,17262,5,9],
        #['facebook.mtx',4039,88234,2,4],
        #['DD6.mtx',4152,10320,9,17],
        #['squirrel.mtx',5201,198493,2,6],
        #['politician.mtx',5908,41729,3,7],
        #['government.mtx',7057,89455,3,6],
        #['crocodile.mtx',11631,170918,3,6],
        #['athletes.mtx',13866,86858,3,7],
        #['company.mtx',14113,52310,4,9],
        #['musae-facebook.mtx',22470,171002,4,8],
        #['new-sites.mtx',27917,106259,3,8],
        #['deezer-europe.mtx',28281,92752,4,10],
        ['grid10x10.mtx',100,180,3,6],
        ['grid20x20.mtx',400,760,5,10],
        ['grid30x30.mtx',900,1740,6,12],
        #['grid40x40.mtx',1600,3120,7,15],
        #['grid50x50.mtx',2500,4900,8,17],
        #['grid60x60.mtx',3600,7080,9,19],
        #['grid70x70.mtx',4900,9660,10,21],
        #['grid80x80.mtx',6400,12640,11,24],
        #['grid90x90.mtx',8100,16020,12,25],
        #['grid320x320.mtx',102400,204160,26,78],
        ]
    for i in range(len(dataset)):
        print("________________________________________________")
        instance = dataset[i][0]
        print("instance: " + instance)
        n = dataset[i][1]
        m = dataset[i][2]
        L = dataset[i][3]
        U = dataset[i][4]
        main(n, m, folder_dataset + dataset[i][0], L, U)
