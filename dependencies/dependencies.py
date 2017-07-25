import rpy2.robjects as robjects
import os
import subprocess
import sys

def main():
    
####################### setup.py install ######################################
    cmd = 'sudo apt-get install python-dev'
    subprocess.call(cmd, shell=True)
    cmd = 'python ../setup.py install'
    subprocess.call(cmd, shell=True)
    cmd = 'pip install rpy2'
    subprocess.call(cmd, shell=True)
################################################################################



####################### boost library of C++ ##############################
    cmd = 'wget "http://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2"'
    subprocess.call(cmd, shell=True)
    cmd = 'tar --bzip2 -xf boost_1_64_0.tar.bz2'
    subprocess.call(cmd, shell=True)
    cmd = 'cd boost_1_64_0'
    subprocess.call(cmd, shell=True)
    cmd = './bootstrap.sh'
    subprocess.call(cmd, shell=True)
    cmd = './b2 install'
    subprocess.call(cmd, shell=True)
    cmd = 'cd ..'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo mv boost_1_64_0 /usr/local/'
    subprocess.call(cmd, shell=True)
###############################################################################



########################## R package install include SPP ###########################
    robjects.r('''install.packages( 'multicore_0.2.tar.gz' , repos=NULL , dependencies = TRUE)''')
    robjects.r('''install.packages( 'caTools')''')
    robjects.r('''install.packages( 'bitops')''')
    robjects.r('''install.packages( 'snow')''')
    robjects.r('''install.packages( 'snowfall')''')
    robjects.r('''source("https://bioconductor.org/biocLite.R")''')
    robjects.r('''biocLite("Rsamtools",suppressUpdata=TRUE)''')
    robjects.r('''install.packages( 'oppa/spp/spp_1.14.tar.gz' )''')
#####################################################################################



################################## bamtools and samtools install ######################
    cmd = 'sudo apt-get install bamtools'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo apt-get install samtools'
    subprocess.call(cmd, shell=True)
#####################################################################################


if __name__ == '__main__':
    main()
