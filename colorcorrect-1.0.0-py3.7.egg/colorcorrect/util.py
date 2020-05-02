# -*- coding: utf-8 -*-
# import numpy as np
import cupy as np
from PIL import Image
import cv2


def from_pil(pimg):
    pimg = pimg.convert(mode='RGB')
    nimg = np.array(pimg)
    return nimg


def to_pil(nimg):
    return Image.fromarray(np.uint8(nimg))


def pil2cv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # gray
        pass
    elif new_image.shape[2] == 3:  # color
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # alpha
        new_image = new_image[:, :, [2, 1, 0, 3]]
    return new_image


def cv2pil(image):
    new_image = image.copy()
    if new_image.ndim == 2:  # gray
        pass
    elif new_image.shape[2] == 3:  # color
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # alpha
        new_image = new_image[:, :, [2, 1, 0, 3]]
    new_image = Image.fromarray(new_image)
    return new_image

