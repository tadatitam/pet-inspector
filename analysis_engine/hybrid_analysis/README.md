# Hybrid Analysis

This module contains code used for the hybrid analysis. These python functions require access to an observational dataset of fingerprints. You can set the location of the dataset by editing the host, user, passwd, database and table parameters in `data_interface.py`.

* `hybrid_analyze.py` contains functions to perform hybrid evaluation of PETs. It computes effectiveness metrics without any PET, as well as with each AFPET. It also performs popularity-based evaluations and outputs all results to different TeX files. Run using the following command:
```python hybrid_analyze.py```

* `compute_surprisal.py` computes surprisal values for certain `attributes_to_check` based on an observational database. Run using the following command:
```python compute_surprisal.py```
