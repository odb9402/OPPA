import os
import subprocess
import sys

def main():

    curr_dir = os.getcwd()

####################### setup R language #####################################
    cmd = 'sudo apt-key --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD56CBB651716619EO84DAB9'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo add-apt-repository' 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo apt-get update'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo apt-get install r-base'
    subprocess.call(cmd, shell=True)
##############################################################################


    
####################### setup.py install #####################################
    cmd = 'sudo apt-get install python-pip'
    subprocess.call(cmd, shell=True)        
    cmd = 'sudo apt-get install python-dev'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo pip install --upgrade pip'
    subprocess.call(cmd, shell=True)
    cmd = 'python ../setup.py install'
    subprocess.call(cmd, shell=True)
    cmd = 'sudo pip install rpy2'
    subprocess.call(cmd, shell=True)
##############################################################################



####################### boost library of C++ #################################
#    cmd = 'wget "http://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2"'
#    subprocess.call(cmd, shell=True)
#    cmd = 'tar --bzip2 -xf boost_1_64_0.tar.bz2'
#    subprocess.call(cmd, shell=True)
#    cmd = '.' + curr_dir + '/boost_1_64_0/bootstrap.sh'
#    subprocess.call(cmd, shell=True)
#    cmd = '.' + curr_dir '/boost_1_64_0/b2'
#    subprocess.call(cmd, shell=True)
#    cmd = 'sudo mv boost_1_64_0 /usr/local/'
#    subprocess.call(cmd, shell=True)
##############################################################################



########################## R package install include SPP #####################
    import rpy2.robjects as robjects
    robjects.r('''install.packages( 'multicore_0.2.tar.gz' , repos=NULL , dependencies = TRUE)''')
    robjects.r('''install.packages( 'caTools')''')
    robjects.r('''install.packages( 'bitops')''')
    robjects.r('''install.packages( 'snow')''')
    robjects.r('''install.packages( 'snowfall')''')
    robjects.r('''source("https://bioconductor.org/biocLite.R")''')
    robjects.r('''biocLite("Rsamtools")''')
    robjects.r('''install.packages( 'spp_1.14.tar.gz' )''')
##############################################################################



######################### bamtools and samtools install ######################
#    cmd = 'sudo apt-get install bamtools'
#    subprocess.call(cmd, shell=True)
#    cmd = 'sudo apt-get install samtools'
#    subprocess.call(cmd, shell=True)
#    cmd = 'sudo apt-get install macs'
#    subprocess.call(cmd, shell=True)
##############################################################################


######################### install PeakSeq ####################################
    cmd = 'unzip '+ curr_dir +'/dependencies/PeakSeq_1.31.zip'
    subprocess.call(cmd, shell=True)
    cmd = 'make -C'+ curr_dir +'/dependencies/PeakSeq'
    subprocess.call(cmd, shell=True)
##############################################################################

######################### install HOMER ######################################
    cmd = 'wget http://homer.ucsd.edu/homer/configureHomer.pl'
    subprocess.call(cmd, shell=True)
    cmd = 'perl configureHomer.pl -install homer'
    subprocess.call(cmd, shell=True)
##############################################################################
if __name__ == '__main__':
    main()
