import sys
import argparse

from oppa.macs.learnMACSparam import run
from oppa.loadParser import loadLabel
from oppa.bamtools import run as bamtools

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i","--input",  help="input file")
    arg_parser.add_argument("-l","--label", help="label file")
    arg_parser.add_argument("-cr", "--control", help="control file")
    arg_parser.add_argument("-q", "--Qval", help="Q value")
    arg_parser.add_argument("-ct", "--callType", help="callType")

    args = arg_parser.parse_args()

    bamtools(args.input)

    label = loadLabel(args.label)

    result = run(args.input, label, args.Qval, args.ct ,args.cr)

    print "error is : " + str(result)
    return result

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("i hope you complete. \n")
        sys.exit()
