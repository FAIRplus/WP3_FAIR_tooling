from os import path
from flask import Flask, request, render_template, flash, session, jsonify, make_response, send_from_directory, Response
from jinja2 import Environment, FileSystemLoader, Template
import pandas as pd
import io
import time
import uuid
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import biotools_API_querying as bAq


class unique_run(object):

    def __init__(self, request):
        self.request = request
        self.request_ID = self.generate_request_id()

        self.parse_input()

    def generate_request_id(self):
        new_id = uuid.uuid4()
        return new_id

    def parse_input(self):
        inputs_kw = []
        missing_weights_n = 0
        try:
            for line in self.request.json['textarea_content'].split('\n'):
                if line:
                    if ',' in line:
                        k = line.split(',')[0].lower()
                        w = float(line.split(',')[1])
                    else:
                        k = line.lstrip().lower()
                        w = 1.00
                        missing_weights_n += 1
                    inputs_kw.append({'keyword':k, 'weight':w})
            if missing_weights_n == len(inputs_kw):
                self.custom_weights = False
            else:
                self.custom_weights = True
            
        except Exception as err:
                print(err)
                raise
        else:
            print(inputs_kw)
            self.inputs_kw = inputs_kw
            
            
                

    def build_results_html(self):
        html=render_template('results.html', 
                              input=self.inputs_kw, 
                              tools_results=self.tools_discov.html_df, 
                              results_id=self.request_ID)
        return(html)

    def write_inputs_disk(self):
        path = f"temp/{self.request_ID}_input.csv"
        self.tools_discov.ranked_keywords.to_csv(path, index=False)  

    def run_tool_discoverer_query(self):
        ## run tool:
        print('running tool')
        self.tools_discov = bAq.tools_discoverer(self.request_ID,
                                            self.inputs_kw,
                                            'temp',#output directory
                                            None, #default score 
                                            self.custom_weights, # True is any custom weight entered
                                            True) #verbosity

        self.tools_discov.run_pipeline()
        json_result = self.tools_discov.generate_outputs()
        return(json_result)


app = Flask(__name__,
            static_url_path='',
            static_folder='assets',
            template_folder='templates')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)

@app.route('/',methods = ['POST'])
def run_discoverer():
    if request.method == 'POST':
        try:
            # run query
            this_run = unique_run(request)
            result = this_run.run_tool_discoverer_query()
            input_parameters = this_run.inputs_kw
            data = {'result':result, 'input_parameters':input_parameters}
        except Exception as err:
            data = {'message': "something went wrong", 'code': 'ERROR'}
            resp = make_response('', 400)
            print(err)
        else:
            #prepare response
            data = {'message': data, 'code': 'SUCCESS'}
            resp = make_response(jsonify(data), 201)
        finally:
            resp.set_cookie('same-site-cookie', 'foo', samesite='Lax');
            resp.set_cookie('cross-site-cookie', 'bar', samesite='Lax', secure=True);
            return resp
    else:
      return(make_response('', 400))

@app.route('/path:filename')
def send_misc(path,filename):
    return send_from_directory("/".join(app.static_folder,path),filename)


@app.route('/getInputCSV/<results_id>', methods=['GET'])
def getInputCSV(results_id):
    path = f"temp/{results_id}_input.csv"
    with open(path) as fp:
         csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=tool_discoverer_input.csv"})


@app.route('/getResultsCSV/<results_id>', methods=['GET'])
def getResultsCSV(results_id):
    path = f"temp/{results_id}_ranked_tools.csv"
    with open(path) as fp:
         csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=tool_discoverer_results.csv"})


@app.route("/help")
def template_help():
    return render_template('help.html', help="active")

@app.route("/fairification")
def template_fairification():
    return render_template('fairification.html', fairification="active")

@app.route("/about")
def template_about():
    return render_template('about.html', about="active")

if __name__ == '__main__':
    app.run(debug=True)