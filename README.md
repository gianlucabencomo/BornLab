# Born Lab - Time-Varying Behavorial Analysis

This repository contains the methods ... (in progress!)

## Dependencies
- Python 3.10.5
- Numpy 1.20
- Matplotlib 3.3
- Scipy 1.8.0

## Data
One task for one subject is included in this repository (Apollo, Cardinal, no cooling).  The subject's data is alreadypre-processed and ready to run. This repository is compatiable with two subjects (Apollo, Urkel), three tasks paradigms, (Cardinal, Oblique, Interleaved), and with cooling/non-cooling data.  The data was collected as a part of a series of experiments done at Harvard Medical School with the Born Lab (experiments not done by me).

## Run

From the root folder, run
```
python run.py -s [subject] -t [task]
```
For example, the following will run Apollo's non-cooling Cardinal task from 2017, with standardization and plotting: 
```
python run.py -s A -t C --standardize --plot
```
A wide selection of configurations are available for specification: 
```
Usage: train.py [OPTIONS]

Options:
  -d, --dataset [vgg|mbm|dcc|adi]
                                  Dataset to train model on (HDF5).
                                  [required]

  -lr, --learning_rate FLOAT      Initial learning rate.
  -e, --epochs INTEGER            Number of training epochs.
  -b, --batch_size INTEGER        Batch size for both training and validation.
  -a, --augment                   Augment training data.
  -uf, --unet_filters INTEGER     Number of filters for U-Net convolutional
                                  layers.

  -c, --convolutions INTEGER      Number of layers in a convolutional block.
  -p, --plot                      Generate a live plot.
  -wd, --weight_decay FLOAT       Weight decay.
  -m, --momentum FLOAT            Momentum.
  -o, --optim TEXT                Optimizer for training (Options: AdamW,
                                  RMSprop, SDG).

  -s, --seed INTEGER              Seed for train/test split.
  -sc, --scheduler TEXT           Learning rate scheduler.
  -l, --loss_function TEXT        Loss function to use.
  -sp, --save_path TEXT           Specify the save path to which
                                  models/results should be saved.  [required]

  --help                          Show this message and exit.
```

## Regraph

The `predict.py` script is provided to run a trained model on any given input image.

```
Usage: predict.py [OPTIONS]

Options:
  -d, --dataset [vgg|mbm|dcc|adi]
                                  Dataset to pull image from (HDF5).
                                  [required]

  -i, --index INTEGER             Image index to visualize.
  -c, --checkpoint FILENAME       A path to a checkpoint with weights.
                                  [required]

  -u, --unet_filters INTEGER      Number of filters for U-Net convolutional
                                  layers.

  -co, --convolutions INTEGER     Number of layers in a convolutional block.
  -v, --visualize                 Visualize predicted density map.
  --help                          Show this message and exit.

```

### Examples

```
$ python run.py -s A -t C --standardize --plot                                   
```

![](./etc/example.png)

