# Analysis Engine

This module comprises of code used for the analysis. The analysis engine has several components: 

## Mask Model Generator

`mask_model_generator` contains code and experimental data for generating the mask models for each PET. The analysis code outputs the mask models in the form of a TeX file. Additional description is available within the folder. 

## Hybrid Analysis

`hybrid_analysis` contains code for performing the hybrid evaluation of PETs. Additional description is available within the folder. 

## Tor Case Study

`tor_case_study` contains code and data for a case study on informing design choices for Tor. Additional description is available within the folder.

## Common

`common`  contains common libraries that are used in different modules: 
* `data_interface.py` has functions to read data and transfrom it into various formats
* `metrics.py` contains functions for computing various metrics and statistics
* `plot.py` contains functions for generating various plots
* `texify.py` contains functions to generate results in the form of TeX files