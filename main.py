from collections import defaultdict
from heapq import heappush, heappop 
from math import sqrt

def prim(graph):
    """
    ### TODO:
    Update this method to work when the graph has multiple connected components.
    Rather than returning a single tree, return a list of trees,
    one per component, containing the MST for each component.

    Each tree is a set of (weight, node1, node2) tuples.    
    """
    def prim_helper(visited, frontier, tree):
        while frontier:
            weight, node, parent = heappop(frontier)
            if node not in visited:
                if weight != 0:
                    tree.add((weight, parent, node))
                visited.add(node)
                for neighbor, w in graph[node]:
                    if neighbor not in visited:
                        heappush(frontier, (w, neighbor, node))
        return tree
    
    visited = set() # store the visited nodes (don't need distance anymore)
    trees = []
    
    for node in graph:
        if node not in visited:
            frontier = []
            heappush(frontier, (0, node, node))
            tree = prim_helper(visited, frontier, set())
            trees.append(tree)
    
    return trees

def test_prim():    
    graph = {
            's': {('a', 4), ('b', 8)},
            'a': {('s', 4), ('b', 2), ('c', 5)},
            'b': {('s', 8), ('a', 2), ('c', 3)}, 
            'c': {('a', 5), ('b', 3), ('d', 3)},
            'd': {('c', 3)},
            'e': {('f', 10)}, # e and f are in a separate component.
            'f': {('e', 10)}
        }

    trees = prim(graph)
    assert len(trees) == 2
    # since we are not guaranteed to get the same order
    # of edges in the answer, we'll check the size and
    # weight of each tree.
    len1 = len(trees[0])
    len2 = len(trees[1])
    assert min([len1, len2]) == 2
    assert max([len1, len2]) == 5

    sum1 = sum(e[0] for e in trees[0])
    sum2 = sum(e[0] for e in trees[1])
    assert min([sum1, sum2]) == 10
    assert max([sum1, sum2]) == 12
    ###



def mst_from_points(points):
    """
    Return the minimum spanning tree for a list of points, using euclidean distance 
    as the edge weight between each pair of points.
    """
    if not points:
        return []
    
    graph = defaultdict(list)
    n = len(points)
    
    for i in range(n):
        for j in range(i+1, n):
            city1, x1, y1 = points[i]
            city2, x2, y2 = points[j]
            distance = euclidean_distance(points[i], points[j])


            graph[city1].append((city2, distance))
            graph[city2].append((city1, distance))
    

    mst = prim(graph)
    return list(mst[0]) if mst else []

def euclidean_distance(p1, p2):
    return sqrt((p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def test_euclidean_distance():
    assert round(euclidean_distance(('a', 5, 10), ('b', 7, 12)), 2) == 2.83

def test_mst_from_points():
    points = [('a', 5, 10), #(city_name, x-coord, y-coord)
              ('b', 7, 12),
              ('c', 2, 3),
              ('d', 12, 3),
              ('e', 4, 6),
              ('f', 6, 7)]
    tree = mst_from_points(points)
    # check that the weight of the MST is correct.
    assert round(sum(e[0] for e in tree), 2) == 19.04

