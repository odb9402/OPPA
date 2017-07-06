import os
import sys

def run(input_file, args):
    """it will be runned by protoPFC.py"""
    if args.control is None:
        callMAC(input_file, args.validSet, input_q = args.Qval)
    else:
        callMAC(input_file, args.validSet, input_q = args.Qval, control_bam=args.control)


def callMAC(input_bam, input_q, validSet, control_bam=""):
    """call MACS by LINUX shell with input parameter"""
    """in MACS, can input control bam file for getting more accurate result, so check it"""

    if control_bam is not "":
        commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q, "-n", input_bam]
    else:
        commands = ["macs2", "callpeak", "-t", input_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q, "-n", input_bam]


    #call(commands)
