import time
from multiprocessing import cpu_count
from multiprocessing import Process
import subprocess
import os

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

def learnSPPparam(args, test_set, validation_set):
    """
    this function actually control learning steps. args is given by
    oppa.py ( main function of this program ) from command line.
    and make wrapper_function to use BayesianOptimization library,
    only wrapper_function`s arguments will be learned by library.

    :param args:
        argument from command lines

    :param test_set:
        python list of test set

    :param validation_set:
        python list of validation set

    :return: learned parameter.
    """
    input_file = args.input
    control = args.control
    call_type = args.callType

    def wrapper_function(opt_fdr):
        error = run(input_file, validation_set, str(opt_fdr), call_type, control)
        return -error

    parameter_bound = {'opt_fdr' : (10**-8,0.9)}
    number_of_init_sample = 2

    fdr = 0.01
    print run(input_file, validation_set+test_set, fdr, call_type, control)


def run(input_file, valid_set, opt_fdr, call_type, control=None):
    """
    this function run SPP and calculate error at once.
    each arguments will be given by learnSPPparam that from command line.

    :param input_file:
        input file name.
    :param valid_set:
        python list of labeled data
    :param opt_fdr:
        fdr value which will be SPP`s parameter
    :param control:
        control bam file in SPP. it is necessary.

    :return:
        error rate of between SPP_output and labeled Data.
    """
    
    curr_dir = os.getcwd()
    input_file = curr_dir + "/" + input_file
    control = curr_dir + "/" + control

    print control

    CORE_NUM = cpu_count()

    if call_type is None:
        output_name = input_file.rsplit('.',1)[0] + ".narrowPeak"
    else:
        output_name = input_file.rsplit('.',1)[0] + ".broadPeak"

    command = ['Rscript','oppa/spp/run_spp.R','-c=',input_file,'-i=',control,'-fdr=',str(opt_fdr),\
               '-savn='+ output_name,'-p='+str(CORE_NUM),'-rf']

    subprocess.call(command, shell=True)
    print "end" 
    # to Split result file of SPP by chromosome then calculate error
    command = ['./oppa/loadParser/spliter.sh ' + output_name]
    subprocess.call(command, shell=True)

    if not valid_set:
	print "there are no matched validation set :p\n"
    else:
	error_num, label_num = summerize_error(input_file.rsplit('.',1)[0], valid_set, call_type)

    if label_num is 0:
	return 0
    return (1 - error_num/label_num ) * 100


def summerize_error(bam_name, validation_set, call_type):
    sum_error_num = 0
    sum_label_num = 0
    reference_char = ".REF_chr"

    if call_type == "broad":
	print "is SPP work on broadpeak??"
	return 0, 0
    else:
	output_format_name = ".narrowPeak"

    for chr_no in range(22):
	input_name = bam_name + reference_char + str(chr_no+1) + ".narrow_peaks" + output_format_name
	error_num, label_num = calculateError(input_name , parseLabel(validation_set, input_name))
	sum_error_num += error_num
	sum_label_num += label_num

    input_name = bam_name + reference_char + 'X' + ".narrow_peaks" + output_format_name
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num
    
    input_name = bam_name + reference_char + 'Y' + ".narrow_peaks" + output_format_name
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num

    return sum_error_num, sum_label_num
