import sys

from ..loadParser.loadPeak import run as loadPeak

def ensembleMethod(results_files, test_errors):

	peaks = []	

	for files in result_files:
		peaks.append(loadPeak(result_files))

	print peaks[0]	

ensembleMethod(sys.argv[1], sys.argv[2])
