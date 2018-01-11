from math import exp
import glob
import os
import re
from multiprocessing import cpu_count, Process , Manager
import multiprocessing

from ..Helper.tools import parallel_learning
from ..Helper.tools import return_accuracy
from ..Helper.tools import extract_chr_cpNum
from ..optimizeHyper import run as optimizeHyper

from ..calculateError import run as calculateError
from ..loadParser.parseLabel import run as parseLabel


def learnMACSparam(args, test_set, validation_set, PATH, kry_file=None, call_type=None):
	"""
    This function actually control learning steps. args is given by
    OPPA1 ( main function of this program ) from command line.
    And make wrapper_function to use BayesianOptimization library,
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
	control_file = args.control
	chromosome_list = []
	cpNum_files = []
	cpNum_controls = []

	# result value about bayesian optimization
	manager = Manager()
	return_dict = manager.dict()	

	if not os.path.exists(PATH + '/MACS'):
		os.makedirs(PATH + '/MACS')

	if call_type == "broad":
		parameters_bounds = {'opt_Qval':(10**-8,30.0),\
				'opt_cutoff':(10**-7,35.0)}
	else:
		parameters_bounds = {'opt_Qval':(10**-8,30.0)}
	
	number_of_init_sample = 3

	chromosome_list, cpNum_controls, cpNum_files = extract_chr_cpNum(chromosome_list, input_file, control_file,
																	 cpNum_controls, cpNum_files, kry_file, test_set,
																	 validation_set, PATH, tool_name='MACS')

	reference_char = ".REF_"
	bam_name = input_file[:-4]  ## delete '.bam'
	cr_bam_name = control_file[:-4]

	MAX_CORE = cpu_count()
	learning_processes = []

	################################################################################
	if kry_file is None:
		for chromosome in chromosome_list:
			if call_type == "broad":
				# create wrapper function about broad peak calling
				def wrapper_function_broad(opt_Qval, opt_cutoff):
					target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
					accuracy = run(target, validation_set + test_set, str(exp(opt_Qval/100)-1),\
							call_type, PATH, control_file, str(exp(opt_cutoff/100)-1), False, kry_file,)
					print chromosome,\
						"Qval :" + str(round(exp(opt_Qval/100)-1,4)),\
						"Broad-cutoff:" + str(round(exp(opt_cutoff/100)-1,4)),\
						"score:" + str(round(accuracy,4)) + '\n'
					return accuracy
				# set function will be input of bayesian optimization
				function = wrapper_function_broad

			else:
				# create wrapper function about narrow peak calling
				def wrapper_function_narrow(opt_Qval):
					target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
					accuracy = run(target, validation_set + test_set, str(exp(opt_Qval/100)-1)\
							, call_type, PATH, control_file, None, False, kry_file,)
					print chromosome,\
						"Qval :" + str(round(exp(opt_Qval/100)-1,4)),\
						"score:" + str(round(accuracy,4)) + '\n'
					return accuracy
				# set function will be input of bayesian optimization
				function = wrapper_function_narrow
			
			# each learning_process and wrapper function will be child process of OPPA
			if call_type == "broad":
				learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
						parameters_bounds, number_of_init_sample, return_dict, 13, 'ei', chromosome,))
			else:
				learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
						parameters_bounds, number_of_init_sample, return_dict, 20, 'ucb', chromosome,))

			# running each bayesian optimization process in parallel by multiprocessing in python.
			parallel_learning(MAX_CORE, learning_process, learning_processes)

	else:
		for index in range(len(cpNum_files)):
			cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
			cpNum = int(cpNum_str[2:3])
			if call_type == "broad":
				def wrapper_function_broad(opt_Qval, opt_cutoff):
					accuracy = run(cpNum_files[index], validation_set + test_set, str(exp(opt_Qval/100)-1),\
							call_type, PATH, control_file, str(exp(opt_cutoff/100)-1),False,kry_file,)
					print cpNum_str,\
						"Qval :" + str(round(exp(opt_Qval/100)-1,4)),\
						"Broad-cutoff:" + str(round(exp(opt_cutoff/100)-1,4)),\
						"score:" + str(round(accuracy,4)) + '\n'
					return accuracy
				function = wrapper_function_broad
			else:
				def wrapper_function_narrow(opt_Qval):
					accuracy = run(cpNum_files[index], validation_set + test_set, str(exp(opt_Qval/100)-1)\
							, call_type, PATH, control_file,None,False,kry_file,)
					print cpNum_str,\
						"Qval :" + str(round(exp(opt_Qval/100)-1,4)),\
						"score:" + str(round(accuracy,4)) + '\n'
					return accuracy
				function = wrapper_function_narrow

			if call_type == "broad":
				learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
						parameters_bounds, number_of_init_sample, return_dict, 13, 'ei', cpNum,))
			else:
				learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
						parameters_bounds, number_of_init_sample, return_dict, 20, 'ucb', cpNum,))
			parallel_learning(MAX_CORE, learning_process, learning_processes)

	for proc in learning_processes:
		proc.join()
	
	print "finish learning parameter of MACS !"
	print "Running MACS with learned parameter . . . . . . . . . . . . ."
	
	learning_processes = []

	if kry_file is None:
		for chromosome in chromosome_list:
			parameters = return_dict[chromosome]['max_params']
			target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
			opt_Qval = parameters['opt_Qval']

			if call_type == 'broad':
				opt_cutoff = parameters['opt_cutoff']
				learning_process = multiprocessing.Process(target=run, args=(\
							target, validation_set + test_set, str(exp(opt_Qval/100)-1), call_type, PATH, control_file, \
							str(exp(opt_cutoff / 100) - 1), True,))
			else:
				learning_process = multiprocessing.Process(target=run, args=(\
							target, validation_set + test_set, str(opt_Qval), call_type, PATH, control_file,\
							None,True,))
				
			parallel_learning(MAX_CORE, learning_process, learning_processes)
	else:
		for index in range(len(cpNum_files)):
			cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
			cpNum = int(cpNum_str[2:3])
			
			parameters = return_dict[cpNum]['max_params']
			opt_Qval = parameters['opt_Qval']

			if call_type == 'broad':
				opt_cutoff = parameters['opt_cutoff']
				learning_process = multiprocessing.Process(target=run, args=(\
							cpNum_files[index], validation_set + test_set, str(exp(opt_Qval/100)-1), call_type, PATH, control_file, \
							str(exp(opt_cutoff / 100) - 1), True,kry_file,))
			else:
				learning_process = multiprocessing.Process(target=run, args=(\
							cpNum_files[index], validation_set + test_set, str(opt_Qval), call_type, PATH, control_file,\
							None,True,kry_file,))
				
			parallel_learning(MAX_CORE, learning_process, learning_processes)
			
	for proc in learning_processes:
		proc.join()
			 
	return return_dict	

def run(input_file, valid_set, Qval, call_type, PATH, control = None, broad=None, final=False, kry_file = None):
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
	
	pure_input_file = input_file.rsplit('/',1)[1]
	output_PATH = PATH + '/MACS/' + pure_input_file
	
	if call_type == "broad":
		output_format_type = '.broadPeak'
	else:
		output_format_type = '.narrowPeak'

	process = MACS.run(input_file, Qval, call_type, control, broad)
	process.wait()

	peakCalled_file = output_PATH[:-4] + ".bam_peaks" + output_format_type
	
	return return_accuracy(final, kry_file, peakCalled_file, valid_set)

