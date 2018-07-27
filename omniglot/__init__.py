"""Omniglot helper package.

   @description
     Model - For training, validating/evaluating & predictions with SiameseNetwork.
     Dataset - For visualizing, pre-processing and loading the Omniglot dataset.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola/

   @project
     File: __init__.py
     Created on 18 May, 2018 @ 5:22 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""

from omniglot.data import Dataset, Visualize
from omniglot.data import n_runs, compressed_dir, data_dir, base_dir

from omniglot.model import SiameseNetwork


__all__ = [
    # Dataset.
    'base_dir', 'data_dir',
    'compressed_dir', 'n_runs',
    'Dataset',

    # Model.
    'SiameseNetwork',
]