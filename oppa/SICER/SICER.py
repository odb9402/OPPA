import os
import subprocess


"""
    The order of command line parameters in SICER ::

$ sh DIR/SICER.sh ["InputDir"] ["bed file"] ["control file"] ["OutputDir"] ["Species"] 
["redundancy threshold"] ["window size (bp)"] ["fragment size"]
["effective genome fraction"] ["gap size (bp)"] ["FDR"]



    meaningful parameters in SICER ::

REDTHRESH  : -rt
    number of copies of identical reads allowed in a library.
    In this case we don`t care about this

WINDOWSIZE : - w'
    resolution of SICER algorithm.

Fragment size :
    It is for determination of the amount of shift from the beginning of a
    read to the center of the DNA fragment represented by read.

Effective genome fraction :
    Effective Genome

GAPSIZE : -g
    It needs to be multiples of window size.
    For example, if WINDOWSIZE is 170, GAPSIZE must be
    {170, 340, 510, ... , n*170}
    
"""

def run(input_file, control_file, windowSize, fragSize, gapSize):
    """

    :param input_file:
    :param control_file:
    :param fdr:
    :return:
    """

    spliter = input_file.rsplit('/',1)
    working_dir = spliter[0] + '/SICER/' +spliter[1].rsplit('.',2)[1].rsplit('_')[1]
    output_file_name = spliter[0] + '/SICER/' + spliter[1][:-3] + 'bam_peaks.bed'

    commands = ['python ' + os.getcwd() + '/dependencies/SICERpy/SICERpy/SICER.py -t ' + input_file\
                + ' -c ' + control_file + ' -w ' + windowSize + ' -fs ' + fragSize \
                + ' -g ' + str(int(gapSize)) + ' -rt 0 > ' + output_file_name]

    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(commands, shell= True, cwd=working_dir, stdout=FNULL, stderr=subprocess.STDOUT)
    process.wait()


    return process