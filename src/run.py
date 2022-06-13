
from config import get_config
from data import init_data

#def Pillow(optList, data, weights, folds=10):
def train(data, weights, config):
    
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

        # TODO : finish

def main():
    # acquire config
    config = get_config().parse_args()
    
    # set up file system
    if not os.path.exists(config.data_path): 
        os.makedirs(config.data_path)
    if not os.path.exists(config.save_path):
        os.makedirs(config.save_path)

    # load data
    print(f'\nLoading and Initializing Data... (Subject: {config.subject}, Task: {config.task}, Cooling: {config.cooling})')
    weights, data = init_data(config)

    # TODO : training loop

    # TODO : plotting    
    
if __name__ == '__main__':
    main()
