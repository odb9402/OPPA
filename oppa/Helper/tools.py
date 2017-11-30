import os
import time
from ..calculateError import run as calculateError
from ..loadParser.parseLabel import run as parseLabel
from ..loadParser.loadPeak import run as loadPeak

def parallel_learning(MAX_CORE, learning_process, learning_processes):
    """

    :param MAX_CORE:
    :param learning_process:
    :param learning_processes:
    :return:
    """
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


def return_accuracy(final, kry_file, result_file, valid_set):
    """

    :param final:
    :param kry_file:
    :param result_file:
    :param valid_set:
    :return:
    """

    if not valid_set:
        print "there are no matched validation set :p\n"
        exit()
    else:
        if not os.path.exists(result_file):
            return 0, 0
        peaks = loadPeak(result_file)

        if kry_file is None:
            error_num, label_num = calculateError(peaks, parseLabel(valid_set, result_file))
        else:
            error_num, label_num = 0, 0

            peaks_by_chr = []
            containor = []
            for index in range(len(peaks)):
                if not (index + 1 == len(peaks)):
                    if peaks[index]['chr'] != peaks[index + 1]['chr']:
                        containor.append(peaks[index])
                        peaks_by_chr.append(containor)
                        containor = []
                    else:
                        containor.append(peaks[index])
                else:
                    peaks_by_chr.append(containor)

            for peak_by_chr in peaks_by_chr:
                if len(peak_by_chr) > 0:
                    chromosome = peak_by_chr[0]['chr']
                    print chromosome + " ====================== "
                    temp_error, temp_label = calculateError(peak_by_chr, \
                                                            parseLabel(valid_set, result_file,
                                                                       input_chromosome=chromosome,
                                                                       cpNum_file_name=kry_file))
                    error_num += temp_error
                    label_num += temp_label
                    print "============================\n"

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