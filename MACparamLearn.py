"""
this module is actual fix some parameter by using
bayesian optimization. if we run this function in parallel,
we need to satisfied many condition which mentioned in the paper
named 'practical bayesian optimization in machine learning algorithm'
"""

from subprocess import call
from subprocess import Popen
import argparse
import numpy as np


def callLearningScript(input_bed, validSet, control_bam = "", input_q = "0.01"):
    """until we find proper parameter"""


def run(args):
    import MACS
    import errorCalculation

    learned_Qval = args.Qval

    """it will be runned by protoPFC.py"""
    bam_name = args.input[:-4]  ## delete '.bam'
    reference_char = ".REF_chr"

    p1 = MACS.run(bam_name + reference_char + "1.bam", args)
    p2 = MACS.run(bam_name + reference_char + "2.bam", args)
    p3 = MACS.run(bam_name + reference_char + "3.bam", args)
    p4 = MACS.run(bam_name + reference_char + "4.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "5.bam", args)
    p2 = MACS.run(bam_name + reference_char + "6.bam", args)
    p3 = MACS.run(bam_name + reference_char + "7.bam", args)
    p4 = MACS.run(bam_name + reference_char + "8.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "9.bam", args)
    p2 = MACS.run(bam_name + reference_char + "10.bam", args)
    p3 = MACS.run(bam_name + reference_char + "11.bam", args)
    p4 = MACS.run(bam_name + reference_char + "12.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()

    p1 = MACS.run(bam_name + reference_char + "13.bam", args)
    p2 = MACS.run(bam_name + reference_char + "14.bam", args)
    p3 = MACS.run(bam_name + reference_char + "15.bam", args)
    p4 = MACS.run(bam_name + reference_char + "16.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()
    
    p1 = MACS.run(bam_name + reference_char + "17.bam", args)
    p2 = MACS.run(bam_name + reference_char + "18.bam", args)
    p3 = MACS.run(bam_name + reference_char + "19.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()

    p1 = MACS.run(bam_name + reference_char + "20.bam", args)
    p2 = MACS.run(bam_name + reference_char + "21.bam", args)
    p3 = MACS.run(bam_name + reference_char + "22.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()
    
    p1 = MACS.run(bam_name + reference_char + "M.bam", args)
    p2 = MACS.run(bam_name + reference_char + "X.bam", args)
    p3 = MACS.run(bam_name + reference_char + "Y.bam", args)
    p1.wait()
    p2.wait()
    p3.wait()

    """The ErrorCalculation can be also parallel by choromosome.
    """
    ##errorCalculation.run("default",args.validSet)
