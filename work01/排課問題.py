from random import random, randint, choice
import numpy as np

courses = [
    {'teacher': '  ', 'name':'　　', 'hours': -1}, #那一節沒上課
    {'teacher': '甲', 'name':'機率', 'hours': 2},
    {'teacher': '甲', 'name':'線代', 'hours': 3},
    {'teacher': '甲', 'name':'離散', 'hours': 3},
    {'teacher': '乙', 'name':'視窗', 'hours': 3},
    {'teacher': '乙', 'name':'科學', 'hours': 3},
    {'teacher': '乙', 'name':'系統', 'hours': 3},
    {'teacher': '乙', 'name':'計概', 'hours': 3},
    {'teacher': '丙', 'name':'軟工', 'hours': 3},
    {'teacher': '丙', 'name':'行動', 'hours': 3},
    {'teacher': '丙', 'name':'網路', 'hours': 3},
    {'teacher': '丁', 'name':'媒體', 'hours': 3},
    {'teacher': '丁', 'name':'工數', 'hours': 3},
    {'teacher': '丁', 'name':'動畫', 'hours': 3},
    {'teacher': '丁', 'name':'電子', 'hours': 4},
    {'teacher': '丁', 'name':'嵌入', 'hours': 3},
    {'teacher': '戊', 'name':'網站', 'hours': 3},
    {'teacher': '戊', 'name':'網頁', 'hours': 3},
    {'teacher': '戊', 'name':'演算', 'hours': 3},
    {'teacher': '戊', 'name':'結構', 'hours': 3},
    {'teacher': '戊', 'name':'智慧', 'hours': 3}
]

teachers = ['甲', '乙', '丙', '丁', '戊']

rooms = ['A', 'B']

slots = [
    'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
    'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27',
    'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37',
    'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47',
    'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57',
    'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
    'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27',
    'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37',
    'B41', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47',
    'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57',
]

#產生索引列表
def randSlot() :
    return randint(0, len(slots)-1)
#生成隨機的時間槽索引

def randCourse() :
    return randint(0, len(courses)-1)
#生成隨機的課程索引

def neighbor(a):    # 單變數解答的鄰居函數。
                    #函數用於生成一個鄰近的解答，它隨機選擇一個時間槽，然後隨機決定是更改該時間槽的課程還是與另一個時間槽的課程交換位置
        fills = a.copy()
        choose = randint(0, 1)
        if choose == 0: # 任選一個改變 
            i = randSlot()
            fills[i] = randCourse()
        else :
            i = randSlot()
            j = randSlot()
            tmp = fills[i]
            fills[i] = fills[j]
            fills[j] = tmp
        return fills     # 建立新解答並傳回。

def height(a) :      # 高度函數
                     #函數計算了解答的高度，也就是解答的評分。它考慮了一些因素，例如連續上課是否合適、每門課的總時數是否符合要求等
        fills = a
        courseCounts = [0] * len(courses)
        score = 0
        # courseCounts.fill(0, 0, courses.length)
        for si in range(len(slots)):
            courseCounts[fills[si]] += 1
            #                        連續上課:好                   隔天:不好     跨越中午:不好
            if si < len(slots)-1 and fills[si] == fills[si+1] and si%7 != 6 and si%7 != 3:
                score += 0.1
            if si % 7 == 0 and fills[si] != 0: # 早上 8:00: 不好
                score -= 0.15
        
        for ci in range(len(courses)):
            if (courses[ci]['hours'] >= 0):
                score -= abs(courseCounts[ci] - courses[ci]['hours']) # 課程總時數不對: 不好
        return score

def str(a) :    # 將解答轉為字串，以供印出觀察。

        outs = []
        fills = a
        for i in range(len(slots)):
            c = courses[fills[i]]
            if i%7 == 0:
                outs.append('\n')
            outs.append(slots[i] + ':' + c['name'])
        return 'height={:f} {:s}\n\n'.format(height(fills), ' '.join(outs))

def init():
        fills = [0] * len(slots)
        for i in range(len(slots)):
            fills[i] = randCourse()
        return fills

def hillClimbing(x, height, neighbor, max_fail):  # 印出初始解
    fail = 0
    while True:
        nx = neighbor(x)
        if height(nx)>height(x):
            print(str(x))
            x = nx
            fail = 0
        else:
            fail += 1
            if fail > max_fail:
                return x 



# 執行爬山演算法
hillClimbing(init(), height, neighbor, max_fail=60000)
#最大失敗次數為60000演算法從一個隨機的解答開始，然後在解答空間中移動，盡可能提高解答的高度，直到連續失敗次數達到 60000 次為止