"""to load the file of error rate wrote."""
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
    label_table = ['regions', 'peakStat', 'cellType']
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

    ### check the condition ( chromosome ) and change to python map
    for label in labels:
        if label[0] == chromosome_num:
            label_map = dict(zip(label_table, label[1]))
            result_labels_list.append(label_map)


    print "%d`s label data is found.\n" % len(result_labels_list)

    if len(result_labels_list) == 0:
        print "there are matched label data. so cannot handle it"
        return -1

    for label in result_labels_list:
        if len(label) == 2 or not cell_type in label['cellType']:
            label['peakStat'] = 'noPeak'

    for label in result_labels_list:
        label['regions'] = label['regions'].split('-')
        label['regions'][0] = int(label['regions'][0].replace(',',''))
        label['regions'][1] = int(label['regions'][1].replace(',',''))

    print "Labeled Data List ::::::::::\n" + str(result_labels_list)

    return result_labels_list



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



def run(validSet):
    ### load and handle labeled Data
    peak_labels = peak_label_load(validSet)
    peak_labels = parse_peak_labels(peak_labels)

    ## cannot found label about selected area.
    if peak_labels is -1:
        pass

    global test_set
    global validation_set
    test_set, validation_set = split_label_for_crossValidation(peak_labels)
    return test_set, validation_set