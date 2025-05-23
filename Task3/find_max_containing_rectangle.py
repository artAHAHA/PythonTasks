"""
Для набора прямоугольников, стороны которых параллельны OX и OY,
заданных координатами 2-х диагональных вершин, найти прямоугольник,
внутри которого расположено максимальное кол-во других прямоугольников
(граница вложенного прямоугольника может проходить по границе внешнего прямоугольника).
В случае существования нескольких подходящих прямоугольников – выбрать максимальной площади
(если и таких будет несколько – то произвольный).
"""


def is_inside(rect_a, rect_b):
    (ax1, ay1), (ax2, ay2) = rect_a
    (bx1, by1), (bx2, by2) = rect_b

    ax_min, ax_max = min(ax1, ax2), max(ax1, ax2)
    ay_min, ay_max = min(ay1, ay2), max(ay1, ay2)

    bx_min, bx_max = min(bx1, bx2), max(bx1, bx2)
    by_min, by_max = min(by1, by2), max(by1, by2)

    return (ax_min >= bx_min and ax_max <= bx_max and
            ay_min >= by_min and ay_max <= by_max)


def rectangle_area(rect):
    (x1, y1), (x2, y2) = rect
    return abs(x2 - x1) * abs(y2 - y1)


def find_max_containing_rectangle(rectangles):
    max_count = -1
    best_rectangle = None

    for i, rect in enumerate(rectangles):
        count = 0
        for j, other_rect in enumerate(rectangles):
            if i != j and is_inside(other_rect, rect):
                count += 1

        if count > max_count:
            max_count = count
            best_rectangle = rect

        elif count == max_count:
            if rectangle_area(rect) > rectangle_area(best_rectangle):
                best_rectangle = rect

    return best_rectangle, max_count
