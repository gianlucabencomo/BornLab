import os
import time
import numpy as np

from config import get_config
from data import init_data

def train(data, weights, config):
    
    start = time.time()

    from pillow.hyperOpt import hyperOpt
    
    K = np.sum([weights[i] for i in weights.keys()])

    hyper= {'sigInit' : 2**4.,
            'sigma' : [2**-4.]*K, 
            'sigDay' : [2**-4.]*K}

    print("Beginning Hyperoptimzation...")
    hyp, evd, wMode, hess = hyperOpt(data, hyper, weights, config.optList)
    print(hyp)
    print("Beginning Credible Interval Calculation...")
    from pillow.aux.invBlkTriDiag import getCredibleInterval
    credibleInt = getCredibleInterval(hess)
    
    from pillow.aux.crossValidation import Kfold_crossVal

    trainDs, testDs = Kfold_crossVal(data, F=config.folds)

    from pillow.aux.crossValidation import Kfold_crossVal_check

    test_results = []
    for k in range(config.folds):
        print("Running xval fold", k+1)

        _, _, wMode_K, _ = hyperOpt(trainDs[k], hyper, weights, config.optList)

        logli, gw = Kfold_crossVal_check(testDs[k], wMode_K, trainDs[k]['missing_trials'], weights)

        res = {'logli' : np.sum(logli), 'gw' : gw, 'test_inds' : testDs[k]['test_inds']}
        test_results += [res]

    print("Cross-validated log-likelihood of model:", np.sum([i['logli'] for i in test_results]))

    cvll = np.sum([i['logli'] for i in test_results])

    end = time.time()

    print(f'Total Training Time: {end - start:.2f} s')

    # save results
    save_dict = dict()
    save_dict.update({
            "data": data,
            "weights": weights,
            "test_results": test_results,
            "wMode": wMode,
            "credibleInt": credibleInt,
            "cvll": cvll,
            "hyp": hyp,
            "duration": END - START,
        })
    np.savez_compressed(config.save_path, save_dict=save_dict)
    
    return wMode, data, weights, credibleInt, test_results, cvll, hyp, duration
    
def main():
    
    config = get_config().parse_args()
    
    # set up file system
    if not os.path.exists(config.data_path): 
        os.makedirs(config.data_path)
    if not os.path.exists(config.save_path):
        os.makedirs(config.save_path)

    # load data
    print(f'\nLoading and Initializing Data... (Subject: {config.subject}, Task: {config.task}, Cooling: {config.cooling}, Seed: {config.seed})')
    weights, data = init_data(config)
     
    # TODO : training loop
    wMode, data, weights, credibleInt, test_results, cvll, hyp, duration = train(data, weights, config)
    
    # TODO : plotting    
    from pillow.plot.analysisFunctions import makeWeightPlot
    
    if config.plot:
        makeWeightPlot(wMode, data, weights, END=100000, errorbar=credibleInt,
                        perf_plot=True, bias_plot=True, prediction=test_results)    

if __name__ == '__main__':
    main()
