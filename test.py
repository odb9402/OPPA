from oppa.ensembler.ensembler import ensembleMethod as ensembler
import sys
import random

### python test.py [inputfile1] [inputfile2]
### and it generate random error rate.

foo = []
foo.append(sys.argv[1])
foo.append(sys.argv[2])

i = []
for k in range(len(foo)):
	i.append(random.random()%0.3)

ensembler(foo,i)
