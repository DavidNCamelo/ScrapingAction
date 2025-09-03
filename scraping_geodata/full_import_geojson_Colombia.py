''' 
Created By David Camelo on 03/09/2025
Helped by ChatGPT

Script to extract public Colombia geojson shape
wihtout directly downloading dependency  
'''

# Required libraries
import requests
import json

BASE_URL = "https://services.arcgis.com/wLfHepIACaM0pwj9/ArcGIS/rest/services/MGN_MPIO_POLITICO_DANE/FeatureServer/0/query"

params = {
    "where": "1=1",
    "outFields": "*",
    "outSR": "4326",
    "f": "geojson",
    "resultOffset": 0,
    "resultRecordCount": 2000 # Actaully is possible will exist more records
                                # Is important considerate the total of "Municipios"
}

features = []

while True:
    print(f"Descargando desde offset {params['resultOffset']}...")

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "features" not in data or len(data["features"]) == 0:
        break

    features.extend(data["features"])
    params["resultOffset"] += params["resultRecordCount"]

print(f"\nTotal de entidades descargadas: {len(features)}\n")

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# 👉 imprime en pantalla como texto JSON bonito
print(json.dumps(geojson, indent=2, ensure_ascii=False))
