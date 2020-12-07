from __future__ import annotations
from typing import List, Dict
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import os
import sys
import cv2
import base64
from io import BytesIO
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
from modules.network import Net

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
    MARGIN: int = 5
    _img: np.ndarray

    def __init__(self, gray_x: np.ndarray, width: int, height: int):
        """
        :param gray_x: np.ndarray shape=(n, )
        :param width: int
        :param height: int
        """
        rgb_x = np.stack([gray_x, gray_x, gray_x], 0).T.reshape((width, height, 3)).astype(np.uint8)
        img = cv2.cvtColor(rgb_x, cv2.COLOR_RGB2BGR)
        self._img = img

    def divide_to_digit(self) -> List[Dict[str, int, int, np.ndarray]]:
        """
        :return [{
            raw digit array as string,
            raw digit's width,
            raw digit's height,
            input array to fed into the model
            }]
        """
        data = list()
        for raw_dig in self._labeling():
            pil_img = Image.fromarray(raw_dig)
            buff = BytesIO()
            pil_img.save(buff, format="JPEG")
            new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
            data.append({
                # 'raw_digit': ','.join(list(map(str, raw_dig.flatten()))),
                'raw_digit': new_image_string,
                'width': raw_dig.shape[0],
                'height': raw_dig.shape[1],
                'input': cv2.resize(raw_dig, (DIM, DIM))
            })
        return data

    def _labeling(self):
        _, bin_img = cv2.threshold(self._img, 128, 255, cv2.THRESH_BINARY)
        _, _, data, _ = cv2.connectedComponentsWithStats(bin_img[:, :, 0])

        img_list = list()
        for (x, y, w, h, _) in sorted(data[1:], key=lambda x: x[0]):
            img_i = self._to_square(x=self._img[:, :, 0][y:y+h, x:x+w])
            img_list.append(img_i)
        return img_list

    def _to_square(self, x: np.ndarray):
        h, w = x.shape
        if h > w:
            square_x = np.zeros((h + self.MARGIN * 2, h + self.MARGIN * 2))
            margin = (h - w) // 2
            square_x[self.MARGIN : self.MARGIN + h, self.MARGIN + margin : margin + self.MARGIN + w] = x
        elif h <= w:
            square_x = np.zeros((w + self.MARGIN * 2, w + self.MARGIN * 2))
            margin = (w - h) // 2
            square_x[self.MARGIN + margin:self.MARGIN + margin + h, self.MARGIN:self.MARGIN + w] = x
        return cv2.resize(square_x, (100, 100)).astype(np.uint8)

    @classmethod
    def _to_gray_scale(self, x: np.ndarray) -> np.ndarray:
        return x[:, :, 0]


class ParameterParser:

    @classmethod
    def to_numpy(cls, str_arr: str) -> np.ndarray:
        """
        :param str_arr: ex) '[0, 1, 2, 3]'
        :return np.ndarray ex) [0, 1, 2, 3]
        """
        return np.array(list(map(int, str_arr.replace('[', '').replace(']', '').split(','))))
