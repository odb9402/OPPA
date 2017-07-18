from multiprocessing import cpu_count
import subprocess
import os
import time

from loadParser import parseLabel

def run(input_bam, valid_set):
    """

    :param input_bam: name of input bam file for samtools.

    :param valid_set: python list of each line in labeled file.

    :return:
    """
    subprocess.call(['bamtools','index','-in',input_bam])
    bam_name = input_bam[:-4]  ## delete '.bam'
    reference_char = ".REF_"

    label_regions = []
    for label in valid_set:
        label_regions.append(label.split(' ',1)[0])

    chromosome_list = []
    for label in valid_set:
        chromosome_list.append(label.split(':')[0])
    chromosome_list = list(set(chromosome_list))

    regions = []
    for chromosome in chromosome_list:
	containor = ""
	for label in label_regions:
	    if chromosome in label:
		containor += label + " "
        regions.append(containor)

    MAX_CORE = cpu_count()
    TASKS = len(chromosome_list)
    TASK_NO = 0
    samtools_process = []

    bam_name = bam_name + reference_char 

    while (len(samtools_process) < MAX_CORE - 1) and (TASK_NO < TASKS):
	samtools_process.append(samtools(input_bam, regions[TASK_NO], bam_name + chromosome_list[TASK_NO] + ".bam"))
	TASK_NO += 1	
	output_name = bam_name + reference_char + chromosome_list[TASK_NO] + ".bam"

    while len(samtools_process) > 0:
        time.sleep(0.1)

        for proc in reversed(range(len(samtools_process))):
            if samtools_process[proc].poll() is not None:
                del samtools_process[proc]

        while (len(samtools_process) < MAX_CORE - 1) and (TASK_NO < TASKS):
            samtools_process.append(samtools(input_bam, regions[TASK_NO], bam_name + chromosome_list[TASK_NO] +".bam"))
            TASK_NO += 1


def samtools(input_bam, regions, output_name):
    
    commands = ['samtools','view','-b',input_bam ,regions,'>',output_name]
    print commands
    FNULL = open(os.devnull, 'w')
    return subprocess.Popen(commands, stdout = FNULL, stderr=subprocess.STDOUT)

