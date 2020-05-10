# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np


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

