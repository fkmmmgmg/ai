from scipy.optimize import linprog

def linear_programming_3d():
    c = [3, 2, 5]  # 目標函數的係數：3x + 2y + 5z

    # 不等式約束的係數矩陣 A_ub 和右側值 b_ub
    A_ub = [[-1, 0, 0],  # x >= 0
            [0, -1, 0],  # y >= 0
            [0, 0, -1],  # z >= 0
            [1, 1, 0],   # x + y <= 10
            [2, 0, 1],   # 2x + z <= 9
            [0, 1, 2]]   # y + 2z <= 11
    b_ub = [0, 0, 0, 10, 9, 11]

    # 變量界限
    bounds = [(0, None), (0, None), (0, None)]  # x, y, z 都大於等於 0

    # 使用線性規劃函數求解
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

    # 打印結果
    print("Optimal value:", res.fun)
    print("Optimal solution (x, y, z):", res.x)

# 執行演算法
linear_programming_3d()