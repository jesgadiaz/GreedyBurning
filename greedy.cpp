#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <chrono>
#include <iostream>
#include <fstream>

using namespace std;
using namespace std::chrono;

vector<vector<int>> graph;
vector<vector<int>> d;

vector<vector<int>> allPairsDistance() {
    int n = graph.size();
    vector<vector<int>> distance(n, vector<int> (n, numeric_limits<int>::max()));
    for (int start=0 ; start<n ; start++){
        vector<bool> visited(n, false);
        queue<int> q;
        vector<int> traversal;
        vector<int> d_local(graph.size(), numeric_limits<int>::max());
        d_local[start] = 0;
        visited[start] = true;
        q.push(start);
        while (!q.empty()) {
            int current = q.front();
            q.pop();
            for (int neighbor : graph[current]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                    d_local[neighbor] = d_local[current] + 1;
                }
            }
        }
        for(int i=0;i<n;i++){
                distance[start][i] = d_local[i];
                distance[i][start] = d_local[i];
        }
    }
    return distance;
}

bool validBurningSequence(vector<int> s, int n){
    int counter = 0;
    for(int i=0;i<n;i++){
        int b = s.size();
        for(int j=0;j<b;j++){
                if(d[i][s[j]] <= b - (j+1)){
                    counter += 1;
                    break;
                }
        }
    }
    if (counter == n){
        return true;
    }else{
        return false;
    }
}

vector<int> BFF(int n){
    int first_vertex = 0;
    vector<int> s;
    s.push_back(first_vertex);
    queue<int> q;
    int dist[n];
    int C[n];
    for(int i=0;i<n;i++){
        dist[i] = d[i][0];
        C[i]    = 0;
    }
    int number_of_burned_vertices = 1;
    q.push(0);
    C[0] = 1;
    int farthest_vertex;
    int larger_distance;
    int v;
    while(number_of_burned_vertices<n){
        int q_size = q.size();
        for(int i=0;i<q_size;i++){
            v = q.front();
            q.pop();
            for(int k=0;k<graph[v].size();k++){
                if(C[graph[v][k]]==0){
                    q.push(graph[v][k]);
                    C[graph[v][k]] = 1;
                    number_of_burned_vertices += 1;
                }
            }
        }
        farthest_vertex = 0;
        larger_distance = 0;
        for(int i=0;i<n;i++){
            if(dist[i] > larger_distance){
                larger_distance = dist[i];
                farthest_vertex = i;
            }
        }
        q.push(farthest_vertex);
        s.push_back(farthest_vertex);
        C[farthest_vertex] = 1;
        number_of_burned_vertices += 1;
        for(int i=0;i<n;i++){
            if(d[i][farthest_vertex] < dist[i]){
                dist[i] = d[i][farthest_vertex];
            }
        }
    }
    return s;
}

vector<int> Gr(int n, int k){
    vector<int> s;
    int max_value;
    int max_value_vertex;
    int C[n];
    for(int i=0;i<n;i++){
        C[i]=0;
    }
    vector<vector<int>> A;
    for(int i=0;i<n;i++){
        vector<int> a;
        for(int j=0;j<n;j++){
            if(d[i][j] <= k-1){
                a.push_back(j);
            }
        }
    A.push_back(a);
    }
    vector<int> idxToDelete;
    for(int r=k-1;r>=0;r--){
        if(r<k-1){
            for(int i=0;i<n;i++){
                for(int j=0;j<A[i].size();j++){
                    if(d[i][A[i][j]] > r || C[A[i][j]]==1){
                        idxToDelete.push_back(j);
                    }
                }
                for(int z=idxToDelete.size()-1;z>=0;z--){
                    A[i].erase(A[i].begin()+idxToDelete[z]);
                }
                idxToDelete.clear();
            }
        }
        max_value        = 0;
        max_value_vertex = 0;
        for(int i=0;i<n;i++){
            if(A[i].size() > max_value){
                max_value = A[i].size();
                max_value_vertex = i;
            }
        }
        for(int j=0;j<A[max_value_vertex].size();j++){
            C[A[max_value_vertex][j]] = 1;
        }
        s.push_back(max_value_vertex);
    }
    return s;
}

vector<int> GrP(int n, int k){
    vector<int> s;
    int max_value;
    int max_value_vertex;
    int C[n];
    vector<vector<int>> A_original;
    for(int i=0;i<n;i++){
        vector<int> a;
        for(int j=0;j<n;j++){
            if(d[i][j] <= k-1){
                a.push_back(j);
            }
        }
    A_original.push_back(a);
    }
    vector<vector<int>> A; // copy
    int burned_vertices;
    vector<int> idxToDelete;

    for(int rep=0;rep<n;rep++){
        for(int i=0;i<n;i++){
            C[i]=0;
        }
        A = A_original;
        for(int r=k-1;r>=0;r--){
            if(r<k-1){
                for(int i=0;i<n;i++){
                    for(int j=0;j<A[i].size();j++){
                        if(d[i][A[i][j]] > r || C[A[i][j]]==1){
                            idxToDelete.push_back(j);
                        }
                    }
                    for(int z=idxToDelete.size()-1;z>=0;z--){
                        A[i].erase(A[i].begin()+idxToDelete[z]);
                    }
                    idxToDelete.clear();
                }
            }
            if(r==k-1){
                max_value_vertex = rep;
            }else{
                max_value        = 0;
                max_value_vertex = 0;
                for(int i=0;i<n;i++){
                    if(A[i].size() >= max_value){
                        max_value = A[i].size();
                        max_value_vertex = i;
                    }
                }
            }
            for(int j=0;j<A[max_value_vertex].size();j++){
                C[A[max_value_vertex][j]] = 1;
            }
            s.push_back(max_value_vertex);
        }
        burned_vertices = 0;
        for(int i=0;i<n;i++){
            if(C[i]==1){
                burned_vertices += 1;
            }
        }
        if(burned_vertices==n){
            return s;
        }
        s.clear();
    }
    s.clear();
    return s;
}

int main(int argc, char **argv) {
    int n,m;
    string heuristic   = "Gr";
    vector<string> instances = {"karate", "chesapeake","dolphins","rt-retweet","polbooks","adjnoun","ia-infect-hyper","C125-9","ia-enron-only","c-fat200-1","c-fat200-2","c-fat200-5","sphere","DD244","ca-netscience","infect-dublin","c-fat500-1","c-fat500-2","c-fat500-5","bio-diseasome","web-polblogs","DD687","rt-twitter-copen","DD68","ia-crime-moreno","DD199","soc-wiki-Vote","DD349","DD497","socfb-Reed98","lattice3D","bal_bin_tree_9","delaunay_n10","stufe","lattice2D","bal_ter_tree_6","email-univ","econ-mahindas","ia-fb-messages","bio-yeast"};
    for(string instance : instances){
        graph.clear();
        d.clear();
        cout << "----" + instance + "----" << endl;
        ifstream myfile ("C:\\Users\\perro\\Documents\\GBP\\cpp\\dataset\\" + instance + ".mtx");
        string line;
        stringstream check1(line);
        vector<string> tokens;
        if (myfile.is_open()) {
            getline(myfile, line);
            n = stoi(line);
            graph.resize(n, vector<int>(0));
            for(int i=0;i<n;i++){
                graph[i].push_back(i);
            }
            cout << "n: " << n << endl;
            getline(myfile, line);
            m = stoi(line);
            cout << "m: " << m << endl;
            while (getline(myfile, line)) {
                istringstream iss(line);
                string s;
                int a,b;
                int i = 0;
                while(getline(iss, s, ' '))
                {
                    if (i==0){
                        a = stoi(s) - 1;
                        i = i+1;
                    }
                    if (i==1){
                        b = stoi(s) - 1;
                    }
                }
                graph[a].push_back(b);
                graph[b].push_back(a);
            }
        }
        auto start = high_resolution_clock::now();
        // Compute all-pairs shortest path
        d = allPairsDistance();
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(stop - start);
        double time = duration.count();
        cout << endl <<"All-pairs shortest path running time: " << time << " miliseconds" << endl;
        vector<int> s;
        vector<int> best_burning_sequence;
        int best_burning_sequence_size = numeric_limits<int>::max();
        // BFF solution
        start = high_resolution_clock::now();
        best_burning_sequence = BFF(n);
        best_burning_sequence_size = best_burning_sequence.size();
        stop = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(stop - start);
        time = duration.count();
        cout << endl <<"BFF running time: " << time << " miliseconds" << endl;
        cout << "BFF burning sequence: " << endl;
        for(int v : best_burning_sequence){
            cout << v << " ";
        }
        cout << endl << "Sequence size: " << best_burning_sequence.size() << endl;
        cout << endl;
        // Set lower and upper bounds
        int low  = ceil(best_burning_sequence.size()+2)/3;
        int high = best_burning_sequence.size();
        cout << "lower bound: " << low << endl;
        cout << "upper bound: " << high << endl;
        // Binary search
        start = high_resolution_clock::now();
        while(low <= high){
            int k = floor((high+low)/2);
            if(heuristic == "Gr"){
                s = Gr(n,k);
            }
            if(heuristic == "GrP"){
                s = GrP(n,k);
            }
            if(validBurningSequence(s,n)){
                high = k-1;
                if(s.size() <= best_burning_sequence_size){
                    best_burning_sequence_size = s.size();
                    best_burning_sequence = s;
                }
            }else{
                low = k+1;
            }
        }
        stop = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(stop - start);
        time = duration.count();
        cout << endl << heuristic << " running time: " << time << " miliseconds" << endl;
        cout << "Best burning sequence: " << endl;
        for(int v : best_burning_sequence){
            cout << v << " ";
        }
        cout << endl << "Sequence size: " << best_burning_sequence.size() << endl;
        cout << endl;
    }
    return 0;
}
