import numpy as np
from micrograd.engine import Value

def gradientDescendent(f, p, lr=0.01, epsilon=1e-5, max_iters=1000):
    for i in range(max_iters):
        # 將參數轉換為 Value 對象
        x, y, z = [Value(pi) for pi in p]
        
        # 計算函數值
        value = f([x, y, z])
        
        # 使用反向傳播計算梯度
        value.backward()
        
        # 取得梯度並進行更新
        grad_x, grad_y, grad_z = x.grad, y.grad, z.grad
        p = [p[0] - lr * grad_x, p[1] - lr * grad_y, p[2] - lr * grad_z]
        
        # 檢查收斂條件
        if np.linalg.norm([grad_x, grad_y, grad_z]) < epsilon:
            break
    
    return p, value.data

def f(p):
    [x, y, z] = p
    return (x-1)**2 + (y-2)**2 + (z-3)**2

p = [0.0, 0.0, 0.0]
result, min_value = gradientDescendent(f, p)
print("Minimum point:", result)
print("Minimum value:", min_value)

#gradientDescendent(f, p, lr=0.01, epsilon=1e-5, max_iters=1000) 是梯度下降的主要函數。
#f 是我們要最小化的目標函數。
#p 是初始參數值。
#lr 是學習率（learning rate），控制每次更新參數的步長。
#epsilon 是收斂條件，如果梯度的範數小於 epsilon，則認為已經收斂。
#max_iters 是最多迭代次數，如果在達到最大迭代次數之前沒有收斂，就停止迭代。



