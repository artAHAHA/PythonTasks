from Task2.utils.file_utils import read_matrices_from_file, write_matrices_to_file
from Task2.sort_сolumns import sort_columns

def main(input_filename, output_filename):
    matrices = read_matrices_from_file(input_filename)

    sorted_matrices = [sort_columns(matrix) for matrix in matrices]

    write_matrices_to_file(output_filename, sorted_matrices)

    print(f"Данные из файла '{input_filename}' обработаны и сохранены в '{output_filename}'.")


if __name__ == "__main__":
    input_filename = "tests/input.txt"
    output_filename = "tests/output.txt"
    main(input_filename, output_filename)