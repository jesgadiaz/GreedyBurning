# Algorithms for graph burning problem.
This repository contains:
- One integer linear program (ILP) for graph burning problem (GBP) modeled as a series of clustered maximum coverage problems (CMCPs).
- Two greedy heuristics for GBP.

(A PrePrint is soon to be published.)

# Integer Linear Program
It models the GBP as a series of CMCPs. To run this implementation you need Gurobi to be installed. Afterward, on a terminal run the command:
```
$ python ILP.py
```
The data set must be specified at line 144 with the format:

[name.mtx, n, m, l, h]

Your graph must be in mtx format:
- Vertices are labeled from 1 to n.
- The first line has the number of vertices.
- The second line has the number of edges.
- The remaining lines have an edge. For instance, the mtx file of a path graph P_4 would be:  
4  
3  
1 2  
2 3  
3 4  
- n is the number of vertices.
- m is the number of edges.
- l is a lower bound on b(G).
- h is an upper bound on b(G).
For instance,

['karate.mtx', 34, 78, 3, 4]
