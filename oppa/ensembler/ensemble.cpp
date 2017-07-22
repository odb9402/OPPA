#include <Python.h>
#include <vector>

struct peak{
	char* chr;
	int chr_start;
	int chr_end;
	float score;
	float signal;
	float q_value;
};


static PyObject *
ens_main(PyObject *self, PyObject *args){

	PyObject *peaks_data = (PyObject*)PyList_New(0);	
	PyObject *error_data = (PyObject*)PyList_New(0);

	PyObject *peak_containor = (PyObject*)PyList_New(0);
	PyObject *dict_containor = (PyObject*)PyDict_New();

	std::vector<peak> peak_vec;
	peak* peak_element;

	char* chr;
	char* chr_start;
	char* chr_end;
	char* signal;
	char* q_value;
	char* score;

	//////// Python Object to C++ Local variable /////////
	if(!PyArg_ParseTuple(args, "O!O", &PyList_Type, &peaks_data, &PyList_Type, &error_data))
		return NULL;

	for ( int i = 0; i < PyList_Size(peaks_data); i++){
		printf("%d th output file process::::::\n" , i);
		peak_containor = PyList_GetItem(peaks_data,i);

		for ( int j = 0 ; j < PyList_Size(peak_containor) ; j++){
			dict_containor = PyList_GetItem(peak_containor, j);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"region_s"), "s", &chr_start);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"region_e"), "s", &chr_end);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"chr"), "s", &chr);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"score"), "s", &score);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"signalValue"), "s", &signal);
			PyArg_Parse(PyDict_GetItemString(dict_containor,"qValue"),"s",&q_value);
			
			peak_element = new peak;
			peak_element->chr = chr;
			peak_element->chr_start = atoi(chr_start);
			peak_element->chr_end = atoi(chr_end);
			peak_element->score = atof(score);
			peak_element->signal = atof(signal);
			peak_element->q_value = atof(q_value);
			
			peak_vec.push_back(*peak_element);
			printf("now parse %d`s of peak , signal = %f\n", peak_vec.size(), peak_element->signal);
		}
	}
	//////// C++ value to Python Object /////////////////
	return Py_BuildValue("i",1);
}

static PyMethodDef ensembleMethods[] = {
	{"ensembler", ens_main, METH_VARARGS, "main flow of ensembler."},
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initensemble(void){
	(void) Py_InitModule("ensemble",ensembleMethods);
}


int main(int argc, char *argv[]){
	Py_SetProgramName(argv[0]);
	Py_Initialize();
	initensemble();
	return 0;
}
