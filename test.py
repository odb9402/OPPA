from oppa.ensembler.ensembler import ensembleMethod as ensembler
import sys

foo = []
foo.append(sys.argv[1])

i = []
for k in range(len(foo)):
	i.append(0)

ensembler(foo,i)
