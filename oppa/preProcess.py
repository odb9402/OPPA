from multiprocessing import cpu_count
from loadParser.loadKaryotype import run as loadKaryotype

import subprocess
import os


def split_by_chr(input_bam, valid_set, PATH, input_karyo):
	"""
	This method make subsection of bam files from input_bam
	and it will write that subsection as file in PATH.
	Those files will be input file of Bayesian Optimization
	Process and it can run in parallel.

	:param input_bam: name of input bam file for samtools.

	:param valid_set: python list of each line in labeled file.

	:param PATH:

	:return:
	"""

	print "\npreprocessing step. . . . . . . . . . . . . . . . . . . .\n"
	print "spliting by chromosome. . . . . . . . . . . . . . . . . . .\n"
	print "indexing bam file by Bamtools . . . . . . . . . . . . . . .\n"

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

	print "slicing bam file with samtools. . . . . . . . . . . . . .\n"

	for TASK_NO in range(TASKS):
		samtools(input_bam, regions[TASK_NO], bam_name + chromosome_list[TASK_NO] + ".bam", PATH)


	if not (input_karyo == None):
		"""
			If analysis by karyotype argument is true, need additional slicing.
			Karyotype data Table ::

			chromosome / chr start / chr end / copy number / size
		
		"""
		karyotypes = loadKaryotype(input_karyo, chromosome_list)
		print karyotypes


def split_by_karyotype(input_bam, kayrotypes, PATH):
	"""
	This method make subsection of bam files from input_bam
	and it will write that subsection as file in PATH.
	Those files will be input file of Bayesian Optimization
	Process and it can run in parallel.

	:param input_bam: name of input bam file for samtools.

	:param kayrotypes:

	:param PATH:

	:return:
	"""

	print "\npreprocessing step. . . . . . . . . . . . . . . . . . . .\n"
	print "spliting by karyotype . . . . . . . . . . . . . . . . . . .\n"
	print "indexing bam file by Bamtools . . . . . . . . . . . . . . .\n"

	subprocess.call(['bamtools','index','-in',input_bam])




def samtools(input_bam, regions, output_name, PATH):
	"""
	This is Python wrapper of Samtools.

	:param input_bam:
	:param regions:
	:param output_name:
	:param PATH:
	:return:
	"""
	# check input file is full path or not
	if not ('/' in input_bam):
		input_bam = os.getcwd() + '/' + input_bam

	target = PATH + '/' + output_name	
	commands = ["samtools view -b " + input_bam + " " + regions + ' > ' + target]
	print "'"+target+"' is created" + "\n regions  ::: " + regions + "\n"
	FNULL = open(os.devnull, 'w')
	subprocess.call(commands, shell = True, stdout = FNULL, stderr=subprocess.STDOUT)


def run(input_bam, valid_set, PATH, input_karyo=None):
	"""
	There are two ways to preprocesses ( spliting ) which are
	spliting by chromosome or kayrotype.

	:param input_bam:

	:param valid_set:

	:param PATH:

	:param input_kayro:

	:return:
	"""

	split_by_chr(input_bam, valid_set, PATH, input_karyo)
