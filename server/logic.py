def calculate(expression: str) -> float:
    """
    Выводит результат выражения. При невалидном выражении кидает исключение ValueError
    """
    tokens = get_tokens(expression)
    if not is_valid(tokens):
        raise ValueError()

    raise NotImplementedError()

# Токены: float, (, ), +, -, *, /
def get_tokens(expression: str) -> list:
    if expression.isspace():
        raise ValueError()

    tokens = []
    token = ''
    i = 0
    size = len(expression)
    if size == 0:
        raise ValueError()

    while i < size:
        ch = expression[i]

        if ch in ['(', ')', '+', '-', '*', '/']:
            tokens.append(ch)

        elif ch.isdigit():
            was_point = False
            while i < size:
                ch = expression[i]

                if ch.isdigit():
                    token += ch

                elif ch == '.':
                    if was_point:
                        raise ValueError()
                    token += '.'
                    was_point = True
                    if not (i + 1 < size and expression[i + 1].isdigit()):
                        raise ValueError()

                else:
                    tokens.append(token)
                    token = ''
                    i -= 1
                    break

                i += 1

            if i == size:
                tokens.append(token)
                token = ''

        elif ch != ' ':
            raise ValueError()

        i += 1

    return tokens

def is_valid(tokens: list) -> bool:
    i = 0
    size = len(tokens)
    if size == 0:
        return False

    last_is_op = False
    last_is_num = False
    while i < size:
        token = tokens[i]

        if token == '(':
            if not i + 1 < size:
                return False

            if last_is_num:
                return False

            if not (last_is_op or i == 0):
                return False

            left_bracket_count = 1
            right_bracket_count = 0
            right_bracket_index = -1
            for j in range(len(tokens[i + 1:])):
                token = tokens[i + 1 + j]
                if token == '(':
                    left_bracket_count += 1
                elif token == ')':
                    right_bracket_count += 1
                if left_bracket_count == right_bracket_count:
                    right_bracket_index = i + 1 + j
                    break

            if left_bracket_count != right_bracket_count:
                return False

            if not is_valid(tokens[i + 1: right_bracket_index]):
                return False

            i = right_bracket_index
            last_is_num = True
            last_is_op = False

        elif token == ')':
            return False

        elif token[0][0].isdigit():
            if last_is_num:
                return False

            if not (last_is_op or i == 0):
                return False

            last_is_num = True
            last_is_op = False

        elif token in ['*', '/', '+', '-']:
            if not last_is_num:
                if token != '-':
                    return False

            if not (i + 1 < size and (tokens[i + 1] == '(' or tokens[i + 1][0].isdigit())):
                return False

            if last_is_op:
                return False

            last_is_num = False
            last_is_op = True

        i += 1

    return True
