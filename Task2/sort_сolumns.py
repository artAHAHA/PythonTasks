"""
6) Отсортировать столбцы переданного двумерного массива по возрастанию со следующим критерием сравнения столбцов.
Один столбец считается большим второго столбца, если первый элемент
(с индексом строки 0) первого столбца больше первого элемента второго столбца
и наоборот в противном случае. Если первые элементы столбцов совпадают,
то аналогичным образом для сравнения столбцов сравниваются вторые элементы столбцов и т.д.
"""

def sort_columns(matrix):
    transposed_matrix = list(zip(*matrix))

    sorted_transposed_matrix = sorted(transposed_matrix)

    sorted_matrix = list(zip(*sorted_transposed_matrix))

    return sorted_matrix
