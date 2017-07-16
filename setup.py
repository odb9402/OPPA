from setuptools import setup

setup(name='OPPA',
      version='0.1',
      description='Oppa _ 오빠 :: Optimize Parameter in Peak'
                  ' detection Algorithm by bayesian optimization.',
      url='http://github.com/odb9402/OPPA',
      author='dong pin oh',
      license='MIT',
      packages=['OPPA'],
      install_requires=['scikit-learn','scipy','numpy','Cython','MACS2'],
      zip_safe=False)
