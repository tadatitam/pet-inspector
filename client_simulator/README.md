# Client Simulator  

This module consists of code for running experiments, including setting up clients with different browsing platforms
and driving them to visit the fingerprinting server's address. 

## start.py 

*start.py* starts experiments by invoking functions from *client/* and *start\_visit/*.

It takes in two configuration files: one for experimental attributes, and another for server-related information.
See *example\_configs* for more details.  

To start experiments, run the following:

    python start.py <config_for_experiments> <config_for_server>

## Client

Contains code for creating a client. 

## Start Visit

Contains code for client behaviors while visiting the server.

## Example Configs

Contains configuration templates to pass to *start.py*.
