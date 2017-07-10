"""to load the file of error rate wrote."""
import random


def parse_chr_celltype():
    pass


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

    return result_labels_list



def run(validSet, file_name):
    ### load and handle labeled Data
    peak_labels = parse_peak_labels(validSet)

    ## cannot found label about selected area.
    if peak_labels is -1:
        return -1

    return peak_labels