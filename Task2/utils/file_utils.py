def read_matrices_from_file(filename):
    """
    Читает несколько матриц из файла.
    Матрицы разделены пустыми строками.
    """
    matrices = []
    current_matrix = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                row = list(map(int, line.split()))
                current_matrix.append(row)
            else:
                if current_matrix:
                    matrices.append(current_matrix)
                    current_matrix = []

        if current_matrix:
            matrices.append(current_matrix)

    return matrices


def write_matrices_to_file(filename, matrices):
    """
    Записывает несколько матриц в файл.
    Матрицы разделяются пустыми строками.
    """
    with open(filename, 'w') as file:
        for matrix in matrices:
            for row in matrix:
                file.write(' '.join(map(str, row)) + '\n')
            file.write('\n')
