import sys
import ensemble

from ..loadParser.loadPeak import run as loadPeak

def ensembleMethod(result_files, test_errors):

	peaks = []
	for files in result_files:
		peaks.append(loadPeak(files))
	ensemble.ensembler(peaks, test_errors)
