import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import os
import sys
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')))
from server.modules.network import Net

DIM: int = 28

class DigitClassifier:
    _mean: float = 33.318421449829934
    _scale: float = 78.56749083061408
    _model: Net

    def __init__(self, from_row_data=False):
        if from_row_data:
            trainset = torchvision.datasets.MNIST(
                root='./data',
                train=True,
                download=True,
                transform=None
                )
            train_data = torch.tensor(trainset.data.clone().detach().numpy(), dtype=torch.float64)
            self._mean = float(torch.mean(train_data))
            self._scale = float(torch.std(train_data))
            print(self._mean, self._scale)
        self._model = Net()
        self._model.load_state_dict(torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pth')))
        self._model.eval()
        self._softmax = nn.Softmax()

    def predict(self, x: np.ndarray) -> int:
        """
        :param: x np.ndarray shape=(28, 28)
        :return int
        """
        x = self._normalize(x)
        x = x.reshape((1, 1, DIM, DIM))
        x = torch.from_numpy(x).float()
        y = self._softmax(self._model(x))
        return int(torch.argmax(y))

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        x_ = ((x - self._mean) / self._scale) * np.sqrt(0.5) + 0.5
        return x_


class ImageProcessor:
    _img: np.ndarray

    def __init__(self, gray_x: np.ndarray, width: int, height: int):
        """
        :param gray_x: np.ndarray shape=(n, )
        :param width: int
        :param height: int
        """
        from matplotlib import pyplot as plt
        rgb_x = np.stack([gray_x, gray_x, gray_x], 0).T.reshape((width, height, 3)).astype(np.uint8)
        print(rgb_x.shape)
        img = cv2.cvtColor(rgb_x, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (DIM, DIM))
        self._img = img
        cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample.jpg'), self._img)

    def to_gray_scale(self) -> np.ndarray:
        return self._img[:, :, 0]


class ParameterParser:

    @classmethod
    def to_numpy(cls, str_arr: str) -> np.ndarray:
        """
        :param str_arr: ex) '[0, 1, 2, 3]'
        :return np.ndarray ex) [0, 1, 2, 3]
        """
        return np.array(list(map(int, str_arr.replace('[', '').replace(']', '').split(','))))


if __name__ == "__main__":
    b = np.ones(32 * 32) * 255
    a = ImageProcessor(b, 32, 32)
