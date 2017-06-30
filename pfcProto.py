#!/usr/bin/env python
# Time-stamp: < >

import os
import sys
import argparse
import tempfile

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
    if args.tool == "MACS":
        from MACparamLearn import run
	print args
        run( args )

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
