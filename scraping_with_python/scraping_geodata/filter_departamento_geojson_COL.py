"""
Created By David Camelo on 03/09/2025
Helped by ChatGPT

Script to extract public Colombia geojson shape
wihtout directly downloading dependency
Implementing a class and selecting segments
"""

# Required Libraries
import geopandas as gpd
import json
import argparse
import time
from filtering_geojson_Colombia import ArcGISDownloader

# Measure executio time
start_time = time.time()

# Console args
parser = argparse.ArgumentParser()
parser.add_argument(
    "--departamento", type=str, required=True, help="Nombre del departamento a filtrar"
)
args = parser.parse_args()

# Element to filter
departamento = args.departamento

BASE_URL = "https://services.arcgis.com/wLfHepIACaM0pwj9/ArcGIS/rest/services/MGN_MPIO_POLITICO_DANE/FeatureServer/0/query"

# Download all
downloader = ArcGISDownloader(BASE_URL)
geojson_data = downloader.download()

# Save temporal
tmp_file = "municipios.geojson"
with open(tmp_file, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False)

# Read geopandas
gdf = gpd.read_file(tmp_file, driver="GeoJSON")

# Filtering
gdf_departamento = gdf[gdf["DPTO_CNMBR"] == departamento]

# Save final result
salida = f"{departamento}_municipios.geojson"
gdf_departamento.to_file(salida, driver="GeoJSON")

# Total time
end_time = time.time()
elapsed = end_time - start_time

print(f"File saved in: {salida}")
print(f"Execution total time: {elapsed:.2f} segundos")
