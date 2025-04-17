def remove_parentheses(text):
    result = []
    level = 0

    for char in text:
        if char == '(':
            level += 1
        elif char == ')':
            level -= 1
        elif level == 0:
            result.append(char)

    return ''.join(result)