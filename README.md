
OPPA
======
Optimize Parameter in Peak detection Algorithm by bayesian optimization. ( it is being developed . . . )

<p align="center">
    <img src="https://github.com/odb9402/OPPA/blob/master/oppa/oppa.jpg" alt="OPPA logo" size=50  width="210" height="200">
</p>

> **OPPA :** A respectful Korean term used by females to call older males such as older male friends or older brothers, but now with the Hallyu kickin' in, people are using it being as annoying as the Japanese, "Kawaii" wave.

oppa try to bayesian optimize hyperparameter of peak detection algirithm , like a macs , by using labeled data.

--------
QUICK START
-------

>INSTALL:
>
> 
	cd dependencies
	python dependencies.py
you can install dependencies from this python script
>		
	sudo apt-get install bamtools
	sudo apt-get install samtools
and you need bamtools and samtools  for execute oppa

---

>RUNNING:
>
	example :	
    `OPPA -t MACS -I input_name -c control_file_name -vs label_name`
    see more :
    `OPPA -h`



--------
LABELED DATA
-------

for running oppa, you need labeled data file for defining error.  all these approach is from [1] ( 2016 HOCKING , Toby Dylan  ,et al ). example of labeled data is like this. (ASCII)

> 
	chr1:1,000,000-1,100,000 peaks K562
	chr1:1,100,000-1,200,000 peakStart K562
	chr1:1,250,000-1,300,000 peakEnd K562
	chr2:10,000,000-10,002,000 peaks


in line 1, mean cell K562 at least has one peak in that regions. in line 2, 3, mean cell K562 just only one peak in that regions. in line 4,  there is no peak in that regions about K562 or other cell. if you using this label data on other cell,  all the line 1-4 mean 'noPeak' because there is no cell name in line. as the paper [1], you can label your own data in 10 minute at UCSC genome browser. if you want to know specific rules of this labeling work, please look [here.](https://academic.oup.com/bioinformatics/article/33/4/491/2608653/Optimizing-ChIP-seq-peak-detectors-using-visual)

--------
DEPENDENCY
-------

- python2.7 -using python 2.7
 >- [BayesianOptimization](https://github.com/fmfn/BayesianOptimization)
 >- scipy
 >- numpy
 >- skleran

- R 
 >- multicore
 
- samtools - 
- bamtools - using bamtools
- [MACS](https://github.com/taoliu/MACS) - using MACS version 2.1.0
- [SPP](https://github.com/xinwang2hms/SPP) - using SPP version 2.0.1
- [phantompeakqualtools](https://github.com/kundajelab/phantompeakqualtools) - using phantompeakqualtools
---------
>**CITATION**
1. HOCKING, Toby Dylan, et al. Optimizing ChIP-seq peak detectors using visual labels and supervised machine learning. Bioinformatics, 2016, 33.4: 491-499.
2.  SNOEK, Jasper; LAROCHELLE, Hugo; ADAMS, Ryan P. Practical bayesian optimization of machine learning algorithms. In: Advances in neural information processing systems. 2012. p. 2951-2959.
