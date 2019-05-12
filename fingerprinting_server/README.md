# Fingerprinting Server

This is a copy of the code used for setting up the fingerprinting server. 
Check out the original repository at *https://github.com/amberlu/FP_Modified*.

## Summary
This project aims to collect fingerprints from the user's browser as inclusive as possible.
Its fingerprinting tests come from Fingerprint Central, Panopticlick and some of our own.
Credit to:
[Fingerprint Central](https://github.com/plaperdr/fp-central)
 and [Panopticlick](https://github.com/EFForg/panopticlick-python)

## Installation

### Option 1: Running on a localhost

To launch the project, one will start the **run.py** script. We recommend the following steps:

Creation of your virtual environment

Local installation of packages through pip

    pip3 install -r requirements.txt

After this step, you can directly run

    python3 run.py

By default, the website is launched on port 5000.

    http://127.0.0.1:5000

Summary report of the user's browser is stored under **outputs/**

### Option 2: Running on a web server

Depending on the web server, the setup procedure can be different.
For example, one can deploy this Flask application with Apache WSGI.
You may need to modify *fp.wsgi* and *__init__.py*. 
One useful resource is at http://flask.pocoo.org/docs/1.0/deploying/. 

## General structure
**run.py** is the major execution file. It, at the same time, makes calls to */static/js/clientAPI.js*.

**templates** dir contains all the html files. Only *base.html* and *fp.html* are used here.

**fingerprint** dir is the most important folder that contains all fp tests. 
All added tests are placed in *fingerprint/attribute/standard/js/*. 
To add a new test, both new-test.json and new-test.js need to be 
included. 

**outputs** dir contains fingerprint log of visitors' browsers in txt format.

## Fingerprint Tests Include:
user agent

accept headers

cookie enabled?

math and tan functions

dom storage

language

do not track Enabled?

buildID

touch support?

platform

fonts (JS)

webGL Fingerprint

canvas Fingerprint

openDB

indexedDB

cpuClass

timezone

color depth

adBlock installed?

screen resolution 

IE addBehavior?

browser plugins


## Issues ##
1. If the error code for POST store is 405 - Method Not Allowed, check the POST path which the client sends and make sure it is consistent with the route of store function, "@app.route('some path', method=['POST'])" in run.py.
