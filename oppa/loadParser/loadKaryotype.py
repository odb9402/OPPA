import csv

def load_kry_file(file_name, chr_list):
	"""

	:param file_name:
	:param chr_list:
	:return:
	"""
	kry_list = []
	f = open(file_name,'r')
	csvReader = csv.reader(f)

	for row in csvReader:
		if 'chr' in row[0]:
			row[3] = filter(str.isdigit,row[3])		# Extract copy number
			row[1] = int(row[1])
			row[2] = int(row[2])
			row[3] = int(row[3])
			row[4] = int(row[4])

			kry_list.append(row)

	f.close()
	
	kry_list.sort()

	table = ['chr','start','end','cpNum','size']

	kry_dict_list = []

	for kry in kry_list:
		kry_dict = dict(zip(table, kry))
		kry_dict_list.append(kry_dict)
	
	return kry_dict_list

def run(file_name, chr_list):
	"""

	:param file_name:
	:param chr_list:
	:return:
	"""
	kry_types = load_kry_file(file_name, chr_list)
	return kry_types
