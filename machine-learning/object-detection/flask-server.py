from flask import Flask
from flask import jsonify
from flask import request
from kubernetes import client, config
from create_pod import create_pod

app = Flask(__name__)


param = [{'blob-container': 'newcontainer'}]

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'Hello, World!'})

@app.route('/quarks', methods=['GET'])
def returnAll():
    return jsonify({'param' : param})

@app.route('/quarks/<string:name>', methods=['GET'])
def returnOne(name):
    theOne = param[0]
    for i,q in enumerate(param):
        if q['name'] == name:
            theOne = param[i]
    return jsonify({'param' : theOne})

@app.route('/create-pod', methods=['POST'])
def createPod():
    new_quark = request.get_json()
    param.append(new_quark)

    api_server_endpoint = "YOUR API"
    bearer_token = "YOUR BEARER TOKEN"


    configuration = client.Configuration()
    configuration.host = api_server_endpoint
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + bearer_token}
    client.Configuration.set_default(configuration)
    client_api = client.CoreV1Api()
    c=create_pod({}, param, client_api)
    return c

if __name__ == "__main__":
    app.run(debug=True)