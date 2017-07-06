#!/usr/bin/env python
# Time-stamp: < >

import os
import sys
import argparse
import tempfile
from multiprocessing import Process

def main():
    """The main function for pipeline"""

    ## Setting Script Option.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-t","--tool",  help="what tool you use. : { MACS , Basset }")
    arg_parser.add_argument("-i","--input", help="what file you input.")
    arg_parser.add_argument("-cr","--control", help="it is control-Bam file for MACS")
    arg_parser.add_argument("-f","--format", help="input file format for : { MACS , ")
    arg_parser.add_argument("-q","--Qval", help="it is parameter that will be learned and it mean\n"
                                                "significance value in Statical solutions it is only for"
                                                ": {MACS ")
    arg_parser.add_argument("-vs","--validSet", help="validation set it is labeled. used for : { MACS , ")

    args = arg_parser.parse_args()

    ## Run each other process by what tools they need.
    ## and may be we can each chromosome run in 
    if args.tool == "MACS":
        import MACparamLearn
        import bamtools
        #bamtools.run ( args.input )

        MACparamLearn.run(args)


    elif args.tool == "PeakSeg":
        pass

    elif args.tool == "Basset":
        pass

    else:
        print "the tool %s is not support.",args.tool


def run_in_parallel(*functions):
    """this is function for parallelize Some tools or functions may be by chromosome."""
    proc = []
    for fn in functions:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("i hope you complete. \n")
        sys.exit()
