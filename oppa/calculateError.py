"""this is the module for error calculation. it will run parallel also.
and this module can be used to regular, for MACS and peakSeq which any algorithms
return as bed, narrowpeak, broadpeak file format."""
import os
import random
from loadParser.loadPeak import run as loadPeak

def calculate_error(peak_data, labeled_data, cell_type):
    """
    calculate actual error by numbering to wrong label

    :param peak_data:
    	python map is parsed and it is from result of peak calling algorithm
	like a MACS.
    :param labeled_data:
    	python map is parsed and it is from labeled data file.
    :return:
    	return python tuple ( number of incorrect label , number of whole label )
    """


    error_num = 0.0

    for label in labeled_data:
        if label['peakStat'] == 'peaks':
#	    print "peaks"
            if not is_peak(peak_data, label['regions'], weak_predict= True):
		error_num += 1
#		print "error : peaks"
	elif label['peakStat'] == 'peakStart' or label['peakStat'] == 'peakEnd':
#           print "peakStart PeakEnd"
	    if not is_peak(peak_data, label['regions']):
		error_num += 1
#		print "error : peakStart peakEnd"
	else:
#	    print " no peak"
            if not is_noPeak(peak_data, label['regions']):
		error_num += 1
#		print "error : nopeaks"

    return error_num, len(labeled_data)



def is_peak(target, value, tolerance = 0, weak_predict = False):
    """

    :param target:
    :param value:
    :param tolerance:
    :param weak_predict:
    :return:
    """
    """this function will find to regions in target bed set by using binary search"""
    """the similarity allow the distance of bed file row between label area as long as own value"""

    index = len(target)/2
    min_index = 0
    max_index = len(target)

    # if find correct one, return True
    while True:
        correct_ness = is_same(target, value, index, tolerance)

# 	print len(target), min_index, index, max_index
#       print target[index]['region_s'], target[index]['region_e'], value  

        if correct_ness is 'less':
            max_index = index
            index = (min_index + index) / 2
        elif correct_ness is 'upper':
            min_index = index
            index = (max_index + index) / 2
        #find correct regions
        else:
            # if label is "peaks", correct regions can be bigger than 2.
            # but "peakStart" or "peakEnd" are not they must exist only 1 correct regions.

            if (weak_predict == True):
                return True

            #find one peak
            else:
		if (index + 1) is not len(target)\
	 		and is_same(target, value, index + 1, tolerance) is 'in'\
			or is_same(target, value, index - 1, tolerance) is 'in':
		   return False
		else:
		   return True

	if max_index <= min_index + 1:
	    if is_same(target, value, index , tolerance) is 'in':
		return True
	    else:
		return False


def is_noPeak(target, value, tolerance = 0):
    """

    :param target:
    :param value:
    :param tolerance:
    :return:
    """
    region_min = value[0]
    region_max = value[1]

    #for find start regions, delete end regions
#    value[1] = value[0]

    index = len(target)/2
    min_index = 0
    max_index = len(target)
    steps = 1

    while True:
        find_matched = is_same(target, value, index, 0)

        if find_matched is 'less':
            max_index = index
            index = (min_index + index) / 2
        elif find_matched is 'upper':
            min_index = index
            index = (max_index + index) / 2
        #find correct regions
        else:
	    return False

        if abs(float(target[index]['region_e']) - region_min) < 5 * steps or steps > 1000:
            break
        steps += 1

    #correct label ( no peak )
    if not( index + 1 >= len(target) ):
        if float(target[index + 1]['region_s']) + tolerance > region_max\
		and float(target[index]['region_e']) + tolerance < region_min:
	    return True
    
    #false negative no peak ( there is peak )
    else:
        return False


def is_same(target, value, index, tolerance):
    """
    this function check label value whether bigger than index or lower than index

    :param target:
    :param value:
    :param index:
    :param tolerance:
    :return:
    """

    if value[1] + tolerance <= float(target[index]['region_s']):
        return 'less'
    elif value[0] - tolerance  >= float(target[index]['region_e']):
        return 'upper'
    else:
	return 'in'


def run(input_file_name, input_labels):
    """
    this is the module for calculation Error. it will run parallel also.
    and this module can be used to regular, for MACS and peakSeq which
    any algorithms return as bed file format.

    :param input_file_name:
        this parameter is file name that result of running MACS
         by chromosome.

    :param input_labels:
        this paramerter is python map about labeled data
         that it is loaded by loadParser.loadLabel.py

    :return: number of incorrect label, rate of incorrect label
        (incorrect label / correct label)
    """
    
    #case of input label size is 0, error num error rate is zero.
    if input_labels is -1:
	return 0, 0

    #load and handle peak files
    if not os.path.exists(input_file_name):
	return 0, 0
    input_file = loadPeak(input_file_name)
    cell_type = input_file_name.split('.')[0]
    cell_type = cell_type.rsplit('_',1)[1]

    if len(input_file) is 0:
	return 0, 0

    error_num, total_label = calculate_error(input_file, input_labels, cell_type)
    #print "error is {error label/ total label}:" + str(error_num) + "/" + str(total_label) + '\n'
    return error_num, total_label
