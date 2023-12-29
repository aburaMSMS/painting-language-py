# lexer.py
import re
import math


class Lexer:
    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            # 处理注释、换行
            processed_lines = [
                (line.split("//")[0].split("--")[0].split("\n")[0].upper().strip())
                for line in lines
            ]

            self.file_content = "".join(processed_lines)

        # 符号表，用于存储关键字、函数、运算符等的类型和属性
        self.symbol_table = SYMBOL_TABLE

    def analyze(self):
        token_lists = []
        # 分析文件内容，生成符号列表
        sentences = re.split("(;)", self.file_content)

        for sentence in sentences:
            self.current_token_list = []

            if sentence:
                tokens = sentence.split()
                for token in tokens:
                    try:
                        self.process_token(token)
                    except:
                        try:
                            self.handle_argument(token)
                        except:
                            raise SyntaxError()

                token_lists.extend(self.current_token_list)

        return token_lists

    def process_token(self, token):
        # 输出单词及其对应的符号表信息

        if token not in self.symbol_table:
            # 处理数字，并将数字的符号表信息存储
            temp = {
                "TYPE": "NUMBER",
                "VALUE": float(token),
            }

            self.current_token_list.append([token, temp])
        else:
            self.current_token_list.append([token, self.symbol_table[token]])

        # # 新增对LINEWIDTH的处理
        # if token == "LINEWIDTH":
        #     # 匹配 'IS' 后的表达式，并将LINEWIDTH的符号表信息存储
        #     self.match("IS")
        #     line_width_value = self.match()
        #     line_width_info = {
        #         "TYPE": "NUMBER",
        #         "VALUE": float(line_width_value),
        #         ,
        #     }
        #     self.current_token_list.append(["LINEWIDTH", line_width_info])
        #     self.symbol_table["LINEWIDTH"] = line_width_info

    def handle_argument(self, argument):
        # 处理参数，包括变量、函数、数字等
        i = 0
        length = len(argument)

        while i < length:
            if argument[i] == "*":
                i += 1
                if i < length:
                    if argument[i] == "*":
                        self.process_token("**")
                    else:
                        i -= 1
                        self.process_token(argument[i])
                else:
                    self.process_token(argument[i])
            elif argument[i] in "PSCLTE":
                # 匹配大写字母序列，作为函数或关键字
                temp = re.findall(r"[A-Z]+", argument[i:])[0]
                i += len(temp) - 1
                if temp in KEYWORDS and i < length:
                    raise SyntaxError()

                self.process_token(temp)
                if i >= length:
                    break
            elif argument[i] in "0123456789.":
                if argument[i] == ".":
                    i += 1
                    # 匹配数字序列，包括小数点
                    temp = re.findall(r"\d+", argument[i:])[0]
                    i += len(temp) - 1
                    temp = "0." + temp
                    self.process_token(temp)
                else:
                    # 匹配数字序列，包括小数点
                    temp = re.findall(r"\d+\.?\d*", argument[i:])[0]
                    i += len(temp) - 1
                    self.process_token(temp)
                if i >= length:
                    break
            else:
                # 输出单个字符
                self.process_token(argument[i])
            i += 1


KEYWORDS = [
    "ORGIN",
    "SCALE",
    "ROT",
    "IS",
    "FOR",
    "FROM",
    "TO",
    "STEP",
    "DRAW",
    "COLOR",
    "LINEWIDTH",
]


# 符号表，用于存储关键字、函数、运算符等的类型和属性
SYMBOL_TABLE = {
    "PI": {
        "TYPE": "CONST",
        "VALUE": math.pi,
    },
    "E": {
        "TYPE": "CONST",
        "VALUE": math.e,
    },
    "T": {
        "TYPE": "SYMBOL",
        "VALUE": None,
    },
    "SIN": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "COS": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "TAN": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "LN": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "EXP": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "SQRT": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "ASIN": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "ACOS": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    "ATAN": {
        "TYPE": "FUNC",
        "VALUE": None,
    },
    # 关键字
    "ORIGIN": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "SCALE": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "ROT": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "IS": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "FOR": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "FROM": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "TO": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "STEP": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "DRAW": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "COLOR": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    "LINEWIDTH": {
        "TYPE": "KEYWORD",
        "VALUE": None,
    },
    # 运算符
    "+": {
        "TYPE": "OP",
        "VALUE": None,
    },
    "-": {
        "TYPE": "OP",
        "VALUE": None,
    },
    "*": {
        "TYPE": "OP",
        "VALUE": None,
    },
    "/": {
        "TYPE": "OP",
        "VALUE": None,
    },
    "**": {
        "TYPE": "OP",
        "VALUE": None,
    },
    # 记号
    "(": {
        "TYPE": "LEFT",
        "VALUE": None,
    },
    ")": {
        "TYPE": "RIGHT",
        "VALUE": None,
    },
    ",": {
        "TYPE": "MARK",
        "VALUE": None,
    },
    ";": {
        "TYPE": "MARK",
        "VALUE": None,
    },
    "": {
        "TYPE": "MARK",
        "VALUE": None,
    },
    # 数字
    "0": {
        "TYPE": "NUMBER",
        "VALUE": 0.0,
    },
    "1": {
        "TYPE": "NUMBER",
        "VALUE": 1.0,
    },
    "2": {
        "TYPE": "NUMBER",
        "VALUE": 2.0,
    },
    "3": {
        "TYPE": "NUMBER",
        "VALUE": 3.0,
    },
    "4": {
        "TYPE": "NUMBER",
        "VALUE": 4.0,
    },
    "5": {
        "TYPE": "NUMBER",
        "VALUE": 5.0,
    },
    "6": {
        "TYPE": "NUMBER",
        "VALUE": 6.0,
    },
    "7": {
        "TYPE": "NUMBER",
        "VALUE": 7.0,
    },
    "8": {
        "TYPE": "NUMBER",
        "VALUE": 8.0,
    },
    "9": {
        "TYPE": "NUMBER",
        "VALUE": 9.0,
    },
    ".": {
        "TYPE": "NUMBER",
        "VALUE": None,
    },
}

# lexer = Lexer("CODE.txt")
# tokens = lexer.analyze()
# for token, symbol_info in tokens:
#     print(f"Token: {token}, Symbol Info: {symbol_info}")
