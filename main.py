# main.py
from my_interpreter import Interpreter

if __name__ == "__main__":
    # 输入代码
    #     input_code = """
    # color is (255,0,0);
    # linewidth is 10;
    # origin is (2500, 2500);     -- 设置原点的偏移量
    # rot is pi/4;              -- 设置旋转角度
    # scale is (200, 100);      -- 设置横坐标和纵坐标的比例，增大横坐标缩放比例以突显抛物线的形状
    # for t from 0 to 500 step 0.1 draw (t, t*t);
    # -- 绘制一个抛物线，通过调整原点、旋转角度和缩放比例，观察抛物线的形状变化
    # color is (122,100,55);
    # linewidth is 0.5;
    # origin is (300, 100);     -- 更新原点偏移
    # rot is pi/2;              -- 更新旋转角度
    # scale is (100, 100);      -- 恢复等比例

    # for t from 0 to 500 step 0.1 draw (t, sin(t));
    # -- 绘制一个正弦函数曲线，通过调整原点、旋转角度和缩放比例，观察正弦曲线的形状变化

    #     """

    try:
        # 将输入代码字符串写入文件
        # with open("CODE.txt", "w", encoding="utf-8") as f:
        #     f.write(input_code)

        # 创建解释器对象并生成绘图
        interpreter = Interpreter("CODE.txt")

        # 生成绘图
        interpreter.create()

    except Exception as e:
        # 处理异常
        print(f"An error occurred: {e}")
