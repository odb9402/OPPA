OPPA
======
Optimize Parameter in Peak detection Algorithm by bayesian optimization. ( it is being developed . . . )

<p align="center">
    <img src="https://github.com/odb9402/OPPA/blob/master/oppa/oppa.jpg" alt="OPPA logo" size=50  width="210" height="200">
</p>

> **OPPA :** A respectful Korean term used by females to call older males such as older male friends or older brothers, but now with the Hallyu kickin' in, people are using it being as annoying as the Japanese, "Kawaii" wave.


--------
QUICK START
-------

>INSTALL:
>	    
	setup :
	'python setup.py install'

---

>RUNNING:
>
	example :	
    `python oppa.py -t MACS -I input_name -c control_file_name -vs label_name`
    see more :
    `python oppa.py -h`



--------
LABELED DATA
-------
0


--------
DEPENDENCY
-------

- python2.7 -using python 2.7
 >- [BayesianOptimization](https://github.com/fmfn/BayesianOptimization)
 >- scipy
 >- numpy
 >- skleran

- samtools - 
- bamtools - using bamtools
- [MACS](https://github.com/taoliu/MACS) - using MACS version 2.1.0

---------
>**CITATION**

> - HOCKING, Toby Dylan, et al. Optimizing ChIP-seq peak detectors using visual labels and supervised machine learning. Bioinformatics, 2016, 33.4: 491-499.
> - SNOEK, Jasper; LAROCHELLE, Hugo; ADAMS, Ryan P. Practical bayesian optimization of machine learning algorithms. In: Advances in neural information processing systems. 2012. p. 2951-2959.
