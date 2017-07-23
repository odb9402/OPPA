import sys
import ensemble

from ..loadParser.loadPeak import run as loadPeak

def ensembleMethod(result_files, test_errors):
	"""
	this function make connection python with ensemble.cpp
	it call ensemble.ensembler C++ module with result of each peak detectors,
	and will get back summary data of ensemble method.

	:param result_files:
		this is result file of each peak detector ( narrowPeak, broadPeak .. etc )

	:param test_errors:
		this is error rate of each peak detector ( error rate of MACS, SPP... etc )

	:return:
	 	summary file of after ensemble method.
	"""

	peaks = []
	for files in result_files:
		peaks.append(loadPeak(files))
	ensemble.ensembler(peaks, test_errors)
