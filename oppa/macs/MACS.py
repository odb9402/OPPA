import os
import subprocess


def run(input_file, Qval, call_type,control = None, broad = None):
    if control is None:
	return callMAC(input_file, call_type, input_q = Qval, input_broad = broad)
    else:
        return callMAC(input_file, call_type, input_q = Qval, input_broad = broad, control_bam=control)



def callMAC(input_bam, call_type, control_bam= "", input_q = '0.05', input_broad = '0.1'):
    """call MACS by LINUX shell with input parameter"""
    """in MACS, can input control bam file for getting more accurate result, so check it"""
    output_name = input_bam.rsplit('/',1)[0] + '/MACS/' + input_bam.rsplit('/',1)[1]

    if control_bam is not "":
        if call_type == "broad":
            commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, '--broad', "-g", "hs", "-n", output_name , "--broad-cutoff" , input_broad , "-q", input_q, '--nomodel']
        else:
            commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-g", "hs", "-n", output_name, "-q", input_q, '--nomodel']
    else:
        if call_type == "broad":
            commands = ["macs2", "callpeak", "-t", input_bam, '--broad',  "-g", "hs", "-n", output_name, "--broad-cutoff" , input_broad, "-q", input_q, '--nomodel']
        else:
            commands = ["macs2", "callpeak", "-t", input_bam, "-g", "hs", "-n", output_name,  "-q", input_q, '--nomodel']
    # make subprocess has no output to shell
    # and throw that output into dev/null
    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(commands, stdout = FNULL, stderr=subprocess.STDOUT)
    return process
