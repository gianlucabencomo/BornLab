import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

from pillow.plot.analysisFunctions import makeWeightPlot

def regraph(config):

    # load file
    D = np.load(config.data_path, allow_pickle=True)['save_dict'].item()

    # extract neccessary data
    wMode = D['wMode']
    data = D['data']
    weights = D['weights']
    credibleInt = D['credibleInt']
    test_results = D['test_results']
    
    # plot
    makeWeightPlot(wMode, data, weights, errorbar=credibleInt,
                    perf_plot=config.perf, bias_plot=config.bias, 
                    temperature=config.temp, prediction=test_results)

    # show
    plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-dp', '--data_path', type=str,
                        required=True, 
                        help='File path to data.')
    parser.add_argument('-p', '--perf', action='store_true',
                        help='Plot performance.')
    parser.add_argument('-b', '--bias', action='store_true',
                        help='Plot bias.')
    parser.add_argument('-t', '--temp', action='store_true',
                        help='Plot temperature.')

    config = parser.parse_args()   

    regraph(config)
