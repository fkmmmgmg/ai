import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from keras.utils import to_categorical
from keras.datasets import mnist

# 載入 MNIST 資料集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 將像素值標準化到 [0, 1] 範圍內
train_images = np.asarray(x_train, dtype=np.float32) / 255.0
test_images = np.asarray(x_test, dtype=np.float32) / 255.0

# 將圖像展平為一維向量
train_images = train_images.reshape(60000, 784)
test_images = test_images.reshape(10000, 784)

# 對標籤進行 one-hot 編碼
y_train = to_categorical(y_train)

# 將 NumPy 數组轉換為 PyTorch 
train_images_tensor = torch.tensor(train_images)
train_labels_tensor = torch.tensor(y_train)

test_images_tensor = torch.tensor(test_images)
test_labels_tensor = torch.tensor(y_test)

# 創 Dataset 
train_dataset = TensorDataset(train_images_tensor, train_labels_tensor)
test_dataset = TensorDataset(test_images_tensor, test_labels_tensor)

# 創 DataLoader 
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 定義神經網絡模型
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc = nn.Linear(28 * 28, 10)  # 全連接層，將28x28圖像攤平為一維向量，輸出10個類別的分數
    
    def forward(self, x):
        x = self.fc(x)
        return x

# 定義訓練函數
def train(model, train_loader, criterion, optimizer, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}")

# 定義測試函數
def test(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    print(f"Test Accuracy: {accuracy}%")

# 初始化模型、損失函數和優化器
model = SimpleNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 訓練模型
train(model, train_loader, criterion, optimizer, epochs=10)

# 測試模型
test(model, test_loader)