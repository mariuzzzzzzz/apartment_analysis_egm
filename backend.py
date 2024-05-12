from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import urllib.parse
import requests
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

@app.route('/get_demolition_date', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_demolition_date():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

    # Extract data from the POST request
    address = request.json.get('address')
    base_url = "https://api3.geo.admin.ch/rest/services/api/SearchServer?"
    parameters = {
        "searchText": address,
        "origins": "address",
        "type": "locations",
    }
    url = f"{base_url}{urllib.parse.urlencode(parameters)}"

    # Query EGID via GeoAdmin API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            feature_id = results[0]['attrs']['featureId']
            egid = feature_id.split('_')[0]

            csv_path = './prediction_bestehende_wohnungen.csv'
            df_csv = pd.read_csv(csv_path)
            df_csv['EGID'] = df_csv['EGID'].astype(str)
            filtered_df = df_csv[df_csv['EGID'] == egid]
        
            if not filtered_df.empty:
                demolition_date = int(filtered_df['Predicted Demolition Year'].values[0])
                return jsonify({'demolition_date': demolition_date}), 200
            else:
                return jsonify({'demolition_date': "N/A"}), 404
        else:
            return jsonify({'demolition_date': "N/A"}), 404
    else:
        return jsonify({'demolition_date': "N/A"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
