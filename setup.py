# -*- coding: utf-8 -*-
import os
try: 
    from setuptools import setup 
    from setuptools import Extension 
except ImportError: 
    from distutils.core import setup 
    from distutils.extension import Extension 
import sys
sys.path.append('./src')
version = open('VERSION').read().strip()

libs = []
if os.name == 'posix':
    libs.append('m')

setup(name='colorcorrect',
      version=version,
      description="imprement some of color correction algorithms",
      long_description=open('README').read(),
      classifiers=[],
      keywords=('image-processing computer-vision'),
      author='Tomoe Magica',
      author_email='tomoe.magica@gmail.com',
      url='https://github.com/tomoemagica/colorcorrect',
      license='MIT License',
      package_dir={'': 'src'},
      packages=['colorcorrect']
)
