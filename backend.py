from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/get_demolition_date', methods=['POST'])
def get_demolition_date():
    # Daten aus dem POST-Request extrahieren
    address = request.json.get('address')
    base_url = "https://api3.geo.admin.ch/rest/services/api/SearchServer?"
    parameters = {
        "searchText": address,
        "origins": "address",
        "type": "locations",
    }
    url = f"{base_url}{urllib.parse.urlencode(parameters)}"

    # EGID über GeoAdmin API abfragen
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Verwendung deiner Methode zur Extraktion der EGID
        df = pd.DataFrame.from_dict(list(data.values())[0][0], orient='columns')
        egid = df.iloc[[1], :1].values[0][0]  # Annahme, dass das korrekte EGID extrahiert wird

        # EGID verwenden, um das Abbruchdatum zu finden
        csv_path = '/Users/mariusaffolter/Documents/200_Studium/220_Semester/24FS/Einsatz Geodaten Marketing/Project/apartment_analysis_egm/prediction_bestehende_wohnungen.csv'  # Pfad anpassen
        df_csv = pd.read_csv(csv_path)
        demolition_date = df_csv[df_csv['EGID'] == egid]['Predicted Year of Demolition'].values[0]
        return jsonify({'demolition_date': demolition_date})
    else:
        return jsonify({'error': 'Address not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
