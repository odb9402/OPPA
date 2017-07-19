import time
import rpy2.robjects as robjects
from multiprocessing import cpu_count
from multiprocessing import Process

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.loadLabel import run as loadLabel
from ..loadParser.parseLabel import run as parseLabel

def learnSPPparam(args, test_set, validation_set):
    pass

def run(input_file, valid_set, control=None):
    pass
