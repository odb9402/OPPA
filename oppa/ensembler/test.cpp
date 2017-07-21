#include <Python.h>

static PyObject *

ens_main(PyObject *self, PyObject *args){
	char *str;
	int len;
	
	//////// Python Object to C++ Local variable /////////
	if(!PyArg_ParseTuple(args, "items", &str))
		return NULL;
	
	len = strlen(str);

	//////// C++ value to Python Object /////////////////
	return Py_BuildValue("i",len);
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
