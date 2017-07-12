import os
import subprocess


def run(input_file,  Qval, control = None):
    """it will be runned by protoPFC.py"""
    if control is None:
        return callMAC(input_file, input_q = Qval)
    else:
        return callMAC(input_file, input_q = Qval, control_bam=control)



def callMAC(input_bam, control_bam= "", input_q = '0.05'):
    """call MACS by LINUX shell with input parameter"""
    """in MACS, can input control bam file for getting more accurate result, so check it"""

    if control_bam is not "":
        commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, '--broad', "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q, "-n", input_bam]
    else:
        commands = ["macs2", "callpeak", "-t", input_bam, '--broad',  "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q, "-n", input_bam]

    
    # make subprocess has no output to shell
    # and throw that output into dev/null
    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(commands, stdout = FNULL, stderr=subprocess.STDOUT)
    return process
