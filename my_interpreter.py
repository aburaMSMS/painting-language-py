# interpreter.py
from my_parser import Parser
import math
from my_eval import my_eval
import numpy as np
import matplotlib.pyplot as plt


class Interpreter:
    def __init__(self, path):
        # 解析输入文件并生成中间代码
        self.mid_code = Parser(path).analyze()

    def create(self):
        # 遍历中间代码，生成并显示绘图
        for i in self.mid_code:
            x_points, y_points, color, linewidth = self.calculate_points(i)
            self.plot(x_points, y_points, color, linewidth)

        self.configure_plot()
        plt.show()

    def calculate_points(self, params):
        # 计算绘图点的坐标、颜色和线宽
        x_points, y_points = [], []

        for T in np.arange(params[3][0], params[3][1], params[3][2]):
            # 根据公式计算 x 和 y 的坐标并伸缩变换
            x = my_eval([v for v in params[4][0]], T) * params[1][0]
            y = my_eval([v for v in params[4][1]], T) * params[1][1]

            # 对坐标进行旋转变换并平移变换
            _x = x * math.cos(params[2]) - y * math.sin(params[2]) + params[0][0]
            _y = y * math.cos(params[2]) + x * math.sin(params[2]) + params[0][1]

            x_points.append(_x)
            y_points.append(_y)

        # 提取颜色信息并将RGB值转换为0-1范围内的值
        color = [c / 255.0 for c in params[5]]
        # 提取线宽信息
        linewidth = params[6]

        return x_points, y_points, color, linewidth

    def plot(self, x_points, y_points, color, linewidth):
        # 绘制散点图，并设置颜色和线宽
        plt.plot(x_points, y_points, color=color, linewidth=linewidth)

    def configure_plot(self):
        # 配置图形显示参数
        plt.tick_params(axis="x", top=True, bottom=False, labeltop=True)
        plt.xlim(0, 5000)
        plt.ylim(5000, 0)
