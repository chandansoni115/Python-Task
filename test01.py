from flask import Flask,request
import os
from os import path
import json
app = Flask(__name__) 

@app.route("/", methods=['GET']) 
def index (): 
    lines_rd = []
    start =0
    end = 0
    count= 0
    file_path=''
    response=dict()
    for k in request.args:
        if k not in ['path','start','end']:
            response['status'] = False
            response['message'] = 'unknown parameter specified'
            return json.dumps(response),500
    if 'path' not in request.args:
        file_path = 'file1.txt'
    else:
        file_path= request.args.get('path')
    if  'start' in request.args:
        start =  request.args.get('start')
    if 'end' in request.args:
        end = request.args.get('end')
    try:
        with open(file_path) as f:
            for line in f:
                lines_rd.append(line)            
            if end==0:
                end = len(lines_rd)
            start = int(start)
            end = int(end)
            total_lines = lines_rd[start:end]
            count = len(total_lines)
            response['file_read'] = file_path
            response['number_of_lines_read'] = count
            response['lines'] = total_lines
    except ValueError as v:
        response['status'] = False
        response['message'] = "Start and end parameters should be integer"
    except IOError as i:
        response['status'] = False
        response['message'] = "File not found"
    except Exception as e:
        response['status'] = False
        response['message'] = e.message
        response['name'] = e.__class__.__name__
    return json.dumps(response, sort_keys=True),200
   

if __name__ == "__main__":    
    app.run()