import os
import argparse
import numpy as np

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subject', type=str,
                        choices=['A', 'U'],
                        required=True,
                        help='Subject to use for analysis, Apollo (A) or Urkel (U).')
    parser.add_argument('-t', '--task', type=str,
                        choices=['C', 'O', 'I', 'I19', 'C19'],
                        required=True,
                        help='Task Selection: Cardinal (C), Oblique (O), Interleaved (I), 
                                Interleaved 2019 (I19, Apollo Only), Cardinal 2019 (C19, Apollo Only).')
    parser.add_argument('-c', '--cooling', action='store_true',
                        help='Flag indicating whether or not cooling session is desired.')
    parser.add_argument('-sd', '--seed', type=int, 
                        default=np.random.randint(0, 2**32 - 1),
                        help='Specify a manual seed. Otherwise random.')
    parser.add_argument('-dp', '--data_path', type=str,
                        default=os.path.join(os.path.dirname(os.getcwd()), 'data'), 
                        help='Data path to save to.')
    parser.add_argument('-sp', '--save_path', type=str,
                        default=os.path.join(os.path.dirname(os.getcwd()), 'output'), 
                        help='Experimental path to save to.') 
    parser.add_argument('-w', '--weights', nargs='+', 
                        default=['bias', 'stimulus_strength'],
                        help='List of weights to use. Supported options: .') # TODO : add supported options
    parser.add_argument('-std', '--standardize', action='store_true',
                        help='Zero-mean and normalize data over entire session if set to true.')
    parser.add_argument('-o', '--optList', nargs='+',
                        default=['sigma', 'sigDay'],) # TODO: add help description
    parser.add_argument('-f', '--folds', type=int,
                        default=10,
                        help='Number of folds for cross-validation.')
    
    
    # TODO : Finish adding and modifying configurations
    
    return parser
