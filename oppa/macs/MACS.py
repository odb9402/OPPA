import os
import subprocess


def run(input_bam, input_q, call_type , control_bam, input_broad):
	
	output_name = input_bam.rsplit('/',1)[0] + '/MACS/' + input_bam.rsplit('/',1)[1]

	if call_type == "broad":
		commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, '--broad', "-g", "hs", "-n", output_name , "--broad-cutoff" , input_broad , "-q", input_q, '--nomodel']
	else:
		commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-g", "hs", "-n", output_name, "-q", input_q, '--nomodel']

	FNULL = open(os.devnull, 'w')
	process = subprocess.Popen(commands, stdout = FNULL, stderr=subprocess.STDOUT)
	return process
