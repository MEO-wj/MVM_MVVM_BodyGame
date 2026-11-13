"""
Created by Taizhou CHEN
Shantou University 
tzchen@stu.edu.cn

"""

from torch.utils.data import Dataset
import glob
import os
from segment import segment
import cv2
import numpy as np

class CustomDataset(Dataset):
    def __init__(self, path):
        super().__init__()

        self.path = path
        self.dir = [] # 储存所有图片的路径
        self.labels = [] # 依次储存所有图片的标签

        self.loadDataPath()

    def __len__(self):
        return len(self.dir)

    def __getitem__(self, index):
        """返回第index个数据和对应的标签

        """
        next_img = cv2.imread(self.dir[index]) # 读取图片数据

        mask = segment(next_img) # 提取特征遮罩
        mask = cv2.resize(mask, (128, 128), interpolation=cv2.INTER_AREA) # 缩放到128 x 128的分辨率
        mask = mask.astype(np.float32) / 255 # 归一化

        mask = np.expand_dims(mask, 0)

        next_label = self.labels[index] # 获取对应的标签

        return mask, next_label # 返回数据和标签

    def loadDataPath(self):
        """.../datset/**/*.jpg
        """
        self.dir = glob.glob(
            os.path.join(
                os.path.join(self.path, "**"), "*.jpg"
                )            
            )

        self.labels = [int(path.split(os.path.sep)[-2]) for path in self.dir]

if __name__ == "__main__":
    dataset = CustomDataset("dataset")
    next_img, label = dataset.__getitem__(0)

    print("label: ", label)
    cv2.imshow("img", next_img)
    cv2.waitKey(0)