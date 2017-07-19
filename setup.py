import os
import sys

from setuptools import setup

def main():
      if float(sys.version[:3])<2.7 or float(sys.version[:3])>=2.8:
        sys.stderr.write("python version must be 2.7\n")
        sys.exit(1)

      setup(name='OPPA',
            version='0.1',
            description='Oppa :: Optimize Parameter in Peak'
                        ' detection Algorithm by bayesian optimization.',
            author='dong pin oh',
            author_email='dhehdqls@gmail.com',
            url='http://github.com/odb9402/OPPA',
            scripts=['oppa.py']
            author='dong pin oh',
            license='MIT',
            packages=[],
            install_requires=['scikit-learn','scipy','numpy','Cython','MACS2'],
            zip_safe=False)

if __name__ == '__main__':
      main()
