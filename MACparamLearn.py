from subprocess import call
import argparse
import numpy as np
import rpy2.robjects as robjects

p_learned = 0.01

def peak_error(validSet):
    robjects.r.load(validSet)
    print robjects.r[validSet][0]


def gradient_search(search_rate = 0.05):
    pass

def callMAC(input_bam, input_q, validSet, control_bam = ""):
    if control_bam is not "":
        commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q]
    else:
        commands = ["macs2" , "callpeak", "-t", input_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q]
    peak_error(validSet)
    #call(commands)


def callLearningScript(input_bam, validSet, control_bam = "", input_q = "0.01"):
    while True:
        callMAC(input_bam,input_q,validSet)
        break

def run(args):
    if args.control is None:
        callLearningScript(args.input, args.validSet, input_q = args.Qval)
    else:
        callLearningScript(args.input, args.validSet, input_q = args.Qval, control_bam=args.control)
