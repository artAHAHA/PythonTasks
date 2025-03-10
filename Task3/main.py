from Task3.find_max_containing_rectangle import find_max_containing_rectangle
from Task3.utils.file_utils import read_rectangles, write_result_to_file


def main(input_filename, output_filename):
    rectangles = read_rectangles(input_filename)
    best_rectangle, count = find_max_containing_rectangle(rectangles)
    write_result_to_file(output_filename, best_rectangle, count)


if __name__ == "__main__":
    input_filename = "files/input05.txt"
    output_filename = "files/output.txt"
    main(input_filename, output_filename)