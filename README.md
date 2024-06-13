# Algorithms for graph burning problem
This repository contains:
- A Gurobi implementation of:
  - Two integer linear programs (ILP) for graph burning problem (GBP): ILP-PROP and ILP-COV.
  - An algorithm for GBP modeled as a series of clustered maximum coverage problems (CMCPs). Each CMCP is formulated as an ILP: ILP-CMCP.
- Two greedy heuristics for GBP.

# Citation

<a id="1">[1]</a> Jesús García-Díaz and José Alejandro Cornejo Acosta. "A Greedy Heuristic for Graph Burning." ArXiv PrePrint, January (2024). [https://doi.org/10.48550/arXiv.2401.07577](https://doi.org/10.48550/arXiv.2401.07577).

# Contact

* jesus.garcia@conahcyt.mx
* alexcornejo@inaoep.mx
* https://www.prime.cic.ipn.mx/~jesgadiaz/

# Integer Linear Program
It models the GBP as a series of CMCPs. To run this implementation, you need Gurobi installed. Afterward, on a terminal, run the command:
```
$ python guroby.py
```
The data set must be specified at line 144 in the format:

['name.mtx', n, m, l, h]

Your graph must be in mtx format:
- Vertices are labeled from 1 to n.
- The first line has the number of vertices.
- The second line has the number of edges.
- The third line has an optimal solution.
- The remaining lines are edges. For instance, the mtx file of a path graph P_4 would be:  
4  
3  
2,4  
1 2  
2 3  
3 4  
- n is the number of vertices.
- m is the number of edges.
- l is a lower bound on b(G).
- h is an upper bound on b(G).
For instance,

['karate.mtx', 34, 78, 3, 4]

The output reports the total time consumed (Networkx's breadth-first search and Gurobi) and the optimal solution with vertices labeled from 1 to n.

![karate_output](https://github.com/jesgadiaz/GreedyBurning/blob/main/imgs/karate_gurobi.png?raw=true)

# Greedy heuristics
The data set must be specified at line 240.
The heuristic must be selected at line 239: Gr or GrP.
Compile the code with:
```
$ gcc greedy.cpp -o output.exe
```
or
```
$ gcc greedy.cpp -o output
```
Run with,
```
$ output.exe
```
or
```
$ ./output
```
The output reports the time consumed by breadth-first search, burning farthest first, and the heuristic. The best-found solution is reported with vertices labeled from 1 to n.

![karate_output](https://github.com/jesgadiaz/GreedyBurning/blob/main/imgs/karate_gr.png?raw=true)
