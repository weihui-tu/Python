def voyageur(graphe, ville):
    path_vertexs = [ville]  # used to store path
    path_length = 0
    path = voyageur_iter(graphe, path_vertexs)
    path_length = getPathLength(graphe, path)
    return (path, path_length)


def voyageur_iter(graphe, path_vertexs):

    next_nodes = sortNextNodes(graphe, path_vertexs)

    for v in next_nodes:
        if len(path_vertexs) == len(graphe):
            # print(path_vertexs)
            return path_vertexs

        path_vertexs.append(v)
        next_nodes2 = sortNextNodes(graphe, path_vertexs)

        # next_nodes2 is used to detect final nodes
        if next_nodes2 == []:
            # Only when path_vertexs[-1] node is not the final node
            if (len(path_vertexs) != len(graphe)):
                path_vertexs.pop()
                if v == next_nodes[-1]:
                    path_vertexs.pop()
            continue

        voyageur_iter(graphe, path_vertexs)



def removeList(a, b):
    if b == []:
        return a
    else:
        for i in b:
            for j in a:
                if i == j:
                    a.remove(i)
        return a

def sortNextNodes(graphe, path_vertexs):
    allNodes = []
    nextNodes = []
    currentNode = path_vertexs[-1]
    row = graphe[currentNode]

    for x in range(0, len(row)):
        if row[x] != -1:
            dic = (x, graphe[currentNode][x])
            allNodes.append(dic)

    # sort the all avaliable neighbor nodes in an ascending order
    # store them in the allNodes List[(tuple)]
    # for example, if currentNode is 0,allNodes are [(3, 3), (1, 5), (4, 5), (2, 7)]
    allNodes = sorted(allNodes, key=lambda s: s[1])
    # print("all sorted nodes are " + str(allNodes))

    # find out those nodes which are also in the restNodes[]
    # To avoid duplicate, our next nodes must be choosed from restNodes[]
    restNodes = [x for x in range(0, len(graphe))]
    removeList(restNodes, path_vertexs)
    for i in allNodes:
        for j in restNodes:
            if i[0] == j:
                nextNodes.append(j)

    return nextNodes

def getPathLength(graphe, path):
    size = len(path)
    sum = 0
    for i in range(size - 1):
        a = path[i]
        b = path[i + 1]
        sum += graphe[a][b]
    return sum

def print_path(vertexs, lengths):
    path = []
    vertexs = [vertex for vertex in vertexs]
    for i, vertex in enumerate(vertexs):
        path += str(vertex)
        if i == 4:
            break
    print("le plus court chemin: " + str(lengths))
    print("le trajet：" + str(path))


if __name__ == "__main__":
    graphe = [[-1, 5, 7, 3, 5],
              [5, -1, -1, -1, 9],
              [7, -1, -1, 2, -1],
              [3, -1, 2, -1, 1],
              [5, 9, -1, 1, -1]]
    ville = int(input("une ville de depart: "))
    path_vertexs, path_length = voyageur(graphe, ville)
    print_path(path_vertexs, path_length)


