"""this is the module for calculation Error. it will run parallel also.
and this module can be used to regular, for MACS and peakSeq which any algorithms
return as bed file format."""

import random


validation_set = []
test_set = []
input_bed_name = ''
input_label_name = ''



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
    label_table = ['regions', 'peakStat', 'cellTypes']
    chromosome_num = 0
    cell_type = ""

    ### parse the text file to python list
    for peak in peak_labels:
        containor = []
        containor.append(peak.split(':')[0])
        containor.append(peak.split(':')[1].split(' ',2))
        labels.append(containor)

    ### this part will be change to it decided by input name automatically
    print "what chromosome you choose? :: e. g. chrN "
    chromosome_num = raw_input()
    print "what cell type you choose? :: e. g. {tcell, bcell, monocyte,... etc }"
    cell_type = raw_input()

    ### this list will be return value.
    result_labels_list = []

    ### check the condition ( chromosome and cell type ) and change to python map
    for label in labels:
        if label[0] == chromosome_num:
            if ((len(label[1]) is 3 and
                         cell_type in label[1][2]) or
                        'peaks' in label[1]):
                label_map = dict(zip(label_table,label[1]))
                result_labels_list.append(label_map)

    print "%d`s label data is found.\n" % len(result_labels_list)

    if len(result_labels_list) == 0:
        print "there are matched label data. so cannot handle it"
        return -1

    for label in result_labels_list:
        label['regions'] = label['regions'].split('-')
        label['regions'][0] = int(label['regions'][0].replace(',',''))
        label['regions'][1] = int(label['regions'][1].replace(',',''))

    print "Labeled Data List ::::::::::\n" + str(result_labels_list)
    return result_labels_list



def bed_file_load(input_bed, chrom = None):
    """loading bed files and translate to Python Object"""
    bed_file = open(input_bed,'r')
    peak_data = bed_file.readlines()

    peak_table = ['chr','region_s','region_e','peak_name','score']
    peak_labels = []

    for peak in peak_data:
        peak_labels.append(dict(zip(peak_table,peak.split())))

    return peak_labels



def split_label_for_crossValidation(labels, k_fold = 4):
    """split the label list for k-fold crossValidation."""
    valid_labels = []
    test_labels = []

    while len(labels) is not 0:
        if random.random() > 1.0/k_fold:
            valid_labels.append(labels.pop())
        else:
            test_labels.append(labels.pop())

    print "# of test set :: {%d}, # of validation set :: {%d}" % (len(test_labels), len(valid_labels))
    return (test_labels, valid_labels)



def calculate_error(peak_data, labeled_data):
    """calculate actual error by numbering to wrong label"""

    error_num = 0.0
    error_rate = 0.0

    for label in labeled_data:
        if label['peakStat'] == 'peaks':
            print "in peaks"
            if not is_correct_label(peak_data, label['regions'], weak_predict= True) : error_num += 1

        elif label['peakStat'] == 'peakStart' or 'peakEnd':
            print "in peakStart"
            if not is_correct_label(peak_data, label['regions']) : error_num += 1

    error_rate = error_num / len(labeled_data)
    print "incorrect label // correct label ::" + str(error_num) + ":" + str(len(labeled_data))
    return error_rate



def is_correct_label(target, value, similarity = 500, weak_predict = False):
    """this function will find to regions in target bed set by using binary search"""
    """the similarity allow the distance of bed file row between label area as long as own value"""

    correct_num = 0
    index = len(target)/2
    min_index = 0
    max_index = len(target)

    ## if find correct one, return True
    while True:
        correct_ness = is_same(target, value, index, similarity)

        print target[index], value

        #Case 1 : label is "peaks" or "noPeak" and False Negative or False Positive
        #       and "peakStart" or "peakEnd" also.
        if max_index <= min_index + 1:
            print "cannot find correct peak"
            return False

        #Case 2 : label is "peakStart" or "peakEnd" and Correct.
        elif max_index <= min_index + 1 and correct_num == 1:
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



def is_same(target, value, index, similarity):
    """this function check label value whether bigger than index or lower than index"""
    if value[1] + similarity <= float(target[index]['region_s']):
        return 'less'
    elif value[0] - similarity  >= float(target[index]['region_e']):
        return 'upper'
    else:
        return 'in'



def call_error_cal_script(input_bed, validSet):
    """keep call MACS until we find proper parameter"""

    ### load and handle labeled Data
    peak_labels = peak_label_load(validSet)
    peak_labels = parse_peak_labels(peak_labels)

    ## cannot found label about selected area.
    if peak_labels is -1:
        pass

    global test_set
    global validation_set
    test_set, validation_set = split_label_for_crossValidation(peak_labels)

    ### load and handle bed files
    peak_data = bed_file_load("NA_summits.bed")

    print "error is :" + str(calculate_error(peak_data, validation_set))



def run(input_bed, input_labels):
    """it will be runned by protoPFC.py"""
    global input_bed_name
    input_bed_name = input_bed
    global input_label_name
    input_label_name = input_labels

    input_bed = "NA_summits.bed"

    call_error_cal_script(input_bed, input_labels)
