# -*- coding: utf-8 -*-
import os
from distutils.core import setup, Extension
import sys
sys.path.append('./src')
version = open('VERSION').read().strip()

libs = []
if os.name == 'posix':
    libs.append('m')

module1 = Extension('colorcorrect._cutil',
                    include_dirs=['cutil'],
                    libraries=libs,
                    sources = ['cutil/cutil.cpp'])

setup(name='colorcorrect',
      version=version,
      description="imprement some of color correction algorithms",
      long_description=open('README').read(),
      classifiers=[],
      keywords=('image-processing computer-vision'),
      install_requires=["numpy", "Pillow", "six"],
      author='Tomoe Magica',
      author_email='tomoe.magica@gmail.com',
      url='https://github.com/tomoemagica/colorcorrect',
      license='MIT License',
      package_dir={'': 'src'},
      packages=['colorcorrect'],
      ext_modules = [module1])
#         extra_compile_args=[],
#         Extension(
#             'colorcorrect._cutil', [
#                 'cutil/cutil.cpp',
#             ],
#         ),
#     ],
#     )
