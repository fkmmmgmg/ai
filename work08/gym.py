import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)
score = 0
ans = [] #存分數用的


for _ in range(100):
    env.render()
    
            
    angle = observation[2]  # 轉角度
    
    # 根據角度決定
    if angle < -0.05:  # 如果杆子向左傾斜超過預直
        action = 1  # 向右移
    elif angle > 0.05:  # 如果杆子向右傾斜超過預直
        action = 0  # 向左移
    else:  # 隨機動作
        action = env.action_space.sample()
    
    
    observation, reward, terminated, truncated, info = env.step(action)
    score += reward
    
    print('observation=', observation)
    
    if terminated or truncated: # 這裡要加入程式，紀錄你每次撐多久
        with open('Readme.md', 'a+') as file:
            file.write(f'scores: {score}\n')
        ans.append(score)
        observation, info = env.reset()
        print(f'dead,score:{score}')
        score=0
        
if ans:
    with open('Readme.md', 'a+') as file:
        file.write(f'max: {max(ans)}\n')
        file.write(f'min: {min(ans)}\n')
        file.write(f'avg: {sum(ans)/len(ans)}\n')

env.close()
