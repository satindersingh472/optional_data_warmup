
from dbhelpers import conn_exe_close
from apihelpers import verify_endpoints_info,add_for_patch
from flask import Flask, request, make_response
import json
import dbcreds

app = Flask(__name__)

@app.patch('/api/client')
def client_patch():
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    client_details = conn_exe_close('call client_get_with_token(?)',[request.headers.get('token')])
    object = add_for_patch(request.json,['email','password','bio','image_url'],client_details[0])
    results = conn_exe_close('call client_patch(?,?,?,?,?)',
    [object['email'],object['password'],object['bio'],object['image_url'],request.headers.get('token')])
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('updated successfull',default=str),200)
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps('not updated',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)


if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


