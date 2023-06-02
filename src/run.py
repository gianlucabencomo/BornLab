import os
import time
import numpy as np
import matplotlib.pyplot as plt

from config import get_config
from data import init_data

# TODO : add better comments

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
            "duration": end - start,
        })
    np.savez_compressed(os.path.join(config.save_path, data['name']), save_dict=save_dict)
    
    return wMode, data, weights, credibleInt, test_results, cvll, hyp, (end - start)
    
def main():
    
    config = get_config().parse_args()

    # check for valid subject/task
    assert (config.subject + config.task + ('C' if config.cooling else '')) in \
            ['AC'], 'Subject/Task selection invalid!' # supported

    # TODO : add supported subject/tasks to config file and import
        
    # set random seed globally
    np.random.seed(config.seed)
    
    # check / set up file system
    if not os.path.exists(config.data_path): 
        os.makedirs(config.data_path)
    if not os.path.exists(config.save_path):
        os.makedirs(config.save_path)

    # load data
    print(f'\nLoading and Initializing Data... (Subject: {config.subject}, Task: {config.task}, Cooling: {config.cooling}, Seed: {config.seed})')
    weights, data = init_data(config)
    
    if config.task in ['C','O','C19']:
        wMode, data, weights, credibleInt, test_results, cvll, hyp, duration = train(data, weights, config)
    else:
        # TODO : add training functionality for interleaved
        print('Interleaved functionality unavailable')

    from pillow.plot.analysisFunctions import makeWeightPlot
    
    # plot time-series
    if config.plot:
        makeWeightPlot(wMode, data, weights, errorbar=credibleInt,
                        perf_plot=True, bias_plot=True, temperature=False, 
                        prediction=test_results)    
        plt.show()

    # TODO : add plotting functionality for interleaved

if __name__ == '__main__':
    main()
