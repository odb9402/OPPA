from oppa.ensembler.ensembler import ensembleMethod as ensembler
import sys
import random
import subprocess

### python test.py [inputfile1] [inputfile2]
### and it generate random error rate.

cmd = ['sudo rm -r oppa/ensembler/build']
subprocess.call(cmd, shell=True)

cmd = ['python oppa/ensembler/setup.py install']
subprocess.call(cmd, shell=True)

foo = []
foo.append(sys.argv[1])
foo.append(sys.argv[2])

i = []
for k in range(len(foo)):
	i.append(random.random()%0.3)

ensembler(foo,i)
