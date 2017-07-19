import time
import rpy2.robjects as robjects
from multiprocessing import cpu_count
from multiprocessing import Process

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

def learnSPPparam(args, test_set, validation_set):
    
    input_file = args.input
    control = args.control
    call_type = args.callType

    def wrapper_function(opt_fdr):
	error = run(input_file, validation_set, str(opt_fdr), call_type, control)
	return -error

    parameter_bound = {'opt_fdr' : (0,1)}
    number_of_init_sample = 2

    fdr = 0.01
    run(input_file, validation_set, fdr, call_type, control)

def run(input_file, valid_set, opt_fdr, call_type, control=None):
    
    robjects.r.source('oppa/spp/spp.r')
    SPP = robjects.globalenv['py_spp']

    SPP(input_file,control,fdr=opt_fdr)
