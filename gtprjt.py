import requests
from sys import maxsize
from itertools import permutations

response = requests.get("https://api.mapbox.com/directions-matrix/v1/mapbox/driving/-122.42,37.78;-122.45,37.91;-122.48,37.73;-122.40303222239389,37.798101765891445?approaches=curb;curb;curb;curb&annotations=distance&access_token=pk.eyJ1Ijoic2t5Z3VwdGEzNDUiLCJhIjoiY2xmNDBuNWkxMHk0dTNvcjAzNWE4dDcxOCJ9.q1NkZ5kMRNjsXklpVFFk8Q")


def replace_symmetric(matrix):
    """
    Replace matrix[i][j] and matrix[j][i] with min(matrix[i][j], matrix[j][i]).
    """
    n = len(matrix)

    # Replace matrix[i][j] and matrix[j][i] with min(matrix[i][j], matrix[j][i])
    for i in range(n):
        for j in range(i+1, n):
            val = min(matrix[i][j], matrix[j][i])
            matrix[i][j] = val
            matrix[j][i] = val

    return matrix

# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, s):

    # number of vertices in the graph
    V = len(graph)

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    best_path = []
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = s
        path = [s]
        for j in i:
            current_pathweight += graph[k][j]
            k = j
            path.append(j)
        current_pathweight += graph[k][s]
        path.append(s)

        # update minimum
        if current_pathweight < min_path:
            min_path = current_pathweight
            best_path = path

    return min_path, best_path



dist = response.json()["distances"]

print("Actual matrix: ",dist)

route = replace_symmetric(dist)
s = 0

print("Processed matrix: ",route)

min_weight, best_path = travellingSalesmanProblem(route, s)
print("Minimum weight:", min_weight)
print("Best path:", best_path)