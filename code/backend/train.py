"""
Created by Taizhou CHEN
Shantou University 
tzchen@stu.edu.cn

训练：
uv run train.py -data_path [训练数据集路径] 

测试：
uv run train.py -data_path [测试数据集路径] -model_path [.pth文件储存路径] -test

"""

import argparse
from dataset import CustomDataset

from torch.utils.data import random_split, DataLoader

import torch
from classifier import GestureClassifier
from tqdm import tqdm

def get_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-data_path", 
                        dest="data_path",
                        default="dataset",
                        type=str,
                        help="Path to the training data")
    parser.add_argument("-lr", 
                        dest="lr",
                        default=1e-4,
                        type=float,
                        help="Learning rate for the training process")
    parser.add_argument("-bs", 
                        dest="bs",
                        default=16,
                        type=int,
                        help="Batch size")
    parser.add_argument("-epoch", 
                        dest="epoch",
                        default=10,
                        type=int,
                        help="Number of epoch")
    parser.add_argument("-test", 
                        dest="test",
                        default=False,
                        action='store_true',
                        help="Enable testing mode")
    parser.add_argument("-model_path", 
                        dest="model_path",
                        default="model.pth",
                        type=str,
                        help="The model file to save or load")

    return parser.parse_args()

def train(train_dataloader, val_dataloader, device, args):

    model = GestureClassifier().to(device)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.lr)

    loss_fn = torch.nn.CrossEntropyLoss()
    for epoch in range(args.epoch):
        print(f"Epoch {epoch+1}/{args.epoch}...")

        train_loss_sum = 0

        for batch_idx, (X, y) in tqdm(enumerate(train_dataloader), 
                                      total=len(train_dataloader)):
            X, y = X.to(device), y.to(device)

            # forward
            pred = model(X)
            loss = loss_fn(pred, y)

            # backward
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            train_loss_sum += loss.item() / len(train_dataloader)

        print(f"Loss: {train_loss_sum}")
        print(f"Accuracy on training set: {check_accuracy(train_dataloader, model=model, device=device)}")
        print(f"Accuracy on validation set: {check_accuracy(val_dataloader, model=model, device=device)}")

    return model
        
def check_accuracy(data_loader, model, device):
    num_correct = 0
    num_sample = 0
    model.eval()
    with torch.no_grad():
        for _, (X, y) in enumerate(data_loader):
            X, y = X.to(device), y.to(device)

            # forward
            pred = model(X)
            y_hat = torch.argmax(pred, dim=1)

            # y_hat =   [1, 1, 0, 0, 1]
            # y =       [0, 1, 1, 0, 1]
            num_correct += (y_hat == y).sum()
            num_sample += pred.shape[0]

    return float(num_correct) / float(num_sample)

if __name__ == "__main__":
    args = get_args_parser()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

    # 先直接读取数据集
    dataset = CustomDataset(path=args.data_path)

    # 判断是否进行测试
    # args.test这个值我们设置为store_true，只要在参数里面带上 -test 就会被赋值为True
    if args.test:
        # 若进行测试，直接在读取的数据集上构建DataLoader
        dataloader = DataLoader(
            dataset=dataset,
            batch_size=args.bs,
            shuffle=True
        )
        # 读取模型文件
        model = torch.load("model.pth", weights_only=False).to(device)
        print("Testing...")
        print(f"Accuracy on testing set: {check_accuracy(data_loader=dataloader, model=model, device=device)}")

    else:
        # 若不是进行测试，分割数据集再分别构建DataLoader准备训练和验证
        train_dataset, val_dataset = random_split(dataset, 
            [int(len(dataset) * 0.8), len(dataset) - int(len(dataset) * 0.8)]
            )

        train_dataloader = DataLoader(
            dataset=train_dataset,
            batch_size=args.bs,
            shuffle=True
        )
        val_dataloader = DataLoader(
            dataset=val_dataset,
            batch_size=args.bs,
            shuffle=True
        )

        model = train(train_dataloader, val_dataloader, device, args)

        torch.save(model, args.model_path)
        print(f"Model saved to {args.model_path}")