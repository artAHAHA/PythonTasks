from Task2.utils.file_utils import read_matrices_from_file, write_matrices_to_file
from Task2.sort_сolumns import sort_columns

def main(input_filename, output_filename):

    matrices = read_matrices_from_file(input_filename)

    sorted_matrices = [sort_columns(matrix) for matrix in matrices]

    write_matrices_to_file(output_filename, sorted_matrices)


if __name__ == "__main__":
    input_filename = "files/input.txt"
    output_filename = "files/output.txt"
    main(input_filename, output_filename)