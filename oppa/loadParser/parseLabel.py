from loadKaryotype import run as loadKaryotype

def parse_cellType(file_name):
    """
    Parsing file_name and extracting cell-type , chromosome
    input file must be EXPERIMENT_AREA_CELL-TYPE.bam so bamtools create
    EXPERIMENT_AREA_CELL-TYPE.REF_chrN.PEAK

    :param file_name:

    :return: cell_type
    """
    return file_name.split('.')[0].rsplit('_')[1]


def parse_chr(file_name):
    """
    Parsing file_name and extracting cell-type , chromosome
    input file must be EXPERIMENT_AREA_CELL-TYPE.bam so bamtools create
    EXPERIMENT_AREA_CELL-TYPE.REF_chrN.PEAK

    :param file_name:

    :return: chromosome
    """

    file_name = file_name.rsplit('.',1)[0]

    file_name = file_name.rsplit('.',1)[0]
    file_name = file_name.rsplit('_',1)
    chromosome = file_name[1]

    return chromosome


def parse_peak_labels(peak_labels, chromosome_num, cell_type, cpNum_data=None):
    """

    :param peak_labels:
    :param chromosome_num:
    :param cell_type:
    :param cpNum_data:
    :return:
    """

    labels = []
    if cpNum_data is None:
        label_table = ['regions', 'peakStat', 'cellType']
    else:
        label_table = ['regions', 'peakStat', 'cellType']#, 'cpNum']

    #parse the text file to python list
    for peak in peak_labels:
        containor = []
        containor.append(peak.split(':')[0])
        containor.append(peak.split(':')[1].split(' ',2))
        labels.append(containor)

    if not (cpNum_data is None):
        pass
        # mark cpnum

    #this list will be return value.
    result_labels_list = []

    #check the condition ( chromosome ) and change to python map
    for label in labels:
        if label[0] == chromosome_num:
            label_map = dict(zip(label_table, label[1]))
            result_labels_list.append(label_map)


    #print "%d`s label data is found.i" % len(result_labels_list)

    if len(result_labels_list) == 0:
        #print "there are matched label data. so cannot handle it"
        return -1

    for label in result_labels_list:
        if len(label) == 2 or not cell_type.lower() in label['cellType'].lower():
            label['peakStat'] = 'noPeak'

    for label in result_labels_list:
        label['regions'] = label['regions'].split('-')
        label['regions'][0] = int(label['regions'][0].replace(',',''))
        label['regions'][1] = int(label['regions'][1].replace(',',''))

    return result_labels_list


def run(validSet, file_name, input_chromosome = None, input_cellType = None, cpNum_file_name = None):
    """

    :param validSet:
    :param file_name:
    :param input_chromosome:
    :param input_cellType:
    :return:
    """

    if input_chromosome is None:
        chromosome = parse_chr(file_name)
    else:
        chromosome = input_chromosome

    if input_cellType is None:
        cellType = parse_cellType(file_name)
    else:
        cellType = input_cellType

    if not (cpNum_file_name is None):
        cpNum_data = loadKaryotype(cpNum_file_name, [input_chromosome])
        print cpNum_data
    else:
        cpNum_data = None

    peak_labels = parse_peak_labels(validSet, chromosome, cellType, cpNum_data)

    # cannot found label about selected area.
    if peak_labels is -1:
        return -1

    return peak_labels
