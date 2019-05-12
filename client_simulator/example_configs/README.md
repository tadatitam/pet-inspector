# Example Configs

This folder includes two example pairs of configration files that **start.py** will take.
    
    native_mac.json: experiment config for native Mac 

    native_server.json: server config for native platforms

And 

    vm_all.json: experiment config for virtual machines

    vm_server.json: server config for virtual machines 


## Configs For Experiments

A json file that sets attributes for the experiment, including:

* *type*: whether experiments are done on "native" or "virtual" machines

* *experiment_name*: a string indicating the name of this experiment, for the ease of later analysis

* *oses*: a list of tested operating systems

* *configs*: a dictionary where the key is an operating system and the value is a list of configrations for this OS (you may want to see **client/vm/configs**)

* *browsers*: a list of tested browsers

* *pets*: a dictionary where the key is a browser and the value is a list of PETs to test on that browser

* *repeats*: an integer indicating the number of reloads for *cross\_reload* function

* *test_behaviors*: a list of functions that the client will use to visit the server (see **start\_visit/start\_pet.py**) 


## Configs for Server

A json file that includes information for the fingerprinting server, including:

* *fp\_sites*: a list of fingerprinting website URLs to visit

* *socks5\_proxy*: a boolean value indicating whether or not to configure socks5 proxy for browsers 

* *proxy_setting*: a dictionary of setting info if using socks5 proxy
