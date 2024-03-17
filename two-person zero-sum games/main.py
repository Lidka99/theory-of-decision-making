import numpy as np
import pandas as pd
from scipy.optimize import linprog

#funkcja do printowania ze zmniejszoną liczba po przecinku
def print_tab(tab):
    s = "["
    for i in range(len(tab)):
        s += "%.2f"%tab[i]
        if i < len(tab)-1:
            s += " "
    s += "]"
    return s

# funkcja min
def mini(y):
    index = 0
    min_y = y[0]
    min_index = 0

    for z in y:

        if min_y > z:
            min_y = z
            min_index = index
        index += 1
    return min_y, min_index


# funkcja do redukcji macierzy

def zredukuj():
    kolumny = len(matrix[0])
    wiersze = len(matrix)

    # usuwanie kolumn
    i = 0

    while i < kolumny:
        j = 0
        while j < kolumny:
            if i == j:
                j += 1
                continue
            czyWieksze = False
            czyZdominowana = True

            for k in range(len(matrix)):
                if matrix[k][i] > matrix[k][j]:
                    czyWieksze = True
                elif matrix[k][i] < matrix[k][j]:
                    czyZdominowana = False
                    break
            if czyZdominowana == False or czyWieksze == False:
                j += 1
                continue

            for k in range(len(matrix)):

                a = matrix[k][0:i]
                if (i < len(matrix[k]) - 1):
                    a.append(matrix[k][i + 1:len(matrix[k])])
                matrix[k] = a

            i -= 1

            kolumny = len(matrix[0])

        i += 1

    # usuwanie wierszy
    k = 0

    while k < wiersze:
        l = 0
        while l < wiersze:
            if k == l:
                l += 1
                continue

            czyMniejsze = False
            czyZdominowana = True

            for m in range(kolumny):
                if matrix[k][m] < matrix[l][m]:
                    czyMniejsze = True
                elif matrix[k][m] > matrix[l][m]:
                    czyZdominowana = False
                    break

            if czyZdominowana == False or czyMniejsze == False:
                l += 1
                continue

            matrix.remove(matrix[k])
            k -= 1

            wiersze = len(matrix)

        k += 1

    return


# metoda Von Neumana

def von_neumann():
    mins_tab = []
    for k in range(len(matrix)):
        mins_tab.append(min(matrix[k]))

    v_a = max(mins_tab)
    maks_tab = []

    for i in range(len(matrix[0])):
        maks = matrix[0][i]
        for k in range(len(matrix)):
            if (maks < matrix[k][i]):
                maks = matrix[k][i]

        maks_tab.append(maks)

    v_b = min(maks_tab)

    print("v_a wynosi: ", v_a)
    print("v_b wynosi: ", v_b)
    print()

    punkt_siodlowy = v_a == v_b
    if punkt_siodlowy == True:
        print("Gra ma punkt siodłowy. Wartość gry jest równa ", v_a)
        if (v_a == 0):
            print("Gra jest grą sprawiedliwą.")

        return

    print(
        "Gra nie posiada punktu siodłowego, więc nie jesteśmy w stanie znaleźć rozwiązania w zbiorze strategii czystych")
    print()

    # dla macierzy 2 X 2
    if len(matrix) == 2 and len(matrix[0]) == 2:
        # rozwiązanie dla gracza a bez punktu siodłowego
        a = np.array([[matrix[0][0] - matrix[0][1], matrix[1][0] - matrix[1][1]], [1, 1]])
        ab = np.array([0, 1])
        az = np.linalg.solve(a, ab)
        print("Mieszana strategia gracza a: ", az)
        v_a2 = matrix[0][0] * az[0] + matrix[1][0] * az[1]
        print("Wynik dla gracza a zmienił się z ", v_a, " na ", v_a2)
        print()

        # rozwiązanie dla gracza b bez punktu siodłowego
        b = np.array([[matrix[0][0] - matrix[1][0], matrix[0][1] - matrix[1][1]], [1, 1]])
        bb = np.array([0, 1])
        bz = np.linalg.solve(b, bb)
        print("Mieszana strategia gracza b: ", bz)
        v_b2 = matrix[0][0] * bz[0] + matrix[0][1] * bz[1]
        print("Wynik dla gracza b zmienił się z ", v_b, " na ", v_b2)
        print()
        print("Wartość  gry wynosi: (", v_a, ", ", v_b, ")")

    # SYMPLEKS
    print("Znajdowanie strategii optymalnych metodą programowania liniowego")
    print()

    # Przekształcenie macierzy w macierz o elementach dodatnich

    minim = min(mins_tab)
    if minim < 0:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] -= minim

    if minim != 0:
        print("Przekształcenie macierzy w macierz o elementach dodatnich przez dodanie stałej: ", -(minim))
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j], end=" ")
            print()
        print()

    # zagadnienie pierwotne dla gracza A
    AA = []
    BB = []
    CC = []

    for j in range(len(matrix[0])):
        AJ = []
        for i in range(len(matrix)):
            AJ.append(-matrix[i][j])
        AA.append(AJ)
        BB.append(-1)

    for i in range(len(matrix)):
        tab = []
        for j in range(len(matrix)):
            if i == j:
                tab.append(-1)
            else:
                tab.append(0)
        AA.append(tab)
        BB.append(0)
        CC.append(1)

    A2 = np.array(AA)
    B2 = np.array(BB)
    C2 = np.array(CC)

    res = linprog(C2, A_ub=A2, b_ub=B2, bounds=(0, None))

    print("Gracz A")

    print('X\':', print_tab(res.x))
    v = 1/res.fun

    x = res.x * v
    v += minim
    print("wartość gry: v = ", "%.2f" % v)
    print("x = ", print_tab(x))

    # zadanie dualne dla gracza B
    BAA = []
    BBB = []
    BCC = []

    for i in range(len(matrix)):
        AJ = []
        for j in range(len(matrix[0])):
            AJ.append(matrix[i][j])
        BAA.append(AJ)
        BBB.append(1)

    for i in range(len(matrix[0])):
        BCC.append(-1)

    BA2 = np.array(BAA)
    BB2 = np.array(BBB)
    BC2 = np.array(BCC)
    bres = linprog(BC2, A_ub=BA2, b_ub=BB2, bounds=(0, None))

    print()
    print("Gracz B")

    print('y\':', print_tab(bres.x))
    bv = -(1 / bres.fun)

    bx = bres.x * bv
    bv += minim
    print("wartość gry: v = ", "%.2f" % bv)
    print("y = ", print_tab(bx))


def main():
    # wczytanie macierzy z pliku
    filepath = r"C:\Users\Lidka\Desktop\teoria podejmowania decyzji\zad2\macierz.csv"
    file = open(filepath, "r")
    fr = file.readlines()

    for i in fr:
        a = []
        for number in i.split(";"):
            try:
                a.append(float(number))
            except ValueError:
                print("ERROR")
                return

        matrix.append(a)

    # sprawdzanie czy macierz jest prostokątna
    columns = len(matrix[0])
    for row in matrix:
        if len(row) != columns:
            print("ERROR")
            return

    # wyświetlanie macierzy
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print()
    zredukuj()
    print()
    print("Po redukcji")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print()
    print()

    von_neumann()


matrix = []

if __name__ == "__main__":
    main()
