def read_rectangles(filename):
    """
    Читает прямоугольники из файла.
    Каждая строка файла содержит 4 числа: x1, y1, x2, y2.
    """
    rectangles = []
    with open(filename, 'r') as file:
        for line in file:
            x1, y1, x2, y2 = map(int, line.strip().split())
            rectangles.append(((x1, y1), (x2, y2)))
    return rectangles

def write_result_to_file(filename, best_rectangle, count):
    """
    Записывает результат в файл.
    """
    with open(filename, 'w') as file:
        if best_rectangle:
            file.write(f"Прямоугольник с максимальным количеством вложенных: {best_rectangle}\n")
            file.write(f"Количество вложенных прямоугольников: {count}\n")
        else:
            file.write("Прямоугольники отсутствуют.\n")