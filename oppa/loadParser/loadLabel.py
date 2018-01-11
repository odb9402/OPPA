import random

def peak_label_load(validSet):
	"""loading Validation Set Files and translate to Python Object."""
	valid_file = open(validSet, 'r')
	peak_data = valid_file.readlines()
	peak_labels = []

	for peak in peak_data:
		if peak == "\r\n":
			peak_data.remove(peak)
    
	for peak in peak_data:
		if '#' not in peak and 'chr' in peak:
			peak = peak.rstrip('\r\n')
			peak_labels.append(peak)
	valid_file.close()

	peak_labels = sort_by_region(peak_labels)
	return peak_labels


def split_label_for_crossValidation(labels, k_fold = 3):
	"""split the label list for k-fold crossValidation."""
	test_labels = []
	test_num = len(labels) / k_fold

	for i in range(test_num):
		test_labels.append(labels.pop(random.randint(0,len(labels) - 1)))

	valid_labels = labels

	return (test_labels, valid_labels)


def sort_by_region(valid_list):
	valid_list.sort()
	return valid_list


def run(valid_file_name):
	return split_label_for_crossValidation(peak_label_load(valid_file_name))
