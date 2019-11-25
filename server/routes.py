from server import server
from flask import request
from flask import jsonify
from sklearn.neighbors import LocalOutlierFactor
import pickle

#Load model
model = pickle.load(open("Local Outlier Factor.model", 'rb'))

@server.route('/')
@server.route('/check', methods=['POST'])
def check():
    #Get data
    data = request.get_json()
    data = data['data']

    #Compare with model
    result = model.predict([data])

    #Return result
    return jsonify({'result': int(result[0])})