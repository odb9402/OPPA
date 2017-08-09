import time
from multiprocessing import cpu_count
from multiprocessing import Process
import subprocess
import os

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

def learnPSparam(args, test_set, validation_set):

	def wrapper_function(opt_fdr):
		error = run(args.input, args.control, validation_set,args.callType)
		return error

	parameter_bound = {'opt_fdr' : (10**-8,0.9)}
	number_of_init_sample = 2


def run(input_file, control_file ,valid_set, call_type):
	curr_dir = os.getcwd()
	PATH = curr_dir + '/dependencies/PeakSeq/bin/PeakSeq'

    command = ['./'+PATH, '-peak_select', curr_dir + input_file, curr_dir\
				, ]
