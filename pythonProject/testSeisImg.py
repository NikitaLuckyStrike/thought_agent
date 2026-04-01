import cv2                    # библиотека для загрузки и обработки изображений
import matplotlib.pyplot as plt  # для отображения
import numpy as np              # для работы с матрицами
import os                       # для работы с файлами
import torch
import torch.nn as nn



images = []

for file in os.listdir(r"C:\Users\sabrahar\Desktop\ML\seismic pictures"):
    img = cv2.imread(os.path.join(r"C:\Users\sabrahar\Desktop\ML\seismic pictures", file), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (512, 512))
    img = img/255
    
    images.append(img)
    
    # выводим изображение
    # plt.imshow(img)
    # plt.show()

# Определяем простую сверточную нейросеть
class SimpleSegNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),  # первый слой
            nn.ReLU(),                                  # активация
            nn.Conv2d(8, 16, kernel_size=3, padding=1), # второй слой
            nn.ReLU(),
            nn.Conv2d(16, 1, kernel_size=3, padding=1), # выходной слой
            nn.Sigmoid()                                # чтобы получить значения от 0 до 1
        )

    def forward(self, x):
        return self.model(x)

model = SimpleSegNet()
for img in images:
    # Преобразуем в формат [1, 1, 512, 512]
    img_tensor = torch.from_numpy(img).float().unsqueeze(0).unsqueeze(0)
    print(img_tensor.shape)
    # exit(0)


    # Без обучения — просто пускаем данные вперёд
    with torch.no_grad():  # отключаем обучение (градиенты)
        output = model(img_tensor)  # результат — [1, 1, 512, 512]
        pred_mask = output.squeeze().numpy()  # убираем лишние измерения

    plt.imshow(pred_mask, cmap='hot')
    plt.title("AI-предсказание (псевдо)")
    plt.axis("off")
    plt.show()
