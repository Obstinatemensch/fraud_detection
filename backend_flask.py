from flask import Flask, request, jsonify, abort
import json
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model
model_path = r'F:\Internship projects\Fraud_detection ml model\fraud_model.pkl'

with open(model_path, "rb") as f:
    model = pickle.load(f)


@app.route('/input', methods=['POST'])
def input_data():
    if request.method == "POST":
        data = request.get_json()
        processed_data = []

        if isinstance(data, list):
            for entry in data:
                request_data = {}

                request_data['step'] = entry['step']

                request_data['type'] = entry['type']

                try:
                    request_data['amount'] = entry['amount']
                except KeyError:
                    print("the field amount is empty")
                    # abort(400, 'Missing field: amount')
                    processed_data.append({'message': 'Missing field: amount'})
                    continue

                request_data['nameOrig'] = entry['nameOrig']

                try:
                    request_data['oldbalanceOrg'] = entry['oldbalanceOrg']
                except KeyError:
                    print("the field oldbalanceOrg is empty")
                    # abort(400, 'Missing field: field oldbalanceOrg')
                    processed_data.append({'message': 'Missing field: oldbalanceOrg'})
                    continue
                
                try:
                    request_data['newbalanceOrig'] = entry['newbalanceOrig']
                except KeyError:
                    print("the field newbalanceOrig is empty")
                    # abort(400, 'Missing field: newbalanceOrig')
                    processed_data.append({'message': 'Missing field: newbalanceOrig'})
                    continue

                request_data['nameDest'] = entry['nameDest']

                try:
                    request_data['oldbalanceDest'] = entry['oldbalanceDest']
                except KeyError:
                    print("The field oldbalanceDest is empty")
                    # abort(400, 'Missing field: oldbalanceDest')
                    processed_data.append({'message': 'Missing field: oldbalanceDest'})
                    continue
                
                try:
                    request_data['newbalanceDest'] = entry['newbalanceDest']
                except KeyError:
                    print("The field newbalanceDest is empty")
                    # abort(400, 'Missing field: newbalanceDest')
                    processed_data.append({'message': 'Missing field: newbalanceDest'})
                    continue

                request_data['isFraud'] = entry['isFraud']

                request_data['isFlaggedFraud'] = entry['isFlaggedFraud']

                # Process the data with your model
                feature_vector = [
                    request_data['oldbalanceOrg'],
                    request_data['newbalanceOrig'],
                    request_data['oldbalanceDest'],
                    request_data['newbalanceDest'],
                    request_data['amount']
                ]

                # Convert the feature vector to a numpy array for prediction
                feature_vector = np.array(feature_vector).reshape(1, -1)

                prediction = model.predict(feature_vector)
                if(prediction == 1):
                    isScam = "Scam"
                else:
                    isScam = "Not a Scam"
                i = 0
                while i < len(prediction):
                    processed_entry = {
                        # 'step': str(request_data['step']),
                        # 'type': request_data['type'],
                        # 'amount': str(request_data['amount']),
                        # 'nameOrig': request_data['nameOrig'],
                        # 'oldbalanceOrg': str(request_data['oldbalanceOrg']),
                        # 'newbalanceOrig': str(request_data['newbalanceOrig']),
                        # 'nameDest': request_data['nameDest'],
                        # 'oldbalanceDest': str(request_data['oldbalanceDest']),
                        # 'newbalanceDest': str(request_data['newbalanceDest']),
                        'isFraud': request_data['isFraud'],
                        # 'isFlaggedFraud': request_data['isFlaggedFraud'],
                        'prediction': isScam  # the model returns a single prediction
                    }
                    print("Finished loop iteration", i)
                    i += 1
                    processed_data.append(processed_entry)

                i = 0
                while i < len(processed_data):
                    print('!!!!!!!!!!!!', processed_data[i])
                    i += 1

    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True, port = 3030)
