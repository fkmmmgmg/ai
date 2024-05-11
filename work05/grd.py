import numpy as np
from micrograd.engine import Value

def gradientDescendent(f, p, lr=0.01, epsilon=1e-5, max_iters=1000):
    for i in range(max_iters):
        # 将参数转换为 Value 对象
        x, y, z = [Value(pi) for pi in p]
        
        # 计算函数值
        value = f([x, y, z])
        
        # 使用反向传播计算梯度
        value.backward()
        
        # 获取梯度并进行更新
        grad_x, grad_y, grad_z = x.grad, y.grad, z.grad
        p = [p[0] - lr * grad_x, p[1] - lr * grad_y, p[2] - lr * grad_z]
        
        # 检查收敛条件
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



