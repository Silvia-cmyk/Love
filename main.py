import random
import sys
from math import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QPen
from data import data
# 處理上述座標
new_code_list = data
# 輸出座標
# for order2, test_code in enumerate(test):
#     if order2 + 1 < len(test):
#         # 0.25為間隔，計算兩點之間需要分成多少份
#         pointnum_x = int(abs(test[order2+1][0]-test[order2][0])/0.25)
#         pointnum_y = int(abs(test[order2+1][1]-test[order2][1])/0.25)
#         # 分布均勻，避免太密集
#         pointnum = max(pointnum_x, pointnum_y)
#         # 計算兩點之間橫縱左邊最小距離
#         step_x = ((test[order2+1][0]-test[order2][0])/pointnum)
#         step_y = ((test[order2+1][1]-test[order2][1])/pointnum)
#         # 得出座標x,y值
#         for i in range(pointnum):
#             new_code = (round(test[order2][0]+(i + 1) * step_x,2),
#                         round(test[order2][1]+(i + 1) * step_y,2))
#             if new_code not in new_code_list:
#                 new_code_list.append(new_code)
# print(new_code_list)
# turtle.exitonclick()


# pyqt5定義類別
class Heartwindows(QMainWindow):
    # 類別初始化init
    def __init__(self):
        # 繼承
        super(Heartwindows, self).__init__(None)
        # 基礎設置
        self.setWindowTitle("Surprise Gift")
        # 尺寸
        self.resize(QDesktopWidget().screenGeometry().width(),
                    QDesktopWidget().screenGeometry().height())
        # 位置
        self.move(0, 0)
        # 設置Windows為背景：黑
        self.setStyleSheet("QMainWindow{background-color:#000000}")

        # 核心過程
        # 刷新時間1000=1s（電腦運算力不夠會不流暢）
        self.startTimer(50)
        # 顯示第幾個介面（10->不規律的循環產生心跳效果）
        self.readlist = 0
        # 確定是否收縮還是舒展
        self.largen = True
        # 確定heart中心點橫向座標
        self.cen_x = QDesktopWidget().screenGeometry().width() / 2
        # 確定heart中心點縱向座標
        self.cen_y = QDesktopWidget().screenGeometry().height() / 2 - 50
        # 彌補heart中心空洞矩形範圍的一半
        self.cent = 100
        # 生成所有點的座標及屬性
        self.makecode()

    # 產生中間heart的點座標、大小、顏色
    def makecode(self):
        # 主愛心的點
        # 初始化heart的座標列表
        self.code_list = []
        # 初始化heart跳動（每幀）所有座標列表
        self.all_code_list_jump = []
        # 確定heart從外層到內層，各個層級密集度  # x平方＋y平方=100公式確定延伸；當x趨近0時，y值大且變化平緩，符合外密內稀
        intensity_list = [int(9 * round(sqrt(10000 - (i * i)), 4)) + 200 for i in range(0, 105, 5)]
        # 循環讀取稠密程度列表
        for order, intensity in enumerate(intensity_list):
        # 偏移程度參數，越內圈越離散
            offset = int((len(intensity_list)-sqrt((len(intensity_list)**2)-((order+1)**2))+order+2)*0.8)
        # 讀取愛心座標生成更多的點
            for new_code in new_code_list:
                # ✦控制生成點，目前輸出1/8的點
                if random.randint(1, 8) == 1:
                # 隨機生成點的尺寸，有大有小
                    size = random.randint(1, 4)
                # 調用上邊稠密程度參數生成內外各層級的點
                    heart_x = (new_code[0] * (sqrt(intensity) * 0.024))
                    heart_y = (new_code[1] * (sqrt(intensity) * 0.026))
                # 屏幕左上角為pyqt5（0, 0）點，轉換為屏幕中心的點
                    x = int((heart_x) + self.width() / 2)
                    y = int((-heart_y) + self.height() / 2)
                # 隨機生成偏移量
                    draw_x = x + random.randint(-offset, offset)
                    draw_y = y + random.randint(-offset, offset)
                # ✦隨機生成顏色
                    color_int = random.randint(1, 7)
                    if color_int == 1:
                        color = QColor(190, 43, 77)
                    elif color_int == 2:
                        color = QColor(255, 181, 198) #白粉
                    elif color_int == 3:
                        color = QColor(255, 20, 147)  # 深紅
                    elif color_int == 4:
                        color = QColor(232, 51, 92)
                    elif color_int == 5:
                        color = QColor(255, 0, 0)  # red
                # 根據顏色需求調解以下，白色較多，就在下面再引用白粉色
                    else:
                        color = QColor(255, 181, 198) #白粉
                # 省內存，畫面流暢，添加不同座標、屬性的點
                    if (draw_x, draw_y, size, color) not in self.code_list:
                        self.code_list.append((draw_x, draw_y, size, color))
        # 初始化的愛心點列表作為畫面第一幀
        self.all_code_list_jump.append(self.code_list)

        # 跳動效果（目前分10幀，所以要生成後9幀的點）
        for jump in range(1, 10):
            code_temporary = []
            # 第一幀所有的點
            for code in self.code_list:
                # 跳動的公式->基本原理根據各點與中心點距離遠近去改變向外放大的程度，就有內圈變化劇烈的效果
                flexible = ((536-1.11111111111*sqrt(((code[0]-self.cen_x)**2) +
                                                    ((code[1]-self.cen_y)**2)))*(0.00006)*jump)-(jump*0.01+0.017)
                # 放大參數為正數
                if flexible < 0:
                    flexible = 0
                # 特定點為中心放大縮小公式
                center_x = self.cen_x - (1 + flexible) * (self.cen_x - code[0])
                center_y = self.cen_y - (1 + flexible) * (self.cen_y - code[1])
                # 收集
                code_temporary.append((center_x, center_y, code[2], code[3]))
            # 保存到下一幀
            self.all_code_list_jump.append(code_temporary)


        # heart向外飄散的點;同產生主愛心的原理一樣，參數調整
        self.code_list_out = []
        self.all_code_list_out = []  #此點無規律變化
        # 只到90不然不好看
        intensity_list = [int(round(sqrt(10000 - (i * i)) + 100 - i, 4)) for i in range(0, 92, 5)]
        for order, intensity in enumerate(intensity_list):
            offset = int(len(intensity_list) - sqrt((len(intensity_list) ** 2) - ((order + 1) ** 2)) + 2) + 10
            for out_code in new_code_list:
                if random.randint(1, 7) == 1:
                    size = random.randint(1, 3)
                    heart_x = out_code[0] * (sqrt(intensity) * 0.075)
                    heart_y = out_code[1] * (sqrt(intensity) * 0.078)
                    x = int((heart_x) + self.width() / 2)
                    y = int((-heart_y) + self.height() / 2)
                    # 偏移量
                    draw_x = x + random.randint(-offset, offset)
                    draw_y = y + random.randint(-offset, offset)
                    # ✦外層顏色要更深
                    color_int = random.randint(1, 10)
                    if color_int == 1: #粉色
                        color = QColor(190, 43, 77)
                    elif color_int == 2:
                        color = QColor(255, 181, 198)  # 白粉
                    elif color_int == 3 or color_int == 5:
                        color = QColor(161, 25, 45)  # 深紅
                    elif color_int == 4:
                        color = QColor(232, 51, 92)
                    elif color_int == 7:
                        color = QColor(255, 0, 0)  # red
                    else:
                        color = QColor(214, 79, 100)

                    if (draw_x, draw_y, size, color) not in self.code_list_out:
                        self.code_list_out.append((draw_x, draw_y, size, color))
        # 愛心中心黑區點->為了好看彌補黑區，同上理
        for intensity_darkarea_x in range(-self.cent, self.cent):
            for intensity_darkarea_y in range(-self.cent, self.cent):
                if random.randint(1, 100) == 1:
                    size = random.randint(1, 3)
                    heart_x = intensity_darkarea_x
                    heart_y = intensity_darkarea_y
                    x = int((heart_x) + self.width() / 2)
                    y = int((-heart_y) + self.height() / 2 - 40)
                    # 偏移量
                    offset = 20
                    draw_x = x + random.randint(-offset, offset)
                    draw_y = y + random.randint(-offset, offset)
                    # 顏色配置
                    color_int = random.randint(1, 10)
                    if color_int == 1:
                        color = QColor(190, 43, 77)
                    elif color_int == 2 or color_int == 6:
                        color = QColor(255, 181, 198)  # 白粉
                    elif color_int == 3 or color_int == 5:
                        color = QColor(161, 25, 45)  # 深紅
                    elif color_int == 4:
                        color = QColor(232, 51, 92)
                    elif color_int == 7:
                        color = QColor(255, 0, 0)  # red
                    else:
                        color = QColor(214, 79, 100)
                    if (draw_x, draw_y, size, color) not in self.code_list_out:
                        self.code_list_out.append((draw_x, draw_y, size, color))

    # 刷新頁面
    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        if self.readlist >= 0:
            # 外圍點持續無規則變化刷新
            code_temporary_out = []
            offset = (9 - self.readlist) * 6
            if offset > 0:
                for code in self.code_list_out:
                    paint_x = code[0] + random.randint(-offset, offset)
                    paint_y = code[1] + random.randint(-offset, offset)
                    code_temporary_out.append((paint_x, paint_y, code[2], code[3]))
            else:
                code_temporary_out = self.code_list_out
            # main heart規律變化，更像心臟
            self.all_code_list = self.all_code_list_jump[self.readlist] + code_temporary_out
        # 遍歷所有點，出一幀畫面
        for code in self.all_code_list:
            if code[2] <= 3: #尺寸小於3比較好看
                self.pen = QPen()
                self.pen.setColor(code[3])
                self.pen.setWidth(code[2])
                self.painter.setPen(self.pen)
                self.painter.drawPoint(code[0], code[1])
            else: #尺寸若不小於3
                self.painter.setBrush(code[3])
                self.painter.drawEllipse(code[0], code[1], code[2]-1, code[2]-1)
        self.painter.end()

        # 已最大則開始縮小
        if self.readlist == 9:
            self.largen = False
        # 已最小則開始放大
        elif self.readlist == 0:
            self.largen = True

        if self.largen == True:
            self.readlist += 1 #變大1號
        elif self.largen == False:
            self.readlist -= 1 #變小1號

    # 時時刻刻刷新
    def timerEvent(self, event):
        self.update()


if __name__ == "__main__":
    # 實例化
    app = QApplication(sys.argv)
    window = Heartwindows()
    window.show()
    sys.exit(app.exec_())



