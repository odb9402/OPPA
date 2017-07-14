import os
import subprocess


def run(input_file, Qval, call_type,control = None):
    """it will be runned by protoPFC.py"""
    if control is None:
        return callMAC(input_file, call_type, input_q = Qval)
    else:
        return callMAC(input_file, call_type, input_q = Qval, control_bam=control)



def callMAC(input_bam, call_type, control_bam= "", input_q = '0.05'):
    """call MACS by LINUX shell with input parameter"""
    """in MACS, can input control bam file for getting more accurate result, so check it"""

    if call_type == "broad":
	broad_cutoff = str(float(input_q) * 1.122)

    if control_bam is not "":
        if call_type == "broad":
            commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, '--broad', "-g", "hs", "-n", input_bam , "--broad-cutoff" , broad_cutoff]
        else:
            commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-g", "hs", "-n", input_bam, "-q", input_q]
    else:
        if call_type == "broad":
            commands = ["macs2", "callpeak", "-t", input_bam, '--broad',  "-g", "hs", "-n", input_bam, "--broad-cutoff" , broad_cutoff]
        else:
            commands = ["macs2", "callpeak", "-t", input_bam, "-g", "hs", "-n", input_bam,  "-q", input_q , "--broad-cutoff", bruoad_cutoff]
    # make subprocess has no output to shell
    # and throw that output into dev/null
    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(commands, stdout = FNULL, stderr=subprocess.STDOUT)
    return process
