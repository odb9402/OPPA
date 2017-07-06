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



def run(args):
    import MACS
    import errorCalculation

    learned_Qval = args.Qval

    """it will be runned by protoPFC.py"""
    bam_name = args.input[:-4]  ## delete '.bam'
    reference_char = ".REF_chr"

    """
    run_in_parallel(MACS.run(bam_name + reference_char + "1.bam"),
                    MACS.run(bam_name + reference_char + "2.bam"),
                    MACS.run(bam_name + reference_char + "3.bam"),
                    MACS.run(bam_name + reference_char + "4.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "5.bam"),
                    MACS.run(bam_name + reference_char + "6.bam"),
                    MACS.run(bam_name + reference_char + "7.bam"),
                    MACS.run(bam_name + reference_char + "8.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "9.bam"),
                    MACS.run(bam_name + reference_char + "10.bam"),
                    MACS.run(bam_name + reference_char + "11.bam"),
                    MACS.run(bam_name + reference_char + "12.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "13.bam"),
                    MACS.run(bam_name + reference_char + "14.bam"),
                    MACS.run(bam_name + reference_char + "15.bam"),
                    MACS.run(bam_name + reference_char + "16.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "17.bam"),
                    MACS.run(bam_name + reference_char + "18.bam"),
                    MACS.run(bam_name + reference_char + "19.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "20.bam"),
                    MACS.run(bam_name + reference_char + "21.bam"),
                    MACS.run(bam_name + reference_char + "22.bam"))

    run_in_parallel(MACS.run(bam_name + reference_char + "M.bam"),
                    MACS.run(bam_name + reference_char + "X.bam"),
                    MACS.run(bam_name + reference_char + "Y.bam"))
    """

    errorCalculation.run("default",args.validSet)