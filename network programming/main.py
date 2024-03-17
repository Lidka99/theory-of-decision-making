# task 3

# load data
def load():
    # wczytanie macierzy z pliku
    filepath = r"C:\Users\Lidka\Desktop\teoria podejmowania decyzji\zad3\dane.csv"
    file = open(filepath, "r")
    fr = file.readlines()

    firstLine = True

    for i in fr:
        columns = i.split(";")
        if firstLine == True:
            firstLine = False

            try:
                node_count = int(columns[0])
            except ValueError:
                print("ERROR1")
                return

        else:
            a = 0
            b = 0
            x = 0

            try:
                a = int(columns[0])
            except ValueError:
                print("ERROR2")
                return
            try:
                b = int(columns[1])
            except ValueError:
                print("ERROR3")
                return
            try:
                x = int(columns[2])
            except ValueError:
                print("ERROR4")
                return

            edges.append([a, b, x])

    print("node count: ", node_count)
    print()
    print("edges with length: ")
    print()

    for edge in edges:
        print(edge[0], " - ", edge[1], ": ", edge[2])

    return node_count

def shortest_paths(node):

    neighbours = get_neighbours(node)
    for neighbour in neighbours:

        # sprawdzanie czy etykiety są tymczasowe
        if labels[neighbour - 1][2] == True:
            continue
        length = get_length(node, neighbour)  # odległośc między node i neighbour
        length += labels[node - 1][0]

        if (labels[neighbour - 1][1] == 0) or (labels[neighbour - 1][0] > length):
            labels[neighbour - 1] = [length, node, False]  # etykiety tymczasowe

    min_node = 0
    min_length = float('inf')

    for i in range(len(labels)):
        if (labels[i][2] == True) or (labels[i][1] == 0):
            continue
        if min_length > labels[i][0]:
            min_length = labels[i][0]
            min_node = i + 1
    labels[min_node - 1] = [labels[min_node - 1][0], labels[min_node - 1][1], True]

    if(min_node != 0):
        shortest_paths(min_node)



def get_length(node_a, node_b):
    for edge in edges:
        if (node_a == edge[0] and node_b == edge[1]) or (node_a == edge[1] and node_b == edge[0]):
            return edge[2]
    return -1


def get_neighbours(node):
    neighbours = []
    for edge in edges:
        if edge[0] == node:
            neighbours.append(edge[1])
        elif edge[1] == node:
            neighbours.append(edge[0])
    return neighbours



def get_path(node, path):
    path.append(node)
    if labels[node - 1][1] != node:
        get_path(labels[node - 1][1], path)





    # znalezc wierzchołki sasiadujace z aktualnym i ustalic etykiety, (przejscie po wszystkich krawedziach i sprawdzenie czy ktorys z wierzchołków jest aktualny, jesli tak to ten drugi wierzchołek jest tym który chcemy


# 1. sprawdzenie wierzchołków sąsiadujących z aktualnym, które nie mają stalej etykiety.
# 2. dla nich nadajemy etykiety tymczasowe
# wybieramy z nich tą najniżśzą i przedstawiamy ją jako stałą.


def main():
    node_count = load()

    labels.append([0, 1, True])

    for i in range(node_count - 1):
        labels.append([0, 0, False])
    current_node = 1
    shortest_paths(current_node)

    print()
    print("Najkrótsze drogi - rozwiązanie")
    for i in range (node_count):
        if (i == 0):
            continue
        path = []
        get_path(i + 1, path)
        path.reverse()
        print(i+1, path, labels[i][0])





edges = []
labels = []  # wszystkie zmienne globalne

if __name__ == "__main__":
    main()
