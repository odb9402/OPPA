from multiprocessing import cpu_count
import subprocess
import os
import time

from loadParser import parseLabel

def run(input_bam, valid_set, PATH):
	"""

	:param input_bam: name of input bam file for samtools.

	:param valid_set: python list of each line in labeled file.

	:return:
	"""
	print "preprocessing step. . . . . . . . . . . . . . . . . . . ."
	print "indexing bam file . . . . . . . . . . . . . . . . . . . ."

	subprocess.call(['bamtools','index','-in',input_bam])
	bam_name = input_bam[:-4]  ## delete '.bam'
	reference_char = ".REF_"

	label_regions = []
	for label in valid_set:
		label_regions.append(label.split(' ',1)[0])

	chromosome_list = []
	for label in valid_set:
		chromosome_list.append(label.split(':')[0])
	chromosome_list = sorted(list(set(chromosome_list)))

	pre_regions = []
	for chromosome in chromosome_list:
		containor = ""
		for label in label_regions:
			if chromosome + ":" in label:
				containor += label + " "
		pre_regions.append(containor)

	regions = []
	for region in pre_regions:
		region = region.replace(",","")
		def getKey(item):
			return int(item.split('-')[1])
		containor = sorted(region.split(), key=getKey)

		start = containor[0].split(':')[1].split('-')[0]
		end = containor[-1].rsplit('-')[1]
		
		distance = str(int(end) - int(start))

		start = str(int(start) - (int(distance)/15))
		end = str(int(end) + (int(distance)/15))

		regions.append(containor[0].split(':')[0]+':'+start+'-'+end)


	MAX_CORE  = cpu_count()
	TASKS = len(chromosome_list)
	TASK_NO = 0
	samtools_process = []

	bam_name = bam_name + reference_char 

	print "slicing bam file with samtools. . . . . . . . . . . . . ."

	"""	while (len(samtools_process) < MAX_CORE - 1) and (TASK_NO < TASKS):
		samtools_process.append(samtools(input_bam, regions[TASK_NO], bam_name +chromosome_list[TASK_NO] + ".bam", PATH))
		TASK_NO += 1	

	while len(samtools_process) > 0:
		time.sleep(0.1)

        for proc in reversed(range(len(samtools_process))):
        	if samtools_process[proc].poll() is not None:
				del samtools_process[proc]

		while (len(samtools_process) < MAX_CORE - 1) and (TASK_NO < TASKS):
			samtools_process.append(samtools(input_bam, regions[TASK_NO], bam_name\
					+ chromosome_list[TASK_NO] + ".bam", PATH))
			TASK_NO += 1"""

	for TASK_NO in range(TASKS):
		samtools(input_bam, regions[TASK_NO], bam_name + chromosome_list[TASK_NO] + ".bam", PATH)

def samtools(input_bam, regions, output_name, PATH):
	
	# check input file is full path or not
	if not ('/' in input_bam):
		input_bam = os.getcwd() + '/' + input_bam

	target = PATH + '/' + output_name	
	commands = ["samtools view -b " + input_bam + " " + regions + ' > ' + target]
	print "'"+target+"' is created" + "\n regions  ::: " + regions + "\n"
	FNULL = open(os.devnull, 'w')
	subprocess.call(commands, shell = True, stdout = FNULL, stderr=subprocess.STDOUT)
