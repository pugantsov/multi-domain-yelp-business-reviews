# Multi-Domain Yelp Business Reviews
A multi-domain sentiment classification dataset extended from the Business and Reviews datasets supplied by the [2015 Yelp Dataset Challenge](https://www.yelp.com/dataset).

# Prerequisites
The parsing functionality requires both datasets to be downloaded and supplied to the parsing script.

The following Python packages must be installed:

 - Pandas
 - Numpy
 - Datasets (HuggingFace)

# Usage Instructions
Run `parse.py` with the following, mandatory arguments:

 - `-rf` or `--reviews-file`: Filepath to the Yelp Reviews JSON file (str)
 - `-bf` or `--business-file`: Filepath to the Yelp Business JSON file (str)
 - `-out` or `--output-dir`: Filepath to the directory where the datasets will be saved.
