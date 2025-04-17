from Task4.remove_parentheses import remove_parentheses


def main(input_filename, output_filename):

    with open(input_filename, "r") as input_file:
        input_text = input_file.read().strip()

    cleaned_text = remove_parentheses(input_text)

    with open(output_filename, "w") as output_file:
        output_file.write(cleaned_text)

    print(f"Текст из файла '{input_filename}' обработан и сохранен в '{output_filename}'.")

if __name__ == "__main__":
    input_filename = "tests/input07.txt"
    output_filename = "tests/output.txt"
    main(input_filename, output_filename)