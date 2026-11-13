"""
Created by Taizhou CHEN
Shantou University 
tzchen@stu.edu.cn

"""

import torch
from torch import nn

class GestureClassifier(nn.Sequential):
    def __init__(self):
        super().__init__()

        self.body = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),

            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),

            nn.Flatten(),
            nn.Linear(128 * 2 * 2, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.ReLU(),
            nn.Linear(2048, 3)
        )
    def forward(self, x):
        for i, layer in enumerate(self.body):
            x = layer(x)
            # print(f"{layer.__class__.__name__:} {x.shape}")
        return x

if __name__ == "__main__":
    model = GestureClassifier()

    fake_input = torch.randn(1, 1, 128, 128)
    print(model(fake_input).shape)