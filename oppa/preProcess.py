from multiprocessing import cpu_count
from loadParser.loadKaryotype import run as loadKaryotype

import subprocess
import os
import glob


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

	print "\npreprocessing step. . . . . . . . . . . . . . . . . . . . .\n"
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
		split_by_karyotype(input_karyo, chromosome_list, regions, input_bam, PATH)


def split_by_karyotype(input_karyo, chromosome_list, regions, bamfile, PATH):
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
	print "spliting by karyotypes. . . . . . . . . . . . . . . . . . .\n"

	karyotypes = loadKaryotype(input_karyo, chromosome_list)

	for chr_no in range(len(regions)):
		region = regions[chr_no].split(':')[1]
		region = region.split('-')
		start_label = int(region[0])
		end_label = int(region[1])
		last_hit_cpnum = -1 	

		for kry in karyotypes:
			if kry['chr'] == chromosome_list[chr_no]:
				output_name = bamfile.rsplit('.')[0] + ".CP" + str(kry['cpNum']) + '_REF_' + chromosome_list[chr_no] + ".bam"

				if start_label < kry['start'] < end_label:
					str_new_regions = kry['chr'] + ':' + str(start_label) + '-' + str(kry['start'])

					if os.path.isfile(output_name):
						samtools_cat(bamfile, chromosome_list[chr_no], kry['cpNum'], str_new_regions, PATH)
					else:
						samtools(bamfile,str_new_regions,output_name,PATH)

					start_label = kry['start']
					last_hit_cpnum = kry['cpNum']


				elif start_label < kry['end'] < end_label:
					str_new_regions = kry['chr'] + ':' + str(start_label) + '-' + str(kry['end'])

					if os.path.isfile(output_name):
						samtools_cat(bamfile, chromosome_list[chr_no], kry['cpNum'], str_new_regions, PATH)
					else:
						samtools(bamfile, str_new_regions, output_name, PATH)

					start_label = kry['end']
					last_hit_cpnum = kry['cpNum']

		str_new_region = chromosome_list[chr_no] + ':' + str(start_label) + '-' + str(end_label)
		
		# If there was no spliting before, it should be marked copy number about remained reigon.
		if last_hit_cpnum == -1:
			for kry in karyotypes:
				if kry['chr'] == chromosome_list[chr_no]:
					if kry['start'] < start_label < kry['end']:
						print "A copy number of the remained region "+str_new_region+" is :" + str(kry['cpNum'])
						last_cpnum = kry['cpNum']
						before_name = bamfile.rsplit('.')[0] + ".REF_" + chromosome_list[chr_no] + ".bam"
						after_name = bamfile.rsplit('.')[0] + ".CP" + str(last_cpnum) + '_REF_' + chromosome_list[chr_no] + ".bam"
						print "'" + before_name + "' is changed to '" + after_name + "'\n"
						os.rename(PATH + '/' + before_name, PATH + '/' + after_name)
						break
			
		# If there was spliting , it should be last processing. 
		else:
			samtools_cat(bamfile, chromosome_list[chr_no], last_hit_cpnum, str_new_region, PATH)

	# Eliminate files which was splited before by chromosome.
	for chr_no in chromosome_list:
		if os.path.exists(PATH+'/'+bamfile.rsplit('.')[0]+'.REF_'+chr_no+'.bam'):
			os.remove(PATH+'/'+bamfile.rsplit('.')[0]+'.REF_'+chr_no+'.bam')


def combine_by_karyotypes(file_name, PATH):
	"""

	:param file_name:
	:param PATH:
	:return:
	"""

	file_list = glob.glob(PATH + '/*.bam')

	cpNum_list = []
	for file in file_list:
		cpNum = int(file.split('.')[1].split('_')[0][2:])
		cpNum_list.append(cpNum)

	cpNum_set = list(set(cpNum_list))

	kry_list = []
	for cpNum in cpNum_set:
		kry_set = []
		for index in range(len(cpNum_list)):
			if cpNum_list[index] == cpNum:
				kry_set.append(file_list[index])
		kry_list.append(kry_set)

	for index in range(len(cpNum_set)):
		output_name = PATH + '/' + file_name.split('.')[0] + ".CP" + str(cpNum_set[index]) + ".bam"
		input_strings = ""

		if len(kry_list[index]) == 1:
			cpNum_string = "CP" + str(cpNum_set[index])
			os.rename(glob.glob(PATH + "/*" + cpNum_string + "*")[0] , PATH + '/' + file_name.split('.')[0] + ".CP" + str(cpNum_set[index]) + ".bam" )
			print "'" + PATH + '/' + file_name.split('.')[0] + ".CP" + str(cpNum_set[index]) + ".bam" + "' is renamed about a karyotype copy number.\n"

		else:
			for string in kry_list[index]:
				input_strings += (string + " ")
			cat_command = ['sudo samtools cat -o ' + output_name + ' ' + input_strings]
			FNULL = open(os.devnull, 'w')
			subprocess.call(cat_command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
			print "'" + output_name + "' is combined about same karyotype.\n"


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


def samtools_cat(input_bam, chr_num, cp_num, region, PATH):
	"""
	This is Python wrapper of Samtools-cat.

	:param input_bam:
	:param chr_num:
	:param cp_num:
	:param region:
	:param PATH:
	:return:
	"""

	print "There is copy numbers which duplicated so cat It. . . ."

	input_file = input_bam.rsplit('.')[0] + ".CP" + str(cp_num) + '_REF_' + chr_num + ".bam"
	samtools(input_bam, region, "temp_source.bam", PATH)
	cat_command = ['sudo samtools cat -o ' + PATH + '/temp_target.bam ' + PATH + '/temp_source.bam ' + PATH + '/' + input_file]
	FNULL = open(os.devnull, 'w')
	subprocess.call(cat_command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

	os.remove(PATH + '/' + input_file)
	os.rename(PATH + '/temp_target.bam', PATH + '/' + input_file)
	os.remove(PATH + '/temp_source.bam')
	print "'" + input_file + "' is combined\n"


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
	if not (input_karyo is None):
		combine_by_karyotypes(input_bam, PATH)
