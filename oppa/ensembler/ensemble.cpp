#include <Python.h>
#include <vector>

struct peak{
   char* chr;
   int chr_start;
   int chr_end;
   float score;
   float signal;
   float q_value;
   float error_rate;
};


static PyObject *
ens_main(PyObject *self, PyObject *args){

   PyObject *peaks_data = (PyObject*)PyList_New(0);   
   PyObject *error_data = (PyObject*)PyList_New(0);

   PyObject *mac_containor = (PyObject*)PyList_New(0);
   PyObject *spp_containor = (PyObject*)PyList_New(0);
   PyObject *dict_containor = (PyObject*)PyDict_New();

   double mac_error_containor,spp_error_containor;
   std::vector<peak> mac_vec;
std::vector<peak> spp_vec;
   peak* peak_element;

   char* chr;
   char* chr_start;
   char* chr_end;
   char* signal;
   char* q_value;
   char* score;
   char* error_rate;

   //////// Python Object to C++ Local variable /////////
   if(!PyArg_ParseTuple(args, "O!O!",&PyList_Type,&peaks_data, &PyList_Type, &error_data))
      return NULL;

  
   mac_containor = PyList_GetItem(peaks_data,0);
   mac_error_containor = PyFloat_AsDouble(PyList_GetItem(error_data,0));

   spp_containor = PyList_GetItem(peaks_data,1);
   spp_error_containor = PyFloat_AsDouble(PyList_GetItem(error_data,1));
      
//-----------------------MAC--------------------------
   for ( int j = 0 ; j < PyList_Size(mac_containor) ; j++){
      dict_containor = PyList_GetItem(mac_containor, j);
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
      peak_element->error_rate = mac_error_containor;
         
      mac_vec.push_back(*peak_element);
      printf("now parse %d`s of peak , signal = %f\n", mac_vec.size(), peak_element->signal);
   }
//----------------------------mac-end spp start-----------------------------
   for ( int j = 0 ; j < PyList_Size(spp_containor) ; j++){
      dict_containor = PyList_GetItem(spp_containor, j);
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
      peak_element->error_rate =spp_error_containor;
         
      spp_vec.push_back(*peak_element);
      printf("now parse %d`s of peak , signal = %f\n", spp_vec.size(), peak_element->signal);
   }
// -------------------------------spp-end=-----------------------
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
