import ensemble
import os
import time
from ..loadParser.loadPeak import run as loadpeak


def ensembleMethod(tool_list, score_dict, dir, args):
    """
    this function make connection python with ensemble.cpp
    it call ensemble.Ensembler c++ module with result of each peak detectors,
    and will get back summary data of ensemble method.

    :param tool_list: list of tool already used.

    :param score_dict: score dictionary of learning process.

    :param dir: working directory which result stored.

    :param args: oppa`s command line arguments.

    :return:
    """

    chr_list = score_dict[score_dict.keys()[0]].keys()
    peaks = []
    scores = []

    print len(tool_list)
    for chr in chr_list:
        print dir
        print args
        print chr_list
        print score_dict
        #print tool
        add_peak, add_score = stacking_peaks(dir, args, tool_list, score_dict, chr=chr)

        for peak in add_peak:
            peaks.append(peak)

        for score in add_score:
            scores.append(score)
        ensemble.ensembler(peaks, scores, len(tool_list))
        peaks = []
        score = []
    print peaks, scores

    print len(peaks), len(scores)

    


def stacking_peaks(dir, args, tool_list, score_dict, chr=None):
    """
    this function return < set of peaks , score > from
    each result files of selected tools which like macs.

    :param dir: working directory

    :param args: command line argument from main

    :param chr_list:

    :param score_dict:

    :param tool:

    :return:
    """

    peaks = []
    scores = []
    ref_char = ".REF_"

    #if tool is None:
     #   print "combine error :: tool name is none."
      #  exit()

    for tool in tool_list:
        name_tag = args.input.rsplit(".", 1)[0] + ref_char + chr
        print name_tag

        if "homer" in tool:
            input_name = dir + "/HOMER/" + name_tag + ".bam_peaks.bed"
            waiting_result_file(input_name)
            score = score_dict['homer'][chr]['max_val']

        if "macs" in tool:
            input_name = dir + "/MACS/" + name_tag + ".bam_peaks.broadPeak"
            waiting_result_file(input_name)
            score = score_dict['macs'][chr]['max_val']

        if "spp" in tool:
            input_name = dir + "/SPP/" + name_tag + ".bam_peaks.bed"
            waiting_result_file(input_name)
            score = score_dict['spp'][chr]['max_val']

        if "sicer" in tool:
            input_name = dir + "/SICER/" + name_tag + ".bam_peaks.bed"
            waiting_result_file(input_name)
            score = score_dict['sicer'][chr]['max_val']

        peaks.append(loadpeak(input_name))
        scores.append(score)

    return peaks, scores


def waiting_result_file(input_name):
    """
    This method check check result file is made or not by
    each peak caller. And it have some time limit to prevent
    infinite loop.
    As a result, it is for waiting until result file out.

    :param input_name:

    :return:
    """

    time_limit = 0

    while True:
        if os.path.isfile(input_name) is True:
            break

        if time_limit > 10000:
            print "There is no result file. It over the time limitation."
            exit()

        time.sleep(0.1)
        time_limit += 1
