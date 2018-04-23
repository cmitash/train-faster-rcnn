# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""

__sets = {}

import datasets.APC
import datasets.LINEMOD

import numpy as np

imageset = 'LINEMOD'
devkit = '/media/chaitanya/DATADRIVE0/datasets/rcnn_training/LINEMOD'

def get_imdb(name):
    """Get an imdb (image database) by name."""
    __sets['APC'] = (lambda imageset = 'APC', devkit = devkit: datasets.APC(imageset,'/media/chaitanya/DATADRIVE0/datasets/rcnn_training/APC'))
    __sets['LINEMOD'] = (lambda imageset = 'LINEMOD', devkit = devkit: datasets.LINEMOD(imageset,'/media/chaitanya/DATADRIVE0/datasets/rcnn_training/LINEMOD'))
    if not __sets.has_key(name):
        raise KeyError('Unknown dataset: {}'.format(name))
    return __sets[name]()

def list_imdbs():
    """List all registered imdbs."""
    return __sets.keys()
