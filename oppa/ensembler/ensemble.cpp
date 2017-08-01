#include <Python.h>
#include <vector>
#include <iostream>
#include <cmath>

#define file_num 3
#define threshhold 0.6
#define allowable_difference 20
using namespace std;
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

   PyObject *peak_containor[file_num];
   PyObject *dict_containor = (PyObject*)PyDict_New();

   double error_containor[file_num];
   std::vector<peak> peak_vec[file_num];
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
   for ( int i = 0; i < file_num; i++){
      peak_containor[i] = (PyObject*)PyList_New(0);
      peak_containor[i] = PyList_GetItem(peaks_data,i);
      error_containor[i] = PyFloat_AsDouble(PyList_GetItem(error_data,i));
   }
   for ( int i = 0; i < file_num; i++){
           
      for ( int j = 0 ; j < PyList_Size(peak_containor[i]) ; j++){
         dict_containor = PyList_GetItem(peak_containor[i], j);
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
         peak_element->error_rate = error_containor[i];
         
         peak_vec[i].push_back(*peak_element);
        // printf("now parse %d`s of peak , signal = %f\n", peak_vec[i].size(), peak_element->signal);
      }
   }

   cout <<"==============================================="<<endl;
   vector<peak>::iterator it[file_num];

   for(int i=0; i <file_num; i++)
      it[i] = peak_vec[i].begin();

   double smallest_value, pct;
   int cnt=0;
   int chr_check = 0;
   char current_chr = it[0]->chr[3];

   cout <<it[0]->chr<< " " <<it[1]->chr<<endl;
   smallest_value = it[0]->chr_start < it[1]->chr_start? it[0]->chr_start : it[1]->chr_start; //*********************************************
   for(int i=2; i < file_num;i++){
      if(smallest_value > it[i]->chr_start)
         smallest_value = it[i]->chr_start;
   }
   while(1){
      for(int i=0; i <file_num; i++){
         if(abs(smallest_value - it[i]->chr_start) <allowable_difference){
            cnt++;
         }
      }

      pct = cnt / file_num; // how many files are matched

      if(pct > threshhold){
         cout <<"=========="<<file_num << " of " <<cnt<<" files are match"<<"=========="<<endl;
cout<< it[0]->chr <<endl; 
for(int i=0;i<file_num; i++){
         cout << it[i]->chr_start<<endl;
         }
         cout <<"===================="<<endl;

      }
      cnt = 0;
      for(int i=0; i <file_num; i++){
         if(abs(smallest_value - it[i]->chr_start) <allowable_difference && current_chr == it[i]->chr[3] ){// move to next peak element
            it[i]++;
            if(it[i]==peak_vec[i].end()){
               it[i]--;
               it[i]->chr[3] = 'D';// prevent vector out of idx 
            }
         }
      }
      chr_check=0;
      for(int i=0; i <file_num; i++){
         if(it[i]!= peak_vec[i].end() && current_chr == it[i]->chr[3])
            chr_check++; //should i move to next chromosome?
      }
      if(double(chr_check) / double(file_num) < threshhold){
cout <<" -----------------=======================================";
         for(int i=0; i< file_num; i++){
            if(it[i]->chr[3]=='D')
                 return Py_BuildValue("i",1);
            while(it[i]->chr[3] == current_chr){
               it[i]++;
            }
         }
         current_chr = it[0]->chr[3];
      }
      smallest_value = 2100000000;
      for(int i=0; i <file_num; i++){
         if(it[i]->chr[3] == current_chr && it[i]->chr_start < smallest_value)
            smallest_value = it[i]->chr_start;
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
