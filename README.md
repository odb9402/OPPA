
OPPA
======
Optimize Parameter for Peak detection Algorithm by bayesian optimization.

<p align="center">
    <img src="https://github.com/odb9402/OPPA/blob/master/oppa/oppa.jpg" alt="OPPA logo" size=50  width="210" height="200">
</p>

> **OPPA :** A respectful Korean term used by females to call older males such as older male friends or older brothers, but now with the Hallyu kickin' in, people are using it being as annoying as the Japanese, "Kawaii" wave.

OPPA try to bayesian optimize hyperparameter of peak detection algirithms such as macs2 by using labeled data.

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
	( in directory of OPPA )
	python setup.py install

---

>RUNNING:
>
	example :	
    `OPPA1 -t MACS -I input_name -c control_file_name -vs label_name`
    see more :
    `OPPA1 -h`



--------
LABELED DATA
-------
OPPA uses labeled data which has its own format. All these approaches that use labeled data for marking is from [1]. Examples of labeled data is as the following below. (It based on ASCII)

> 
	chr1:1,000,000-1,100,000 peaks K562
	chr1:1,100,000-1,200,000 peakStart K562
	chr1:1,250,000-1,300,000 peakEnd K562
	chr2:10,000,000-10,002,000 peaks

In line 1, **peaks**, it means that K562 cell has at least one peak in a region (chr1:1,000,000-1,100,000). In line 2, 3 ,**peakStart, peakEnd**, represent that there is an only one single peak in the regions of K562 cell. In line 4, there is no peak in that region about K562 or other cells because there is no matched cell line name at this raw. If you want to use this label data on other cells, all these lines 1-4 are going to be **noPeak** because there is no cell name in the lines. If you want to know specific rules or methods of this labeling work, please look [here.](https://academic.oup.com/bioinformatics/article/33/4/491/2608653/Optimizing-ChIP-seq-peak-detectors-using-visual)

--------
DEPENDENCY
-------

- python2.7 -using python 2.7
 >- [BayesianOptimization](https://github.com/fmfn/BayesianOptimization)
 >- scipy
 >- numpy
 >- skleran

- dev-python

- R 
 >- multicore
 
- C++
 >- boost
 >- python.h ( in dev-python )
 
- samtools - 
- bamtools - using bamtools
- [MACS](https://github.com/taoliu/MACS) - using MACS version 2.1.0
- [SPP](https://github.com/xinwang2hms/SPP) - using SPP version 2.0.1
- [phantompeakqualtools](https://github.com/kundajelab/phantompeakqualtools) - using phantompeakqualtools
- [HOMER](http://homer.ucsd.edu/homer/) - using HOMER
---------
>**CITATION**
1. HOCKING, Toby Dylan, et al. Optimizing ChIP-seq peak detectors using visual labels and supervised machine learning. Bioinformatics, 2016, 33.4: 491-499.
2.  SNOEK, Jasper; LAROCHELLE, Hugo; ADAMS, Ryan P. Practical bayesian optimization of machine learning algorithms. In: Advances in neural information processing systems. 2012. p. 2951-2959.
3. Heinz S, Benner C, Spann N, Bertolino E et al. Simple Combinations of Lineage-Determining Transcription Factors Prime cis-Regulatory Elements Required for Macrophage and B Cell Identities. Mol Cell 2010 May 28;38(4):576-589.
