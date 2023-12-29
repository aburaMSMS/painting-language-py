import math


def infix_to_postfix(tokens, T):
    precedence = {
        "(": 0,
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "**": 3,
        "SIN": 4,
        "COS": 4,
        "TAN": 4,
        "LN": 4,
        "EXP": 4,
        "SQRT": 4,
        "ASIN": 4,
        "ACOS": 4,
        "ATAN": 4,
    }
    output = []
    stack = []

    unary = True
    unary_num = 0

    temp = [token for token in tokens]

    for index, token in enumerate(temp):
        index += unary_num

        if token == "T":
            tokens[index] = T

        if unary:
            if token in ["+", "-"]:
                tokens = tokens[0:index] + [0] + tokens[index:]
                unary_num += 1
                unary = False
            else:
                unary = False

        if token == "(":
            unary = True

    for token in tokens:
        try:
            num = float(token)
            output.append(num)
        except:
            if token not in "()":
                while (
                    stack
                    and stack[-1] not in "()"
                    and precedence[token] <= precedence[stack[-1]]
                ):
                    output.append(stack.pop())
                stack.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()

    while stack:
        output.append(stack.pop())

    return output


def my_eval(tokens, T=0.0):
    postfix_expression = infix_to_postfix(tokens, T)

    postfix_expression
    try:
        result = []
        for v in postfix_expression:
            try:
                float(v)
                result.append(v)
            except:
                z = 0.0
                if v in ["+", "-", "*", "/", "**"]:
                    y = result.pop()
                    x = result.pop()

                    if v == "+":
                        z = x + y
                    elif v == "-":
                        z = x - y
                    elif v == "*":
                        z = x * y
                    elif v == "/":
                        z = x / y
                    elif v == "**":
                        z = x**y
                else:
                    x = result.pop()

                    if v == "SIN":
                        z = math.sin(x)
                    elif v == "COS":
                        z = math.cos(x)
                    elif v == "TAN":
                        z = math.tan(x)
                    elif v == "LN":
                        z = math.log(x)
                    elif v == "EXP":
                        z = math.exp(x)
                    elif v == "SQRT":
                        z = math.sqrt(x)
                    elif v == "ASIN":
                        z = math.asin(x)
                    elif v == "ACOS":
                        z = math.acos(x)
                    elif v == "ATAN":
                        z = math.atan(x)

                result.append(z)

        if len(result) != 1:
            raise SyntaxError()

        float(result[0])

    except Exception as e:
        raise e

    return result[0]
