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


# funkcja max
def maxi(y):
    index = 0
    max_y = y[0]
    max_index = 0

    for z in y:

        if max_y < z:
            max_y = z
            max_index = index
        index += 1
    return max_y, max_index


# funkcja od wyboru wariantów
def f(y):
    match y:
        case '1':
            min_rows = []
            for row in matrix:
                min_rows.append(min(row))
            m = maxi(min_rows)
            print(f"max(min) = {m[0]}")
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])

            return

        case '2':
            max_rows = []
            for row in matrix:
                max_rows.append(max(row))
            m = maxi(max_rows)
            print(f"max(max) = {m[0]}")
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])
            return

        case '3':
            wsp = 0.0
            while True:
                try:
                    wsp = float(input("Podaj współczynnik ostrożności (między 0 a 1): "))
                    if 0 <= wsp <= 1:
                        break
                    else:
                        print("Podaj wartość z przedziału (0,1)")
                except ValueError:
                    print("Podaj wartość zmiennoprzecinkową")

            min_rows = []
            for row in matrix:
                min_rows.append(wsp * min(row) + (1 - wsp) * max(row))
            m = maxi(min_rows)
            # print(f"max(min) = {m[0]}")
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])
            return

        case '4':
            columns = len(matrix[0])
            wsp = []
            min_rows = []
            print("Podaj prawdopodobieństwa sumujące sie do 1 dla wszystkich prócz ostatniego stanu natury")
            for col in range(columns - 1):
                while True:
                    try:
                        temp_wsp = float(input(f" Podaj prawdopodobieństwo {col+1} w wartości zmiennoprzecinkowej: "))
                        if sum(wsp) <= 1:
                            wsp.append(temp_wsp)
                            break
                    except ValueError:
                        print("Podaj wartość zmiennoprzecinkową")

            wsp.append(1 - sum(wsp))

            for row in matrix:
                suma = 0
                for col in range(columns):
                    suma += wsp[col] * row[col]
                min_rows.append(suma)  # wsp * suma komórek
            m = maxi(min_rows)
            print(f"max(min) = {m[0]}")
            print(f"współczynniki: {wsp}")
            print(min_rows)
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])
            return

        case '5':
            wsp = (1 / len(matrix[0]))
            min_rows = []
            for row in matrix:
                min_rows.append(wsp * sum(row))  # wsp * suma komórek
            m = maxi(min_rows)
            print(f"max(min) = {m[0]}")
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])
            return

        case '6':
            min_rows = []
            max_cols = []
            for col in range(len(matrix[0])):
                max_cols.append(matrix[0][col])
                for row in matrix:
                    if max_cols[col] < row[col]:
                        max_cols[col] = row[col]

            for row in matrix:
                wsp = []
                for col in range(len(row)):
                    wsp.append(max_cols[col] - row[col])
                min_rows.append(max(wsp))
            m = mini(min_rows)
            print(f"maksimum z kolumn: {max_cols}")
            print(f"najmniejsza maksymalna strata: {min_rows}")
            print(f"Najlepszym wariantem będzie wariant nr = {m[1] + 1}")
            print(matrix[m[1]])
            return

        case _:
            print("Nie wybrałeś żadnej opcji")
            return


# wczytanie macierzy z pliku
def main():

    filepath = r"C:\Users\Lidka\Desktop\teoria podejmowania decyzji\zad1\macierz.txt"
    file = open(filepath, "r")
    fr = file.readlines()



    for i in fr:
        a = []
        for number in i.split(","):
            try:
                a.append(float(number))
            except ValueError:
                print("ERROR")
                return

        matrix.append(a)

    #sprawdzanie czy macierz jest prostokątna
    columns = len(matrix[0])
    for row in matrix:
        if len(row) != columns:
            print("ERROR")
            return

    #wyświetlanie macierzy
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print()

    # wybór metody przez użytkownika
    print(
        " 1. Kryterium Walda\n 2. Kryterium optymistyczne\n 3. Kryterium Hurwicza\n 4. Kryterium Bayesa Laplacea przy różnych prawdopodobieństwach\n 5. Kryterium Bayesa Laplacea przy jednakowych prawdopodobieńśtwach\n 6. Kryterium Savagea\n")
    x = input("Wybierz metodę którą chcesz rozwiązać zadanie: ")

    f(x)


matrix = []


if __name__ == "__main__":
    main()

