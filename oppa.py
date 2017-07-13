#!/usr/bin/env python
# Time-stamp: < >
import time
from datetime import timedelta
import sys
import argparse
from oppa.loadParser import loadLabel

def main():
    """The main function for pipeline"""

    # setting Script Option.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-t","--tool",  help="what tool you use. : { MACS , Basset , peakSeg }")
    arg_parser.add_argument("-i","--input", help="what file you input.")
    arg_parser.add_argument("-cr","--control", help="it is control-Bam file for MACS")
    arg_parser.add_argument("-f","--format", help="input file format for : { MACS , ")
    arg_parser.add_argument("-q","--Qval", help="it is parameter that will be learned and it mean\n"
                                                "significance value in Statical solutions it is only for"
                                                ": {MACS ")
    arg_parser.add_argument("-vs","--validSet", help="validation set it is labeled. used for : { MACS , ")
    arg_parser.add_argument("-ct","--callType", help="decide peak call type either broad or narrow. used for : {MACS ")

    args = arg_parser.parse_args()

    if args.Qval == None:
        args.Qval = '0.05'

    validation_set, test_set = loadLabel(args.valid)

    # Run each other process by what tools they need.
    # and may be we can each chromosome run in
    if args.tool == "MACS":
        from oppa.macs.learnMACSparam import learnMACSparam
        from oppa.bamtools import run as bamtools
        start_time = time.time()

        #running bamtools to split the bam file
        print "Execute bamtools . . . : split bam file by chromosome "
        #bamtools( args.input )
        elapsed_time_secs = time.time() - start_time
        print "Execution _ bamtools : %s" % timedelta(seconds=round(elapsed_time_secs))

        print "Execute MACS . . . : each chromosome "
        start_time = time.time()
        learnMACSparam(args, validation_set, test_set)
        elapsed_time_secs = time.time() - start_time
        print "Execution _ learning parameter : %s" % timedelta(seconds=round(elapsed_time_secs))


    elif args.tool == "PeakSeg":
        pass

    elif args.tool == "Basset":
        pass

    else:
        print "the tool %s is not support.",args.tool


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("i hope you complete. \n")
        sys.exit()
