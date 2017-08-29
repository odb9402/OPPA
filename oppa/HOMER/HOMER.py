import subprocess
import os


def run(input_file, control, call_type, directory, fdr=None, size=None, minDist=None):
	
	homer_PATH = os.getcwd() + '/dependencies/cpp/'
	pure_input_file = input_file.rsplit('/',1)[1]
	target_PATH = directory + '/HOMER/' + pure_input_file + '/'
	control_PATH = directory + '/HOMER/' + control + '/'

	output_name = target_PATH[:-5] + ".txt"
	FNULL = open(os.devnull, 'w')
	
	#preProcess in Hoemr
	command = [homer_PATH + 'makeTagDirectory ' + target_PATH + ' ' +input_file]
	process = subprocess.Popen(command, shell= True, stdout = FNULL, stderr=subprocess.STDOUT)
	process.wait()

	if call_type == "broad":
		command = [homer_PATH + 'findPeaks ' + target_PATH + ' -style histone'+\
				   ' -o ' + output_name + ' -i ' + control_PATH + ' -size ' + size +\
				   ' -minDist ' + minDist + ' -fdr ' + fdr]
		process = subprocess.Popen(command, shell= True, stdout = FNULL, stderr=subprocess.STDOUT)
	else:
		command = [homer_PATH + 'findPeaks ' + target_PATH + ' -style factor' +\
				  	' -o '+ output_name + ' -i ' + control_PATH + ' -fdr ' + fdr]
		process = subprocess.Popen(command, shell= True, stdout = FNULL, stderr=subprocess.STDOUT)
	process.wait()

	
	if os.path.isfile(output_name):
		command = [os.getcwd()+'/dependencies/bin/pos2bed.pl ' + output_name +\
				  ' > ' + output_name[:-4] + ".bam_peaks.bed"]
		subprocess.call(command, shell= True, stdout = FNULL, stderr=subprocess.STDOUT)

	return process


def run_control_processing(directory, control):
	
	homer_PATH = os.getcwd() + '/dependencies/cpp/'
	control_PATH = directory + '/HOMER/' + control + '/'

	cont_command = [homer_PATH+'makeTagDirectory ' + control_PATH + ' ' + control]
	process = subprocess.Popen(cont_command, shell= True)
	process.wait()
