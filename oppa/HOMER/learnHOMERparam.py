from math import exp
import subprocess
import time
import os
from multiprocessing import cpu_count
from multiprocessing import Process, Manager
import multiprocessing

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

from HOMER import run as HOMER
from HOMER import run_control_processing as control_processing

def learnHOMERparam(args, test_set, validation_set, PATH):
	
	input_file = args.input
	control = args.control
	call_type = args.callType

	manager = Manager()
	return_dict = manager.dict()

	if call_type == "broad":
		parameters_bounds = {'size':(150,1000),\
			'minDist':(350,5000)}
	else:
		parameters_bounds = {'fdr':(10**-8,60)}
		
	number_of_init_sample = 1

	chromosome_list = []
	for label in validation_set + test_set:
		chromosome_list.append(label.split(':')[0])
	chromosome_list = sorted(list(set(chromosome_list)))

	reference_char = ".REF_"
	bam_name = input_file[:-4]
	
	MAX_CORE = cpu_count()
	learning_processes = []

	print " HOMER control ChIP-seq pre processing. . . . . . . . . . . . . ."
	control_processing(PATH, control)

	for chromosome in chromosome_list:
	
		if call_type == "broad":
			def wrapper_function_broad(size, minDist):
				target = bam_name + reference_char + chromosome + ".bam"
				accuracy = run(target, control, validation_set, call_type,\
						 PATH, str(size), str(minDist))
				print chromosome,\
					"size :" + str(size),\
					"minDist :" + str(minDist),\
					"score :" + str(round(accuracy,4))
				return accuracy
			function = wrapper_function_broad
		else:
			def wrapper_function_narrow(fdr):
				target = bam_name + reference_char + chromosome + ".bam"
				accuracy = run(target, control, validation_set, call_type,\
						 PATH, str(exp(fdr/100)-1))
				print chromosome,\
					"fdr :" + str(fdr),\
					"score :" + str(round(accuracy,4))
				return accuracy
			function = wrapper_function_narrow
		
		learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
					parameters_bounds, number_of_init_sample, return_dict, 20, 'ei', chromosome,))

		if len(learning_processes) < MAX_CORE/2:
			learning_processes.append(learning_process)
			learning_process.start()
		else:
			keep_wait = True
			while True:
				time.sleep(0.1)
				if not (keep_wait is True):
					break
				else:
				 	for process in reversed(learning_processes):
						if process.is_alive() is False:
							learning_processes.remove(process)
							learning_processes.append(learning_process)
							learning_process.start()
							keep_wait = False
							break

	for proc in learning_processes:
		proc.wait()
	print return_dict
	return return_dict


def run(input_file, control, valid_set, call_type, PATH, param, param2=None):

	output_PATH = PATH + '/HOMER/' + input_file[:-4]
	input_file = PATH + '/' + input_file

	if call_type == "broad":
		process = HOMER(input_file, control, call_type, PATH, size=param, minDist=param2)
	else:
		process = HOMER(input_file, control, call_type, PATH, fdr=param)

	process.wait()	

	output_format_type = ".bed"
	
	peakCalled_file = output_PATH + ".bam_peaks" + output_format_type

	if not valid_set:
		print "there is no matched validation set :p\n"
		exit()
	else:
		error_num, label_num = calculateError(peakCalled_file, parseLabel(valid_set, peakCalled_file))
		if os.path.isfile(peakCalled_file):
			os.remove(peakCalled_file)
		else:
			print "there is no result file."
	if label_num is 0:
		return 0.0

	return (1 - error_num/label_num)
