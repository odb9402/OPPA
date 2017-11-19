import time
import os
import glob
from multiprocessing import Process, Manager, cpu_count

import multiprocessing

from ..optimizeHyper import run as optimizeHyper
from ..calculateError import run as calculateError
from ..loadParser.parseLabel import run as parseLabel
from SICER import run as SICER

def learnSICERparam(args, test_set, validation_set, PATH, copyNums=None):
    """


    :param args:

    :param test_set:

    :param validation_set:

    :param PATH:

    :return:
    """

    input_file = args.input
    control = args.control

    manager = Manager()
    return_dict = manager.dict()

    if not os.path.exists(PATH + '/SICER'):
        os.makedirs(PATH + '/SICER')

    parameters_bounds = {'windowSize': (1.0/12.0 , 1.0)\
                         ,'fragmentSize': (1.0/9.0 , 1.0)\
                         ,'gapSize': (1.0/6.0, 1.0)}
    number_of_init_sample = 2

    if copyNums is None:
        chromosome_list = []
        for label in validation_set + test_set:
            chromosome_list.append(label.split(':')[0])
        chromosome_list = sorted(list(set(chromosome_list)))

    reference_char = ".REF_"
    bam_name = input_file[:-4]
    cr_bam_name = control[:-4]

    MAX_CORE = cpu_count()
    learning_processes = []

    ## SICER need some preprocess which convert bamfile to bedfiles
    if not os.path.exists(PATH+'/SICER/control/'):
        os.makedirs(PATH + '/SICER/control/')

    for chromosome in chromosome_list:
        output_dir = PATH + '/SICER/' + chromosome + '/'
        if not os.path.exists(PATH + '/SICER/' + chromosome):
            os.makedirs(output_dir)
    ###############################################################



    for chromosome in chromosome_list:
        def wrapper_function(windowSize, fragmentSize, gapSize):
            target = PATH + '/' + bam_name + reference_char + chromosome + '.bam'
            cr_target = PATH + '/' + cr_bam_name + reference_char + chromosome + '.bam'
            accuracy = run(target, cr_target, validation_set + test_set \
                           , str(int(windowSize*600.0))\
                           , str(int(fragmentSize*450.0)), str(int(gapSize*6.0)))
            print chromosome, \
                "windowSize : " + str(int(windowSize*600.0)),\
                "fragmentSize : " + str(int(fragmentSize*450.0)),\
                "gapSize : " + str(int(gapSize*6.0)),\
                "score:" + str(round(accuracy, 4)) + '\n'
            return accuracy

        function = wrapper_function
        learning_process = multiprocessing.Process(target=optimizeHyper, args=(function, \
                                                                               parameters_bounds, number_of_init_sample,
                                                                               return_dict, 20, 'ei', chromosome,))

        if len(learning_processes) < MAX_CORE - 1:
            learning_processes.append(learning_process)
            learning_process.start()
        else:
            keep_wait = True
            while True:
                time.sleep(0.1)
                if not (keep_wait is True):
                    break
                else:
                    for process in reversed(learning_processes):
                        if process.is_alive() is False:
                            learning_processes.remove(process)
                            learning_processes.append(learning_process)
                            learning_process.start()
                            keep_wait = False
                            break

    for proc in learning_processes:
        proc.join()

    print "finish learning parameter of SICER ! "
    print "Running SICER with learned parameter . . . . . . . . . . . . . . ."

    for chromosome in chromosome_list:
        parameters = return_dict[chromosome]['max_params']
        target = bam_name + reference_char + chromosome + '.bam'
        windowSize = parameters['windowSize']
        fragmentSize = parameters['fragmentSize']
        gapSize = parameters['gapSize']

        learning_processes = []

        learning_process = multiprocessing.Process(target=run, args=( \
            PATH + '/' + target, PATH + '/' + cr_bam_name + reference_char + chromosome + '.bam'\
                , validation_set + test_set, str(int(windowSize*600.0)),\
                str(int(fragmentSize*450.0)), str(int(gapSize*6.0)), True,))

        print PATH+'/'+target
        print control

        if len(learning_processes) < MAX_CORE - 1:
            learning_processes.append(learning_process)
            learning_process.start()
        else:
            keep_wait = True
            while True:
                time.sleep(0.1)
                if not (keep_wait is True):
                    break
                else:
                    for process in reversed(learning_processes):
                        if process.is_alive() is False:
                            learning_processes.remove(process)
                            learning_processes.append(learning_process)
                            learning_process.start()
                            keep_wait = False
                            break

    for proc in learning_processes:
        proc.join()

    return return_dict


def run(input_file, control, valid_set, windowSize='200', fragSize='150', gapSize='3', final=False):

    result_file = input_file[:-4] + ".bam_peaks.bed"
    result_file = result_file.rsplit('/',1)[0] + '/SICER/' + result_file.rsplit('/',1)[1]

    process = SICER(input_file, control, windowSize, fragSize, gapSize)

    """ Finding result file which getting out recently.
    This process use glob which for pattern matching about
    file system, and we check writing time among them. """

    if not valid_set:
        print "there are no matched validation set :p\n"
        exit()

    else:
        error_num, label_num = calculateError(result_file, parseLabel(valid_set, result_file))

        if os.path.isfile(result_file) and (not final):
            os.remove(result_file)
        elif final:
            print result_file + " is stored."
        else:
            print "there is no result file.."

    if label_num is 0:
        return 0.0

    if final:
        print "Test Score ::" + str(1 - error_num / label_num)

    return (1 - error_num / label_num)


