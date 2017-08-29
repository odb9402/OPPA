import numpy as np
import math

#from macs.learnMACSparam import run as learnMACparam
from BayesianOptimization.bayes_opt.bayesian_optimization import BayesianOptimization

#function for testing Bayesian optimization.


def optimized_function(function, error, *param):
	"""
    this function will wrap black box function for bayesian optimization.
    now, we denote vector like X = { x1, x2, ... , xn } to capitalize
    like this A = { a1, a2, ... , an }. so in our concept, X is a
    input parameter of peak calling algorithms and y=f(X) is error rate
    about those input. we can make abstraction of that functions.

    :param function:
        the function which you want to wrap.
        e. g. : in MACS, can f : macs.learnMACSparam.run()

    :param error:
        result error rate of input some parameter vector X = {p1,p2,p3}
        e. g. : in MACS, can X = { q value, mfold }

    :param param:
        input parameters or parameter that it will be input to some Peak
        detection algorithm. it is denoted X = { p1, p2, p3 }

    :return:

	"""
	return None


def run(function, Param_bound, init_point, return_dict, num_itr = 10, acq_func = 'ei', chrNo= None):
	"""
    Doing Bayesian optimization with some function. the function is just process that
    input the file and parameter to Peak Detection algorithm and get some error.

    X : parameters
    Y : errors

    f : X -> Y

    in MACS case, for example, run(args) in learnMACSparam.py can be optimized-function.
    or you can wrap that function. ( f : learnMACSparam.run() . . . etc )
    and also, because we use "BayesianOptimization" module if you update or modify or read
     this code, you should keep refer that module.

    :param function:
        function will be optimized.

    :param Param_bound:
        this Parameter would be boundary of parameter will be learned. and it must be
        python tuple : (min,max)

    :param init_point:
        this parameter decide number of sample which randomly generated for first state.
        
    :return:
        return the python dictionary that is
        {'max_val' : maximum observation value. ,
        'max_param' : the parameter can be observe maximum value }
    
	"""

	"""
    In the Bayesian Optimization Class`s field :
        
        keys : Error Value of each parameters ( List : [] )
        
        dim : number of parameters ( int : 0-n )
        
        bounds : boundary of parameters to List ( List : [] )
        
        X : Numpy array place holders ( Numpy Array )
        
        Y : Numpy array place holders ( Numpy Array )
        
        gp : Class Object of GaussianProcessRegressor , 
            set the Kernel function and others ( Class GaussianProcessRegressor )
        
        util : choose your utility function ( function )
        
        res : output (result) dictionary . field is
                self.res['max'] = {'max_val': None, 'max_params': None}
                self.res['all'] = {'values': [], 'params': []}
        
        and etc...

    and you can do optimization by maximize() Method,
    you can initialize data frame ( table of data structure ) by initialize_df method.
	"""
	optimizer = BayesianOptimization(function, Param_bound, verbose=False)
    
	
	optimizer.explore(Param_bound)
	optimizer.maximize(acq = acq_func, init_points=init_point, n_iter=num_itr)

	result = chrNo, optimizer.res['max']

	return_dict[chrNo] = optimizer.res['max']
	print chrNo + " is done insert into result containor."
