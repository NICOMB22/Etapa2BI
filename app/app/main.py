from flask import Flask, render_template, request, make_response
import requests
import pandas as pd
import io
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])

def predict():
    if 'csv_file' in request.files:
        csv_file = request.files['csv_file']

        if csv_file:
            # Guardar el archivo CSV en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".csv") as temp_csv:
                csv_file.save(temp_csv.name)

            # Hacer una solicitud HTTP al endpoint que retorna un CSV
            api_endpoint = 'http://127.0.0.1:8000/predict'
            response = requests.post(api_endpoint, files={'csv_file': open(temp_csv.name, 'rb')})
            
            # Verificar si la respuesta es un archivo CSV
            if 'text/csv' in response.headers.get('content-type', ''):
                csv_data = response.content

                # Devolver el archivo CSV para descargar
                response = make_response(csv_data)
                response.headers["Content-Disposition"] = "attachment; filename=resultado.csv"
                response.headers["Content-Type"] = "text/csv"

                return response

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)