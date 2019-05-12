This directory will contain fingerprint summary files of all visited
browser instances.


Each file contains either an error message for debugging, or a string 
version of python dictionary, or empty which implies that javascript is 
disabled on the client side.

If the summary file correctly contains the python dictionary, one can type

    python read.py "some-log-filename"
    
to pretty print the output file. 
Also, *read.py* contains the example code that can convert the file back to 
a python dictionary.

**tor.txt** and **chrome.txt** are example output logs for Tor and Chrome browsers.
