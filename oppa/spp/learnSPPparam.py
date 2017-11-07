from math import exp
import subprocess
import time
import os
from multiprocessing import Process, Manager, cpu_count
import multiprocessing

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

def learnSPPparam(args, test_set, validation_set, PATH):

	input_file = args.input
	control = args.control
	call_type = args.callType

	manager = Manager()
	return_dict = manager.dict()

	if not os.path.exists(PATH + '/SPP'):
		os.makedirs(PATH + '/SPP')

	parameters_bounds = {'opt_fdr' : (0.005, 0.3)}
	number_of_init_sample = 2 

	chromosome_list = []
	for label in validation_set + test_set:
		chromosome_list.append(label.split(':')[0])
	chromosome_list = sorted(list(set(chromosome_list)))

	reference_char = ".REF_"
	bam_name = input_file[:-4]
	cr_bam_name = control[:-4]

	MAX_CORE = cpu_count()
	learning_processes = []

	print chromosome_list

	for chromosome in chromosome_list:
		def wrapper_function(opt_fdr):
			target = bam_name + reference_char + chromosome + '.bam'
			cr_target = cr_bam_name + '.bam' 
			accuracy = run(target, cr_target, validation_set, call_type, str(exp(opt_fdr)-1), PATH, False)
			print chromosome,\
				"fdr :" + str(round(exp(opt_fdr)-1,4)),\
				"score:" + str(round(accuracy,4)) + '\n'
			return accuracy
	
		function = wrapper_function
		learning_process = multiprocessing.Process(target=optimizeHyper, args=(function,\
					parameters_bounds, number_of_init_sample, return_dict, 7, 'ei', chromosome,))

		if len(learning_processes) < MAX_CORE - 1:
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
		proc.join()

	print "finish learning parameter of SPP ! "
	print "Running SPP with learned parameter . . . . . . . . . . . . . . ."

	for chromosome in chromosome_list:
		parameters = return_dict[chromosome]['max_params']
		target = bam_name + reference_char + chromosome + '.bam'
		opt_fdr = parameters['opt_fdr']

		learning_processes = []

		learning_process = multiprocessing.Process(target = run, args=(\
				target, control, validation_set + test_set, call_type, str(exp(opt_fdr)-1), PATH, True,))

		if len(learning_processes) < MAX_CORE - 1:
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
		proc.join()

	return return_dict


def run(input_file, control, valid_set, call_type, opt_fdr, PATH, final=False):
	
	output_PATH = PATH + '/SPP/' + input_file
	input_file = PATH + '/' + input_file

	if call_type == "broad":
		output_format_type = ".broadPeak"
	else:
		output_format_type = ".narrowPeak"
	
	peakCalled_file = output_PATH[:-4] + ".bam_peaks" + output_format_type

	FNULL = open(os.devnull, 'w')
	# run spp
	command = ['Rscript oppa/spp/run_spp.R -c='+input_file + ' -i='+control+' -fdr='+str(opt_fdr)+\
			  ' -savn='+ peakCalled_file + '_befSort' + ' -rf']
	subprocess.call(command, shell=True, stdout = FNULL, stderr=subprocess.STDOUT)

	# decompressing result file
	command = ['gunzip ' + peakCalled_file + '.gz']
	subprocess.call(command, shell=True, stdout = FNULL, stderr=subprocess.STDOUT)

	command = ['sort -k1,1n -k2,2n ' + peakCalled_file + '_befSort' + ' > '\
			   + peakCalled_file ]
	subprocess.call(command, shell= True, stdout = FNULL, stderr=subprocess.STDOUT)


	if not valid_set:
		print "there are no matched validation set :p\n"
		exit()
	else:
		error_num, label_num = calculateError(peakCalled_file, parseLabel(valid_set, peakCalled_file))

		if final:
			print peakCalled_file + " is stored."
		elif os.path.exists(peakCalled_file):
			os.remove(peakCalled_file)
		else:
			print "there is no result file."

	if label_num is 0:
		return 0.0

	if final:
		print "Test Score ::" + str(1-error_num/label_num) + "\n"
	return (1 - error_num/label_num)


