from django.shortcuts import render
import requests
from sys import maxsize
from itertools import permutations
from django.http import JsonResponse
from config.settings import MAPBOX_KEY

# Create your views here.
def home(request):
    return render(request, 'routefinder/index.html')

def coordinates(request):
    if request.method == "POST":
        coordinates = []
        coordinates.append(request.POST.get('source'))
        dest_count = int(request.POST.get('dest_count'))
        for i in range(1,dest_count+1):
            new_dest = 'dest'+str(i)
            coordinates.append(request.POST.get(new_dest))
        api_req = ";".join(coordinates)
        curb_count = ("curb;"*(dest_count+1)).rstrip(";")
        api_url = f"https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{api_req}?approaches={curb_count}&annotations=distance&access_token={MAPBOX_KEY}"
        print(api_url)
        response = requests.get(api_url)
        dist = response.json()["distances"]
        route = replace_symmetric(dist)

        min_weight, best_path = travellingSalesmanProblem(route)
        optimal_coordinates = []
        for route in best_path:
            optimal_coordinates.append(coordinates[route])
        return JsonResponse({'success': True,'min_weight':min_weight,'best_path':best_path,'optimal_coordinates':optimal_coordinates})
    else:
        return JsonResponse({"success":False})

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
def travellingSalesmanProblem(graph):

    # number of vertices in the graph
    V = len(graph)
    s=0

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