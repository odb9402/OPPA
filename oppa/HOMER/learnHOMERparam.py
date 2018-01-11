from math import exp
import glob
import os
import re
from multiprocessing import cpu_count, Process, Manager
import multiprocessing

from ..Helper.tools import parallel_learning
from ..Helper.tools import return_accuracy
from ..Helper.tools import extract_chr_cpNum
from ..optimizeHyper import run as optimizeHyper

from HOMER import run as HOMER
from HOMER import run_control_processing as control_processing

def learnHOMERparam(args, test_set, validation_set, PATH, kry_file=None, call_type=None):
	input_file = args.input
	control_file = args.control
	chromosome_list = []
	cpNum_files = []
	cpNum_controls = []

	manager = Manager()
	return_dict = manager.dict()

	if call_type == "broad":
		parameters_bounds = {'size':(150.0/1000,1.0),\
			'minDist':(350.0/5000,1.0),\
			'fdr':(10**-6,0.3)}
	else:
		parameters_bounds = {'fdr':(10**-8,0.3)}
		
	number_of_init_sample = 5

	chromosome_list, cpNum_controls, cpNum_files = extract_chr_cpNum(chromosome_list, input_file, control_file,
																	 cpNum_controls, cpNum_files, kry_file, test_set,
																	 validation_set + test_set, PATH, tool_name='HOMER')

	print " HOMER control ChIP-seq pre processing. . . . . . . . . . . . . ."
	control_processing(PATH, control_file)

	reference_char = ".REF_"
	bam_name = input_file[:-4]
	cr_bam_name = control_file[:-4]

	MAX_CORE = cpu_count()
	learning_processes = []

	##################################################################

	if kry_file is None:
		for chromosome in chromosome_list:
			if call_type == "broad":
				def wrapper_function_broad(size, minDist,fdr):
					target = PATH + '/' +bam_name + reference_char + chromosome + ".bam"
					accuracy = run(target, control_file, validation_set, call_type,\
							PATH, str(exp(fdr)-1) ,str(size*1000), str(minDist*5000))
					print chromosome,\
						"fdr :" + str(round(exp(fdr)-1,4)),\
						"size :" + str(size*1000),\
						"minDist :" + str(minDist*5000),\
						"score :" + str(round(accuracy,4)) + "\n"
					return accuracy
				function = wrapper_function_broad
			else:
				def wrapper_function_narrow(fdr):
					target = PATH + '/' + bam_name + reference_char + chromosome + ".bam"
					accuracy = run(target, control_file, validation_set, call_type,\
							PATH, str(exp(fdr)-1))
					print chromosome,\
						"fdr :" + str(round(exp(fdr)-1,4)),\
						"score :" + str(round(accuracy,4)) + "\n"
					return accuracy
				function = wrapper_function_narrow
			
			learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
						parameters_bounds, number_of_init_sample, return_dict, 30, 'ei', chromosome,))

			parallel_learning(MAX_CORE, learning_process, learning_processes)

	else:
		for index in range(len(cpNum_files)):
			cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
			cpNum = int(cpNum_str[2:3])
			if call_type == "broad":
				def wrapper_function_broad(size, minDist,fdr):
					accuracy = run(cpNum_files[index], control_file, validation_set, call_type,\
							PATH, str(exp(fdr)-1) ,str(size*1000), str(minDist*5000),False,kry_file)
					print cpNum_str,\
						"fdr :" + str(round(exp(fdr)-1,4)),\
						"size :" + str(size*1000),\
						"minDist :" + str(minDist*5000),\
						"score :" + str(round(accuracy,4)) + "\n"
					return accuracy
				function = wrapper_function_broad
			else:
				def wrapper_function_narrow(fdr):
					accuracy = run(cpNum_files[index], control_file, validation_set, call_type,\
							PATH, str(exp(fdr)-1), None, None, False, kry_file)
					print cpNum_str,\
						"fdr :" + str(round(exp(fdr)-1,4)),\
						"score :" + str(round(accuracy,4)) + "\n"
					return accuracy
				function = wrapper_function_narrow
			
			learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
				parameters_bounds, number_of_init_sample, return_dict, 30, 'ei', cpNum,))
			parallel_learning(MAX_CORE, learning_process, learning_processes)
	
	for proc in learning_processes:
		proc.join()
	
	print "finish learning parameter of HOMER !"
	print "Running HOMER with learned parameter . . . . . . . . . . . . ."

	learning_processes = []

	# final run about result.
	if kry_file is None:
		for chromosome in chromosome_list:
			parameters = return_dict[chromosome]['max_params']
			target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
			fdr = parameters['fdr']

			if call_type == 'broad':
				size = parameters['size']
				minDist = parameters['minDist']

				learning_process = multiprocessing.Process(target=run, args=(\
							target, control_file, test_set, call_type, PATH, str(exp(fdr)-1),\
							str(size*1000), str(minDist*5000), True,))
			else:
				learning_process = multiprocessing.Process(target=run, args=(\
							target, control_file, test_set, call_type, PATH, str(exp(fdr)-1), None, None, True,))
				
			parallel_learning(MAX_CORE, learning_process, learning_processes)
	else:
		for index in range(len(cpNum_files)):
			cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
			cpNum = int(cpNum_str[2:3])

			parameters = return_dict[cpNum]['max_params']
			fdr = parameters['fdr']
			
			if call_type == 'broad':
				size = parameters['size']
				minDist = parameters['minDist']
				learning_process = multiprocessing.Process(target=run, args=(\
					cpNum_files[index], control_file, test_set, call_type, PATH, str(exp(fdr)-1),\
					str(size*1000), str(minDist*5000), True, kry_file))
			else:
				learning_process = multiprocessing.Process(target=run, args=(\
					cpNum_files[index], control_file, test_set, call_type, PATH, str(exp(fdr)-1), None, None, True,kry_file,))
				
			parallel_learning(MAX_CORE, learning_process, learning_processes)

	for proc in learning_processes:
		proc.join()

	return return_dict


def run(input_file, control, valid_set, call_type, PATH, fdr_in, size_in=None, minDist_in=None, final=False, kry_file = None):
	"""

	:param input_file:
	:param control:
	:param valid_set:
	:param call_type:
	:param PATH:
	:param param:
	:param param2:
	:param param3:
	:param final:

	:return:
	"""
	pure_input_file = input_file.rsplit('/',1)[1]
	output_PATH = PATH + '/HOMER/' + pure_input_file[:-4]

	if call_type == "broad":
		process = HOMER(input_file, control, call_type, PATH, fdr=fdr_in ,size=size_in, minDist=minDist_in)
	else:
		process = HOMER(input_file, control, call_type, PATH, fdr=fdr_in)

	process.wait()	

	peakCalled_file = output_PATH + ".bam_peaks.bed"

	return return_accuracy(final, kry_file, peakCalled_file, valid_set)