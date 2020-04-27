from __future__ import division
import numpy as np
from six.moves import range
from six.moves import xrange
from PIL import Image
import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil
from colorcorrect.algorithm import automatic_color_equalization
from shutil import move
import os
from os import path
import sys
from pathlib import Path, PureWindowsPath
import fnmatch

'''
INTERNAL = os.environ['INTERNAL']
WORKSPACE = os.environ['WORKSPACE']
'''
target_dir = os.getcwd()
target_dir = os.path.join(target_dir, 'data_dst')

file_count = len(fnmatch.filter(os.listdir(target_dir), "*.png"))

print("Checking " + str(file_count) + " files")

colcor_path = os.path.join(target_dir, 'colcor')

if not path.isdir(colcor_path):
   try:
       os.mkdir(colcor_path)
   except OSError:
       print("Creation of the directory %s failed" % colcor_path)
   else:
       print("Successfully created the directory %s " % colcor_path)

Iter = 0

print("Executing...")

for thisFile in os.listdir(target_dir):
    file_name = os.path.join(target_dir, thisFile)
    if os.path.isfile(file_name):
        file_name = os.path.join(target_dir, thisFile)

        Iter += 1
        print("\r" + str(Iter) + '/' + str(file_count), end='')

        img = Image.open(file_name)
        img = to_pil(automatic_color_equalization(from_pil(img)))
        basename = os.path.basename(file_name)
        abs_filename = colcor_path +  '/' + basename
        img.save(abs_filename)

print("\nDone.")
