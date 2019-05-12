#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,render_template,Blueprint,request,make_response,jsonify
from flask import request                   # for reading url parameters
from fingerprint.attributes_manager import *
#from fingerprint.tags_manager import *
from fingerprint.acceptable_manager import *
from flask_babel import Babel
from datetime import datetime, timedelta
from functools import wraps
from pprint import pprint
import env_config as config
import json
import hashlib
import sys
import hashlib
import os

###### App
app = Flask(__name__)
app.debug = config.debug

cwd = os.path.dirname(os.path.abspath(__file__))
attributes_folder = os.path.join(cwd, "fingerprint/attributes")

attributes = Blueprint('site', __name__, static_url_path='', static_folder='fingerprint/attributes',url_prefix='')
app.register_blueprint(attributes)
files,variables = get_files_and_variables(attributes_folder)
variablesWithHTTP = [["User-Agent"],["Accept"],["Accept-Language"],["Accept-Encoding"],["Connection"]]
variablesWithHTTP.extend(variables)
definitions = get_definitions(attributes_folder)
#tagChecker = TagChecker()
#tags = tagChecker.getTagList()
acceptableChecker = AcceptableChecker()
unspecifiedValue = "-"

@app.route('/')
def home():
    print("home")
    exp = request.args.get('exp')
    os1 = request.args.get('os')
    config = request.args.get('config')
    browser = request.args.get('browser')
    pet = request.args.get('pet')
    sess = request.args.get('sess')
    params = [['_exp', exp], ['_os', os1], ['_config', config], ['_browser', browser], ['_pet', pet], ['_session', sess]]
    return render_template('fp.html', files=files, variables=variables, headers=request.headers, params=params)

@app.route('/store', methods=['POST'])
def store():
    print("store")
    return json.dumps(out.storeFP(request, request.data,True))


###### Babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(config.LANGUAGES.keys())

###### DB
class Output(object):
    def storeFP(self, request, fingerprint,decode):
        try:
            # Create an output file whose name is the time when the browser loads 
            output_dir = os.path.join(cwd, "outputs/")
            generated_time = str(datetime.utcnow())
            output_fn = output_dir+"log"
            output_fn = output_fn + "--" + generated_time + '.txt' 
    

            PATH="./"+output_fn
            if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
                response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_fn)
                if response == 'n':
                    sys.exit(0)
            fo = open(output_fn, "w")
            fo.close() 
            
            #'fingerprint' is the raw output
            if decode :
                parsedFP = json.loads(fingerprint.decode('utf-8'))
            else :
                parsedFP = fingerprint
            parsedFP = self.parse(request, parsedFP)
            parsedFP["generated_time"] = generated_time
            # Write the fingerprint report to a file
            with open(output_fn, "w+") as out:
               out.write(str(parsedFP))
      
        except Exception as e:
            # Append the error message to the already-created output file
            with open(output_fn, 'a+') as f:
                f.write("error" + str(e))
    
   
    def parse(self, request, parsedFP):        
        #Adding adBlock information
        if "adBlock installed" not in parsedFP.keys():
            parsedFP["adBlock installed"] = "yes"
        
        #Convert certain attribute values into corresponding dictionaries
        dic = ["has user lied with", "screen", "storage", "touch support"] 
        for i in dic:
            if i not in parsedFP.keys():
                continue
            old = parsedFP[i]
            parsedFP[i] = self.convert_to(old, "dict")
        
        #Change the type of some attribute values into integers
        if "touch support" in parsedFP.keys():
            parsedFP["touch support"]["max touch points"] = int(parsedFP["touch support"]["max touch points"])

        if "screen" in parsedFP.keys():
            for key in parsedFP["screen"].keys():
                if parsedFP["screen"][key] != "undefined":
                    val = parsedFP["screen"][key]
                    try:
                        parsedFP["screen"][key] = int(val)
                    except ValueError:
                        print(key + ":int error")
                        parsedFP["screen"][key] = float(val) 

        # Hash canvas and webgl data if they are strings
        canvas_byte, webgl_byte = None, None 
        if "canvas" in parsedFP.keys():
            if sys.version_info[0] == 2 and isinstance(parsedFP["canvas"], basestring):
                canvas_byte = bytes(parsedFP["canvas"].encode('utf-8'))	
            elif sys.version_info[0] == 3 and isinstance(parsedFP["canvas"], str):
                canvas_byte = bytes(parsedFP["canvas"], 'utf-8')

        if "WebGL" in parsedFP.keys() and "Data" in parsedFP["WebGL"].keys():
            if sys.version_info[0] == 2 and isinstance(parsedFP["WebGL"]["Data"], basestring):
                webgl_byte = bytes(parsedFP["WebGL"]["Data"].encode('utf-8')) 
            elif sys.version_info[0] == 3 and isinstance(parsedFP["WebGL"]["Data"], str):
                webgl_byte = bytes(parsedFP["WebGL"]["Data"], 'utf-8')

        if canvas_byte is not None:
                canvas_hash = hashlib.sha1(canvas_byte)
                parsedFP["canvas"] = canvas_hash.hexdigest()

        if webgl_byte is not None:
            webgl_hash = hashlib.sha1(webgl_byte)
            parsedFP["WebGL"]["Data"] = webgl_hash.hexdigest()

    
        return parsedFP


    def convert_to(self, old, type):
        if type == "dict":
            result = dict()
            old_lst = old.split(";")
            for i in old_lst:
                i = i.split(":")
                if (len(i) != 2):
                    continue
                key, val = i[0], i[1]
                result[key] = val
        elif type == "list":
            result = list()
            old_lst = old.split(";")
            for i in old_lst:
                if len(i) < 1:
                    continue
                result.append(i)

        return result
out = Output()


###### API
def jsonResponse(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))
    return wrapper

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == "updateTags":
        #Update the list of tags of all fingerprints
        out.updateTags()
    else:
        #Launch application
        app.run()
