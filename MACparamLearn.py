"""
this module is actual fix some parameter by using
bayesian optimization. if we run this function in parallel,
we need to satisfied many condition which mentioned in the paper
named 'practical bayesian optimization in machine learning algorithm'
"""

from subprocess import call
import argparse
import numpy as np




def callLearningScript(input_bed, validSet, control_bam = "", input_q = "0.01"):
    """until we find proper parameter"""



def run(input_bed, input_labels):
    """it will be runned by protoPFC.py"""
    callLearningScript(input_bed, input_labels)

