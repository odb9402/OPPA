"""
this module is actual fix some parameter by using
bayesian optimization. if we run this function in parallel,
we need to satisfied many condition which mentioned in the paper
named 'practical bayesian optimization in machine learning algorithm'
"""
import subprocess
import time
from multiprocessing import cpu_count
from multiprocessing import Process


from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel


def learnMACSparam(args, test_set, validation_set):
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

    def wrapper_narrow_cut(opt_Qval):
	correct = run(input_file, validation_set, str(opt_Qval), call_type, control)
        return correct 

    def wrapper_broad_cut(opt_Qval, opt_cutoff):
	correct = run(input_file, validation_set, str(opt_Qval), call_type, control, broad=str(opt_cutoff))
	return correct

    parameters_bounds_narrow = {'opt_Qval':(10**-15,0.8)}

    parameters_bounds_broad = {'opt_Qval':(10**-15,0.8),\
				'opt_cutoff':(10**-14,0.9)}
    number_of_init_sample = 2


    if call_type is None:
        result = optimizeHyper(wrapper_narrow_cut, parameters_bounds_narrow, number_of_init_sample)
    	subprocess.call(['macs2','callpeak','-t',input_file,'-c',control,'-g','hs','-q',str(result['max_params']['opt_Qval'])])
    	print " final error about test set is :::" + str(final_error)
    else:
	result = optimizeHyper(wrapper_broad_cut, parameters_bounds_broad, number_of_init_sample)

def run(input_file, valid_set, Qval, call_type, control = None, broad=None):
    """
    this function run MACS and calculate error at once.
    each arguments will be given by learnMACSparam that from command line.

    :param input_file:
        input file name.
    :param valid_set:
        python list of labeled data
    :param Qval:
        Q-value of MACS. it will be learned.
    :param control:
        control bam file in MACS. not necessary.

    :return:
        error rate of between MACS_output and labeled Data.
    """
    import MACS

    chromosome_list = []
    for label in valid_set:
        chromosome_list.append(label.split(':')[0])
    chromosome_list = list(set(chromosome_list))

    """it will be runned by protoPFC.py"""
    reference_char = ".REF_"
    bam_name = input_file[:-4]  ## delete '.bam'
    if control is not None:
        cr_bam_name = control[:-4]
    
    MAX_CORE = cpu_count()
    TASKS = len(chromosome_list)
    TASK_NO = 0
    macs_processes = []

    while (len(macs_processes) < MAX_CORE-1) and (TASK_NO < TASKS):
	if control is not None:
	    macs_processes.append(MACS.run(bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", Qval, call_type, cr_bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", broad))
	else:
	    macs_processes.append(MACS.run(bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", Qval, call_type, broad=broad))
	    
	TASK_NO += 1

    while len(macs_processes) > 0:
	time.sleep(0.1)
	
	for proc in reversed(range(len(macs_processes))):
	    if macs_processes[proc].poll() is not None:
		del macs_processes[proc]

	while (len(macs_processes) < MAX_CORE - 1) and (TASK_NO < TASKS):
	    if control is not None:
	        macs_processes.append(MACS.run(bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", Qval, call_type, cr_bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", broad))
	    else:
		macs_processes.append(MACS.run(bam_name + reference_char + chromosome_list[TASK_NO] + ".bam", Qval, call_type, broad=broad))
	    TASK_NO += 1

    #there must be valid validation set and test set.
    if not valid_set:
        print "there are no matched validation set :p\n"
        exit()

    #actual learning part
    else:
        error_num, label_num = summerize_error(bam_name, valid_set, call_type)

    if label_num is 0:
	return 1.0
    return (1 - error_num/label_num) * 100


def summerize_error(bam_name, validation_set, call_type):
    """

    :param bam_name:
    :param validation_set:
    :return:
    """
    sum_error_num = 0
    sum_label_num = 0
    reference_char = ".REF_chr"
    if call_type == "broad":
		output_format_name = '.broadPeak'
    else:
		output_format_name = '.narrowPeak'

    for chr_no in range(22):
        input_name = bam_name + reference_char + str(chr_no+1) + ".bam_peaks" + output_format_name
        error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
        sum_error_num += error_num
        sum_label_num += label_num

    # add about sexual chromosome
    input_name = bam_name + reference_char + 'X' + ".bam_peaks" + output_format_name
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num
    
    input_name = bam_name + reference_char + 'Y' + ".bam_peaks" + output_format_name
    error_num, label_num = calculateError(input_name, parseLabel(validation_set, input_name))
    sum_error_num += error_num
    sum_label_num += label_num

    return sum_error_num , sum_label_num


def is_exist_chr(valid_set, chr):
    """
    this method to decide either run MACS or not about
    each chromosome in label data. if some chromosome did not
    included by label data, there is no need to run MACS that
    chromosome.

    :param valid_set:
        validation set before parse to python maps. it just list
        of each line in file like a
        ['chrN:0000-1132 peakStart bcell monocyte' , ... ]

    :param chr:
        input chromosome.

    :return:
        T/F about some chromosome exist in label.
    """
    
    for label in valid_set:
        if chr in label:
            return True
    return False
