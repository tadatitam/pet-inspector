# Tor Case Study

This folder contains relevent code for our case study on Tor to inform AFPET design. 

* `alternate_designs.py` contains the relevant code to generate alternate Tor designs. To display alternate designs from simulated data with cap parameters set to 1350x1000 and 1550x1000 respectively, Run using the following command:
```python alternate_designs.py``` 

* `torpoint.txt` stores the loss and effectiveness measures for Tor's original design. 

* In order to speed up the analysis, we generate and store the simulated data in the folder `simulated_data`and perform the analysis on the data. To generate fresh data, uncomment the function call to `generate_tor_simulation_data` in the first line of the main function.