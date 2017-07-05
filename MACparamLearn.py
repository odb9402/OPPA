from subprocess import call
import argparse
import numpy as np
import rpy2.robjects as robjects


def peak_label_load(validSet):
    """loading Validation Set Files and translate to Python Object."""
    valid_file = open(validSet, 'r')
    peak_data = valid_file.readlines()
    peak_labels = []

    for peak in peak_data:
	if peak == "\r\n":
	    peak_data.remove(peak)
    for peak in peak_data:
	peak = peak.rstrip('\r\n')
	peak_labels.append(peak) 

    valid_file.close()

    return peak_labels


    
def parse_peak_labels(peak_labels):
    """Parsing Peak_labels by each chromosome and cell_types
	if there are correct , append to result and return."""
    
    labels = []
    chromosome_num = 0
    cell_type = ""

    for peak in peak_labels:
	containor = []
	containor.append(peak.split(':')[0])
	containor.append(peak.split(':')[1].split())
	labels.append(containor)

    print "what chromosome you choose? :: e. g. chrN "
    chromosome_num = raw_input()
    print "what cell type you choose? :: e. g. {tcell, bcell, monocyte,... etc }"
    cell_type = raw_input()

    result_labels_list = []

    for label in labels:
	if label[0] == chromosome_num:
	    if (cell_type in label[1] or 'peaks' in label[1]):
	        result_labels_list.append(label[1])

    print "%d`s label data is found.\n" % len(result_labels_list)
    
    if len(result_labels_list) == 0:
	print "there are matched label data."    

    print result_labels_list
 


def calculate_error():
    pass



def gradient_search(search_rate = 0.05):
    """gradient_search algorithm for learning parameter about error rate"""
    pass



def callMAC(input_bam, input_q, validSet, control_bam = ""):
    """call MACS by LINUX shell with input parameter"""
    """in MACS, can input control bam file for getting more accurate result, so check it"""

    if control_bam is not "":
        commands = ["macs2", "callpeak", "-t", input_bam, "-c", control_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q]
    else:
        commands = ["macs2" , "callpeak", "-t", input_bam, "-f", "BAM", "-g", "hs", "-n", input_bam
            , "-B", "-q", input_q]
    
    peak_labels = peak_label_load(validSet)
    peak_labels = parse_peak_labels(peak_labels)    

    #call(commands)



def callLearningScript(input_bam, validSet, control_bam = "", input_q = "0.01"):
    """keep call MACS until we find proper parameter"""
    while True:
        callMAC(input_bam,input_q,validSet)
        break



def run(args):
    """it will be runned by protoPFC.py"""
    if args.control is None:
        callLearningScript(args.input, args.validSet, input_q = args.Qval)
    else:
        callLearningScript(args.input, args.validSet, input_q = args.Qval, control_bam=args.control)
