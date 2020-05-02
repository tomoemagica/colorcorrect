# -*- coding: utf-8 -*-
from __future__ import division
# import numpy as np
import cupy as np
import ctypes.util
import ctypes
from ctypes import POINTER
from ctypes import pointer
from ctypes import Structure
from ctypes import c_ubyte
from ctypes import c_int
from ctypes import c_double
from ctypes import c_void_p
from ctypes import *
from six.moves import range
from six.moves import xrange
import cv2

import os
cutilfolder = os.path.abspath(__file__).rsplit(os.path.sep, 1)[0]
cutilname = "cutil"
libcutil = np.ctypeslib.load_library(cutilname, cutilfolder)


class RGBImage(Structure):
    _fields_ = [
        ("width", c_int),
        ("height", c_int),
        ("r", POINTER(c_ubyte)),
        ("g", POINTER(c_ubyte)),
        ("b", POINTER(c_ubyte)),
    ]


libcutil.calc_ace.argtypes = [POINTER(RGBImage), c_int, c_double, c_double]


def stretch_pre(nimg):
    """
    from 'Applicability Of White-Balancing Algorithms to Restoring Faded Colour Slides: An Empirical Evaluation'
    """
    nimg = nimg.transpose(2, 0, 1)
    nimg[0] = np.maximum(nimg[0] - nimg[0].min(), 0)
    nimg[1] = np.maximum(nimg[1] - nimg[1].min(), 0)
    nimg[2] = np.maximum(nimg[2] - nimg[2].min(), 0)
    return nimg.transpose(1, 2, 0)


def gray_world(nimg):
    nimg = nimg.transpose(2, 0, 1).astype(np.uint32)
    mu_g = np.average(nimg[1])
    nimg[0] = np.minimum(nimg[0] * (mu_g / np.average(nimg[0])), 255)
    nimg[2] = np.minimum(nimg[2] * (mu_g / np.average(nimg[2])), 255)
    return nimg.transpose(1, 2, 0).astype(np.uint8)


def max_white(nimg):
    if nimg.dtype == np.uint8:
        brightest = float(2 ** 8)
    elif nimg.dtype == np.uint16:
        brightest = float(2 ** 16)
    elif nimg.dtype == np.uint32:
        brightest = float(2 ** 32)
    else:
        brightest = float(2 ** 8)
    nimg = nimg.transpose(2, 0, 1)
    nimg = nimg.astype(np.int32)
    nimg[0] = np.minimum(nimg[0] * (brightest / float(nimg[0].max())), 255)
    nimg[1] = np.minimum(nimg[1] * (brightest / float(nimg[1].max())), 255)
    nimg[2] = np.minimum(nimg[2] * (brightest / float(nimg[2].max())), 255)
    return nimg.transpose(1, 2, 0).astype(np.uint8)


def stretch(nimg):
    return max_white(stretch_pre(nimg))


def automatic_color_equalization(nimg, slope=10, limit=1000, samples=500):
    """
    A. Rizzi, C. Gatta and D. Marini, "A new algorithm for unsupervised global and local color correction.",
    Pattern Recognition Letters, vol. 24, no. 11, 2003.
    """
    nimg = nimg.transpose(2, 0, 1)
    nimg = np.ascontiguousarray(nimg, dtype=np.uint8)
    img = RGBImage(nimg.shape[2],
                   nimg.shape[1],
                   nimg[0].ctypes.data_as(POINTER(c_ubyte)),
                   nimg[1].ctypes.data_as(POINTER(c_ubyte)),
                   nimg[2].ctypes.data_as(POINTER(c_ubyte)))
    libcutil.calc_ace(pointer(img), samples, slope, limit)
    return nimg.transpose(1, 2, 0)


def clahe(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    nimg = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return nimg


def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result
