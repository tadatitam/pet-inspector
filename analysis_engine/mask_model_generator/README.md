# Mask Model Generator

This module contains code used for the experimental analysis to generate mask models of AFPETs. 

* `exp_analyze.py` contains code and data for generating mask models. Run using the following command:
```python exp_analyze.py <log_location>```

* `mask_models.py` contains the python representations of the generated mask models generated. For now, the python representations are manually crafted from the TeX file, but this can be easily automated in future iterations. 

* `www2019_data` contains experimental data in the form of logs from experiments conducted using the fingerprinting_server and the client_simulator. It is included in the WWW 2019 submission. 

* `old` contains old experimental data from two experiments conducted in the past and an old-version `exp_analyze.py` for parsing it. It is kept mainly for our own record.
