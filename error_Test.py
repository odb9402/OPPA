import sys
import argparse

from oppa.loadParser.loadLabel import run as loadLabel
from oppa.loadParser.parseLabel import run as parseLabel
from oppa.calculateError import run as calculateError

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input",  help="input file "\
                            ":: Format of input file follow this form\n"\
                            " = name_cellType.REF_chrN.bam_peaks.fileformat")
    arg_parser.add_argument("-vs", "--validationSet", help="validation file")

    args = arg_parser.parse_args()

    valid_label , test_label = loadLabel(args.validationSet)
    valid_label = valid_label + test_label

    print "Calculate Score with input file and validation file"

    error_num, label_num = calculateError(args.input, parseLabel(valid_label, args.input))

    result = 1 - (error_num / label_num)

    print "Score of input Data : " + str(result)
    return result

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("i hope you complete. \n")
        sys.exit()
