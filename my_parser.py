import math
from my_lexer import Lexer
from my_eval import my_eval
from copy import deepcopy


class Parser:
    def __init__(self, path):
        # 初始坐标状态
        self.initial_position = [0, 0]
        # 缩放状态
        self.scale_factors = [1, 1]
        # 旋转状态
        self.rotation_angle = 0
        # 循环状态
        self.loop_parameters = [0, 0, 0]
        # 绘图参数
        self.draw_arguments = ["", ""]
        # 颜色状态
        self.color = [0, 0, 0]
        # 线宽 默认为1
        self.line_width = 0.1
        # 词法分析器
        self.lexer = Lexer(path)
        # 词法分析结果
        self.tokens = self.lexer.analyze()
        # 当前处理位置
        self.current_position = 0
        # 词法分析结果长度
        self.tokens_count = len(self.tokens)

    def analyze(self):
        # 中间代码
        intermediate_code = []
        while self.current_position < self.tokens_count:
            if self.tokens[self.current_position][1]["TYPE"] == "KEYWORD":
                keyword = self.tokens[self.current_position][0]
                handlers = {
                    "ORIGIN": self.process_origin,
                    "SCALE": self.process_scale,
                    "ROT": self.process_rotate,
                    "FOR": self.process_for_loop,
                    "COLOR": self.process_color,
                    "LINEWIDTH": self.process_linewidth,
                }
                try:
                    handler = handlers[keyword]
                except:
                    # 语法错误处理
                    raise SyntaxError(f"Unexpected keyword: {keyword}")
                # 移动到下一个词法单元并执行相应的处理函数
                self.current_position += 1
                handler()
                self.match(";")
                # 对于FOR语句，将当前状态添加到中间代码
                if keyword == "FOR":
                    intermediate_code.append(deepcopy(self.get_current_state()))
        # 将中间代码中的表达式字符串转换为实际值
        return intermediate_code

    def process_origin(self):
        # 解析ORIGIN语句
        self.match("IS")
        self.match("(")

        # 匹配参数并更新初始位置
        x = self.expression()
        self.initial_position[0] = my_eval(x)

        self.match(",")

        y = self.expression()
        self.initial_position[1] = my_eval(y)

        self.match(")")

    def process_scale(self):
        # 解析SCALE语句
        self.match("IS")
        self.match("(")

        # 匹配参数并更新缩放因子
        x = self.expression()
        self.scale_factors[0] = my_eval(x)

        self.match(",")

        y = self.expression()
        self.scale_factors[1] = my_eval(y)

        self.match(")")

    def process_rotate(self):
        # 解析ROT语句
        self.match("IS")
        # 匹配表达式并更新旋转角度
        angle = self.expression()
        self.rotation_angle = my_eval(angle)

    def process_for_loop(self):
        # 解析FOR语句
        self.match("T")
        self.match("FROM")

        start = self.expression()
        self.loop_parameters[0] = my_eval(start)

        self.match("TO")
        # 匹配表达式并更新循环结束值
        end = self.expression()
        self.loop_parameters[1] = my_eval(end)
        self.match("STEP")
        # 匹配表达式并更新循环步长
        step = self.expression()
        self.loop_parameters[2] = my_eval(step)
        self.match("DRAW")
        self.match("(")
        # 匹配参数并更新绘图参数
        self.draw_arguments[0] = self.expression()
        self.match(",")
        self.draw_arguments[1] = self.expression()
        self.match(")")

    def process_color(self):
        # 解析COLOR语句
        self.match("IS")
        self.match("(")

        # 匹配参数并更新颜色状态
        r = self.expression()
        self.color[0] = my_eval(r)

        self.match(",")

        g = self.expression()
        self.color[1] = my_eval(g)

        self.match(",")

        b = self.expression()
        self.color[2] = my_eval(b)

        self.match(")")

    def process_linewidth(self):
        # 解析LINEWIDTH语句
        self.match("IS")
        # 匹配参数并更新线宽状态
        self.line_width = my_eval(self.expression())

    def match(self, expected):
        # 如果提供了期望的关键字，检查是否匹配
        if self.tokens[self.current_position][0] == expected:
            self.current_position += 1
        else:
            raise SyntaxError(
                f"Expected {expected}, got {self.tokens[self.current_position][0]} at position {self.current_position}"
            )

    def expression(self):
        temp = []
        sign = -1
        # 循环直到遇到分号、关键字或到达词法单元末尾
        while (
            self.current_position < self.tokens_count
            and self.tokens[self.current_position] != ";"
            and self.tokens[self.current_position][1]["TYPE"] not in ["MARK", "KEYWORD"]
        ):
            token_value = self.tokens[self.current_position][0]
            token = self.tokens[self.current_position][1]

            if token_value == "(":
                sign -= 1

            if token_value == ")":
                if sign == -1:
                    break
                sign += 1

            if token["TYPE"] == "CONST":
                token_value = token["VALUE"]

            temp.append(token_value)
            self.current_position += 1

        if sign != -1:
            raise SyntaxError()

        return temp

    def get_current_state(self):
        return (
            self.initial_position,
            self.scale_factors,
            self.rotation_angle,
            self.loop_parameters,
            self.draw_arguments,
            self.color,
            self.line_width,
        )


# parser = Parser("test.txt")

# try:
#     # 执行语法分析
#     intermediate_code = parser.analyze()

#     # 打印中间代码
#     print("Intermediate Code:")
#     for code_line in intermediate_code:
#         print(code_line)
# except SyntaxError as e:
#     print(f"SyntaxError: {e}")
