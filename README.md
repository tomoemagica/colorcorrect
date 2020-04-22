# colorcorrect
 colorcorrect

## requires

numpy

Pillow

six

## install

mkdir build

cd build

C:\Program Files\Python-3.7.6\colorcorrect>"C:\Program Files\Cmake\bin\cmake" -G "Visual Studio 16 2019" -T host=x64 -DCMAKE_INSTALL_PREFIX="C:\Program Files\Python-3.7.6\colorcorrect" ..

cd ..

python setup.py sdist

py setup.py build

py setup.py install
