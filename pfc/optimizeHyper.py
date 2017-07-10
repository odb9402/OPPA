import numpy

from moe.python.data_containers import SamplePoint

def run(args):
    pass

points_sampled = [SamplePoint(numpy.array([x]), numpy.random.uniform(-1,1), 0.01)
                  for x in numpy.arange(0, 1, 0.1)]

