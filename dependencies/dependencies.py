import rpy2.robjects as robjects
import os
import subprocess
import sys

def main():
#    cmd = 'python ../setup.py install'
#    subprocess.call(cmd, shell=True)

#    cmd = 'wget "http://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2"'
#    subprocess.call(cmd, shell=True)

#    cmd = 'tar --bzip2 -xf boost_1_64_0.tar.bz2'
#    subprocess.call(cmd, shell=True)

#    cmd = 'cd boost_1_64_0'
#    subprocess.call(cmd, shell=True)

#    cmd = './bootstrap.sh'
#    subprocess.call(cmd, shell=True)

#    cmd = './b2 install'
#    subprocess.call(cmd, shell=True)

#    cmd = 'cd ..'
#    subprocess.call(cmd, shell=True)

#    cmd = 'sudo mv boost_1_64_0 /usr/local/'
#    subprocess.call(cmd, shell=True)
    robjects.r('''install.packages( 'multicore_0.2.tar.gz' , repos=NULL , dependencies = TRUE)''')
    robjects.r('''install.packages( 'caTools')''')
    robjects.r('''source("https://bioconductor.org/biocLite.R")''')
    robjects.r('''biocLite("BiocInstaller")''')
    robjects.r('''install.packages( 'spp.tar.gz' )''')



if __name__ == '__main__':
    main()
