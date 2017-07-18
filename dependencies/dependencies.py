import os
import subprocess
import sys

def main():
    cmd = 'python ../setup.py install'
    subprocess.call(cmd, shell=True)

    cmd = 'wget "http://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2"'
    subprocess.call(cmd, shell=True)

    cmd = 'tar --bzip2 -xf boost_1_64_0.tar.bz2'
    subprocess.call(cmd, shell=True)

    cmd = './boost_1_64_0/bootstrap.sh'
    subprocess.call(cmd, shell=True)

    cmd = './boost_1_64_0/b2 install'
    subprocess.call(cmd, shell=True)

    cmd = 'R CMD INSTALL multicore_0.2.tar.gz'
    subprocess.call(cmd, shell=True)

    cmd = 'R CMD INSTALL spp_2.0.1.tar.gz'
    subprocess.call(cmd, shell=True)






if __name__ == '__main__':
    main()
