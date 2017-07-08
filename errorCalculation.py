"""this is the module for calculation Error. it will run parallel also.
and this module can be used to regular, for MACS and peakSeq which any algorithms
return as bed file format."""

import random
from peakLoad import run as peakLoad



def calculate_error(peak_data, labeled_data):
    """calculate actual error by numbering to wrong label"""

    error_num = 0.0
    error_rate = 0.0
    for label in labeled_data:
        print label['peakStat']
        if label['peakStat'] == 'peaks':
            if not is_peak(peak_data, label['regions'], weak_predict= True) : error_num += 1

        elif label['peakStat'] == ('peakStart' or 'peakEnd'):
            if not is_peak(peak_data, label['regions']) : error_num += 1

        else:
            if not is_noPeak(peak_data, label['regions']) : error_num += 1

    error_rate = error_num / len(labeled_data)
    print "incorrect label // correct label ::" + str(error_num) + ":" + str(len(labeled_data))
    return error_rate



def is_peak(target, value, tolerance = 0, weak_predict = False):
    """this function will find to regions in target bed set by using binary search"""
    """the similarity allow the distance of bed file row between label area as long as own value"""

    correct_num = 0
    index = len(target)/2
    min_index = 0
    max_index = len(target)

    ## if find correct one, return True
    while True:
        correct_ness = is_same(target, value, index, tolerance)

        #print target[index], value

        #Case 1 : label is "peaks" or "noPeak" and False Negative or False Positive
        #       and "peakStart" or "peakEnd" also.
        if max_index <= min_index + 1:
            print "cannot find correct peak"
            return False

        #Case 2 : label is "peakStart" or "peakEnd" and Correct.
        elif max_index <= min_index + 1 and correct_num == 1:
            print "find only one peak"
            return True

        #Case 3 : label is "peakStart" or "peakEnd" and False Negative
        elif max_index <= min_index + 1 and correct_num > 1:
            return False


        if correct_ness is 'less':
            max_index = index
            index = (min_index + index) / 2
        elif correct_ness is 'upper':
            min_index = index
            index = (max_index + index) / 2
        ##find correct regions
        else:
            ### if label is "peaks", correct regions can be bigger than 2.
            ### but "peakStart" or "peakEnd" are not they must exist only 1 correct regions.

            #Case 4 : label is "peaks" or "noPeak" and Correct.
            if (weak_predict is True):
                print "find correct peak"
                return True

            #Case 5 : label is "peakStart" or "peakEnd" and False Positive
            elif (weak_predict is False) and correct_num > 1:
                print "there are too many peak."
                return False

            else:
                print "find one"
                correct_num += 1
                index = len(target) / 2
                min_index = 0
                max_index = len(target)



def is_noPeak(target, value, tolerance = 0):

    region_min = value[0]
    region_max = value[1]

    #for find start regions, delete end regions
    value[1] = value[0]

    correct_num = 0
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
        ##find correct regions
        else:
            break

        if abs(float(target[index]['region_e']) - region_min) < 5 * steps or steps > 1000:
            break
        steps += 1

    if index + 1 == len(target) or\
            float(target[index + 1]['region_s']) + tolerance > region_max:
        print "correct noPeak"
        return True
    else:
        print "false Negative noPeak"
        return False



def is_same(target, value, index, tolerance):
    """this function check label value whether bigger than index or lower than index"""
    if value[1] + tolerance <= float(target[index]['region_s']):
        return 'less'
    elif value[0] - tolerance  >= float(target[index]['region_e']):
        return 'upper'
    else:
        return 'in'



def call_error_cal_script(input_file_name, input_valid):
    """keep call MACS until we find proper parameter"""

    ### load and handle peak files
    input_file = peakLoad(input_file_name)

    print "error is :" + str(calculate_error(input_file, input_valid))



def run(input_file_name, input_labels):
    """it will be runned by protoPFC.py"""
    call_error_cal_script(input_file_name, input_labels)
