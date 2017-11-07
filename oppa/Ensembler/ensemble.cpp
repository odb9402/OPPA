#include <Python.h>
#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>

#define threshhold 0.5
#define allowable_difference 200
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

   char* chr;
   char* chr_start;
   char* chr_end;
   char* signal;
   char* q_value;
   char* score;
   char* error_rate;

   int file_num = 2;

   ofstream fout("result.narrowPeak",ios::app);

   //////// Python Object to C++ Local variable /////////
   if(!PyArg_ParseTuple(args, "O!O!i",&PyList_Type, &peaks_data, &PyList_Type, &error_data, &file_num))
      return NULL;

   PyObject *peak_containor[file_num];
   PyObject *dict_containor = (PyObject*)PyDict_New();
   double error_containor[file_num];

   std::vector<peak> peak_vec[file_num];
   peak* peak_element;

   for ( int i = 0; i < file_num; i++){
      peak_containor[i] = (PyObject*)PyList_New(0);
      peak_containor[i] = PyList_GetItem(peaks_data,i);
      error_containor[i] = PyFloat_AsDouble(PyList_GetItem(error_data,i));
   }

   file_num = 3;

   for ( int i = 0; i < file_num; i++){
      cout << "------------" << endl << i<<endl;

      for ( int j = 0 ; j < PyList_Size(peak_containor[i]) ; j++){
         dict_containor = PyList_GetItem(peak_containor[i], j);
         PyArg_Parse(PyDict_GetItemString(dict_containor,"region_s"), "s", &chr_start);
         PyArg_Parse(PyDict_GetItemString(dict_containor,"region_e"), "s", &chr_end);
         PyArg_Parse(PyDict_GetItemString(dict_containor,"chr"), "s", &chr);

         cout <<chr_start <<" ";

         peak_element = new peak;
         peak_element->chr = chr;
         peak_element->chr_start = atoi(chr_start);
         peak_element->chr_end = atoi(chr_end);
         peak_element->error_rate = error_containor[i];
         peak_vec[i].push_back(*peak_element);
      }
   }

   cout <<"==============================================="<<endl;
   vector<peak>::iterator it[file_num];
   double error_sum= 0;

   for(int i=0; i <file_num; i++){
      it[i] = peak_vec[i].begin();
      error_sum +=error_containor[i];
   }

   cout <<file_num <<endl;

   double smallest_value, pct;
   double cnt=0;
   int chr_check = 0;
   char current_chr = it[0]->chr[3];

   cout <<current_chr <<endl;
   cout << it[1]->chr[3];

   smallest_value = it[0]->chr_start < it[1]->chr_start? it[0]->chr_start : it[1]->chr_start; //*********************************************

   for(int i=2; i < file_num;i++){
      if(smallest_value > it[i]->chr_start)
         smallest_value = it[i]->chr_start;

   }

   while(1){

      for(int i=0; i <file_num; i++){
         if(abs(smallest_value - it[i]->chr_start) <allowable_difference){
            cnt += error_containor[i] ;
         }
      }

      pct = cnt /error_sum; // how many files are matched

      if(pct > threshhold){
         cout <<"=========="<<file_num << " of " <<cnt<<" files are match"<<"=========="<<endl;

	  fout<< it[0]->chr<<"	";
	  cout<< it[0]->chr <<endl;

	  int avg_start =0;
	  int avg_end =0;

	  for(int i=0;i<file_num; i++){
         cout << it[i]->chr_start<<endl;
	     avg_start += it[i]->chr_start;
	     avg_end += it[i]->chr_end;
      }

	  fout<< avg_start/file_num<<"	";
	  fout<< avg_end/file_num<<endl;
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
         for(int i=0; i< file_num; i++){
            if(it[i]->chr[3]=='D'){
		       fout.close();
               return Py_BuildValue("i",1);
	        }

            while(it[i]->chr[3] == current_chr){
               it[i]++;
	           if(it[i] == peak_vec[i].end()){
		          fout.close();
		          return Py_BuildValue("i",1);
		       }
            }
         }
         current_chr = it[0]->chr[3];
	     cout <<endl<<"==================next chr====================="<<endl<<endl;
      }

      smallest_value = 2100000000;

      for(int i=0; i <file_num; i++){
         if(it[i]->chr[3] == current_chr && it[i]->chr_start < smallest_value)
            smallest_value = it[i]->chr_start;
      }

   }

   //////// C++ value to Python Object /////////////////
   fout.close();
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