import time
import os
import glob
import re
from multiprocessing import Process, Manager, cpu_count
import multiprocessing

from ..Helper.tools import parallel_learning
from ..Helper.tools import return_accuracy
from ..optimizeHyper import run as optimizeHyper
from SICER import run as SICER

def learnSICERparam(args, test_set, validation_set, PATH, kry_file=None):
    """

    :param args:
    :param test_set:
    :param validation_set:
    :param PATH:
    :param kry_file:
    :return:
    """

    input_file = args.input
    control = args.control
    chromosome_list = []
    cpNum_files = []
    cpNum_controls = []

    manager = Manager()
    return_dict = manager.dict()

    if not os.path.exists(PATH + '/SICER'):
        os.makedirs(PATH + '/SICER')

    parameters_bounds = {'windowSize': (1.0/12.0 , 1.0)\
                         ,'fragmentSize': (1.0/9.0 , 1.0)\
                         ,'gapSize': (1.0/6.0, 1.0)}

    number_of_init_sample = 2

    if not os.path.exists(PATH+'/SICER/control/'):
        os.makedirs(PATH + '/SICER/control/')

    if kry_file is None:
        for label in validation_set + test_set:
            chromosome_list.append(label.split(':')[0])
        chromosome_list = sorted(list(set(chromosome_list)))
        for chromosome in chromosome_list:
            output_dir = PATH + '/SICER/' + chromosome + '/'
            if not os.path.exists(PATH + '/SICER/' + chromosome):
                os.makedirs(output_dir)
    else:
        cpNum_files = glob.glob(PATH + "/" + input_file.split(".")[0] + ".CP[1-9].bam")
        cpNum_controls = glob.glob(PATH + "/" + control.split(".")[0] + ".CP[1-9].bam")
        str_cpnum_list = []
        for cp in cpNum_files:
            str_cpnum_list.append(re.search("CP[1-9]", cp).group(0))
        for str_cpnum in str_cpnum_list:
            output_dir = PATH + '/SICER/' + str_cpnum + '/'
            if not os.path.exists(PATH + '/SICER/' + str_cpnum):
                os.makedirs(output_dir)


    reference_char = ".REF_"
    bam_name = input_file[:-4]
    cr_bam_name = control[:-4]

    MAX_CORE = cpu_count()
    learning_processes = []


    ###############################################################


    if kry_file is None:
        for chromosome in chromosome_list:
            def wrapper_function(windowSize, fragmentSize, gapSize):
                target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
                cr_target = PATH + '/' + cr_bam_name + reference_char + chromosome + '.bam'
                accuracy = run(target, cr_target, validation_set + test_set \
                               , str(int(windowSize*600.0))\
                               , str(int(fragmentSize*450.0)), str(int(gapSize*6.0)), False, )
                print chromosome, \
                    "windowSize : " + str(int(windowSize*600.0)),\
                    "fragmentSize : " + str(int(fragmentSize*450.0)),\
                    "gapSize : " + str(int(gapSize*6.0)),\
                    "score:" + str(round(accuracy, 4)) + '\n'
                return accuracy

            function = wrapper_function
            learning_process = multiprocessing.Process(target=optimizeHyper, \
                args=(function, parameters_bounds, number_of_init_sample, return_dict, 20, 'ei', chromosome,))

            parallel_learning(MAX_CORE, learning_process, learning_processes)
    else:
        for index in range(len(cpNum_files)):
            cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
            cpNum = int(cpNum_str[2:3])
            def wrapper_function(windowSize, fragmentSize, gapSize):
                accuracy = run(cpNum_files[index], cpNum_controls[index], validation_set + test_set \
                               , str(int(windowSize*600.0))\
                               , str(int(fragmentSize*450.0)), str(int(gapSize*6.0)), False, kry_file, )
                print cpNum_str, \
                    "windowSize : " + str(int(windowSize*600.0)),\
                    "fragmentSize : " + str(int(fragmentSize*450.0)),\
                    "gapSize : " + str(int(gapSize*6.0)),\
                    "score:" + str(round(accuracy, 4)) + '\n'
                return accuracy
            function = wrapper_function
            learning_process = multiprocessing.Process(target=optimizeHyper,\
                args=(function, parameters_bounds, number_of_init_sample, return_dict, 20, 'ei', cpNum,))

            parallel_learning(MAX_CORE, learning_process, learning_processes)

    for proc in learning_processes:
        proc.join()

    print "finish learning parameter of SICER ! "
    print "Running SICER with learned parameter . . . . . . . . . . . . . . ."

    learning_processes = []

    if kry_file is None:
        for chromosome in chromosome_list:
            parameters = return_dict[chromosome]['max_params']
            target = bam_name + reference_char + chromosome + '.bam'
            windowSize = parameters['windowSize']
            fragmentSize = parameters['fragmentSize']
            gapSize = parameters['gapSize']

            learning_process = multiprocessing.Process(target=run,\
                args=( PATH + '/' + target, PATH + '/' + cr_bam_name + reference_char + chromosome + '.bam'\
                    , validation_set + test_set, str(int(windowSize*600.0)), str(int(fragmentSize*450.0)), str(int(gapSize*6.0)), True,))

            parallel_learning(MAX_CORE, learning_process, learning_processes)

    else:
        for index in range(len(cpNum_files)):
            cpNum_str = re.search("CP[1-9]", cpNum_files[index]).group(0)
            cpNum = int(cpNum_str[2:3])

            parameters = return_dict[cpNum]['max_params']
            windowSize = parameters['windowSize']
            fragmentSize = parameters['fragmentSize']
            gapSize = parameters['gapSize']

            learning_process = multiprocessing.Process(target=run,\
                args=(cpNum_files[index], cpNum_controls[index], validation_set + test_set, str(int(windowSize*600.0)),\
                    str(int(fragmentSize*450.0)), str(int(gapSize*6.0)), True, kry_file,))

            parallel_learning(MAX_CORE, learning_process, learning_processes)

    for proc in learning_processes:
        proc.join()

    return return_dict


def run(input_file, control, valid_set, windowSize='200', fragSize='150', gapSize='3', final=False, kry_file=None):
    """

    :param input_file:
    :param control:
    :param valid_set:
    :param final:
    :param kry_file:

    :return: accuracy rate about a result file.
    """
    result_file = input_file[:-4] + ".bam_peaks.bed"
    result_file = result_file.rsplit('/',1)[0] + '/SICER/' + result_file.rsplit('/',1)[1]

    SICER(input_file, control, windowSize, fragSize, gapSize, kry_file)

    return return_accuracy(final, kry_file, result_file, valid_set)


