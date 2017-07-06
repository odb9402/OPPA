"""
this module is actual fix some parameter by using
bayesian optimization. if we run this function in parallel,
we need to satisfied many condition which mentioned in the paper
named 'practical bayesian optimization in machine learning algorithm'
"""

from subprocess import call
import argparse
import numpy as np
from pfcProto import run_in_parallel




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
    run_in_parallel(MACS.run(bam_name + reference_char + "1.bam", args),
                    MACS.run(bam_name + reference_char + "2.bam", args),
                    MACS.run(bam_name + reference_char + "3.bam", args),
                    MACS.run(bam_name + reference_char + "4.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "5.bam", args),
                    MACS.run(bam_name + reference_char + "6.bam", args),
                    MACS.run(bam_name + reference_char + "7.bam", args),
                    MACS.run(bam_name + reference_char + "8.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "9.bam", args),
                    MACS.run(bam_name + reference_char + "10.bam", args),
                    MACS.run(bam_name + reference_char + "11.bam", args),
                    MACS.run(bam_name + reference_char + "12.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "13.bam", args),
                    MACS.run(bam_name + reference_char + "14.bam", args),
                    MACS.run(bam_name + reference_char + "15.bam", args),
                    MACS.run(bam_name + reference_char + "16.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "17.bam", args),
                    MACS.run(bam_name + reference_char + "18.bam", args),
                    MACS.run(bam_name + reference_char + "19.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "20.bam", args),
                    MACS.run(bam_name + reference_char + "21.bam", args),
                    MACS.run(bam_name + reference_char + "22.bam", args))

    run_in_parallel(MACS.run(bam_name + reference_char + "M.bam", args),
                    MACS.run(bam_name + reference_char + "X.bam", args),
                    MACS.run(bam_name + reference_char + "Y.bam", args))
    """
    errorCalculation.run("default",args.validSet)