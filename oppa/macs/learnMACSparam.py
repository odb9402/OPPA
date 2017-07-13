"""
this module is actual fix some parameter by using
bayesian optimization. if we run this function in parallel,
we need to satisfied many condition which mentioned in the paper
named 'practical bayesian optimization in machine learning algorithm'
"""

from subprocess import call
from subprocess import Popen
import argparse
import numpy as np
import logging

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel


def learnMACSparam(args):
    """
    this function actually control learning steps. args is given by
    oppa.py ( main function of this program ) from command line.
    and make wrapper_function to use BayesianOptimization library,
    only wrapper_function`s arguments will be learned by library.

    :param args:

    :return: learned parameter.
    """

    input_file = args.input
    valid_set = args.validSet
    Qval = args.Qval
    control = args.control
    call_type = args.callType

    def wrapper_function(opt_Qval):
        error = run(input_file,valid_set,str(opt_Qval),call_type,control)
	return -error
    parameter_bound = {'opt_Qval' : (10**-16,0.8)}
    number_of_init_sample = 2

    optimizeHyper(wrapper_function, parameter_bound, number_of_init_sample)


def run(input_file, valid_set, Qval, call_type, control = None):
    """
    this function run MACS and calculate error at once.
    each arguments will be given by learnMACSparam that from command line.

    :param input_file:
        input file name.
    :param valid_set:
        name of labeled data.
    :param Qval:
        Q-value of MACS. it will be learned.
    :param control:
        control bam file in MACS. not necessary.

    :return:
        error rate of between MACS_output and labeled Data.
    """
    import MACS


    """it will be runned by protoPFC.py"""
    bam_name = input_file[:-4]  ## delete '.bam'
    reference_char = ".REF_chr"

    p1 = MACS.run(bam_name + reference_char + "1.bam", Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "2.bam", Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "3.bam", Qval ,call_type,control)
    p4 = MACS.run(bam_name + reference_char + "4.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "5.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "6.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "7.bam",  Qval ,call_type,control)
    p4 = MACS.run(bam_name + reference_char + "8.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "9.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "10.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "11.bam",  Qval ,call_type,control)
    p4 = MACS.run(bam_name + reference_char + "12.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "13.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "14.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "15.bam",  Qval ,call_type,control)
    p4 = MACS.run(bam_name + reference_char + "16.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()
    
    p1 = MACS.run(bam_name + reference_char + "17.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "18.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "19.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()

    p1 = MACS.run(bam_name + reference_char + "20.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "21.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "22.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()
    
    p1 = MACS.run(bam_name + reference_char + "M.bam",  Qval ,call_type,control)
    p2 = MACS.run(bam_name + reference_char + "X.bam",  Qval ,call_type,control)
    p3 = MACS.run(bam_name + reference_char + "Y.bam",  Qval ,call_type,control)
    p1.wait()
    p2.wait()
    p3.wait()

    #The ErrorCalculation can be also parallel by choromosome.

    #load labeled file.
    exist_test_set = True
    test_set, validation_set = loadLabel(valid_set)
    #print "# of test set is      :: " + str(len(test_set))
    #print "# of validation set is :: " + str(len(validation_set))

    #there must be valid validation set and test set.
    if not test_set or not validation_set:
        print "there are no matched validation set :p\n"
        exit()

    #actual learning part
    else:
        error_num, label_num = summerize_error(bam_name, validation_set)
       	return error_num/label_num

def summerize_error(bam_name, validation_set):
    """

    :param bam_name:
    :param validation_set:
    :return:
    """
    sum_error_num = 0
    sum_label_num = 0
    reference_char = ".REF_chr"

    for chr_no in range(22):
        input_name = bam_name + reference_char + str(chr_no+1) + ".bam_peaks" + ".broadPeak"
        error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
        sum_error_num += error_num
        sum_label_num += label_num

    # add about sexual chromosome
    input_name = bam_name + reference_char + str('X') + ".bam_peaks" + ".broadPeak"
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num
    
    input_name = bam_name + reference_char + str('Y') + ".bam_peaks" + ".broadPeak"
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num

    return sum_error_num , sum_label_num
