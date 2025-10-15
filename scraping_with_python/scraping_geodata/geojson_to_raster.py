"""
Created By David Camelo on 14/10/2025
Helped by ChatGPT

Convert Geojson from Colombia in a Rasterfile
Considering each categorical layer as a band
of the raster file
"""

# --- Required Libraries ---
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import numpy as np
import argparse
import time
import json
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

# Define output raster path
output_raster = f"raster_{departamento.replace(' ', '_')}.tif"

# Define raster resolution (in degrees)
resolution = 0.01  # Ajusta según el nivel de detalle deseado

# Get bounds of the department
minx, miny, maxx, maxy = gdf_departamento.total_bounds

# Compute transform based on bounds and resolution
width = int((maxx - minx) / resolution)
height = int((maxy - miny) / resolution)
transform = from_bounds(minx, miny, maxx, maxy, width, height)

# --- Identify categorical columns --- #
# Exclude geometry and numeric columns
categorical_cols = [
    col
    for col in gdf_departamento.columns
    if gdf_departamento[col].dtype == "object" and col != "geometry"
]

print(f"Categorical columns to rasterize: {categorical_cols}")

# --- Encode categorical data as integers --- #
encoded_layers = {}
value_maps = {}

for col in categorical_cols:
    categories = gdf_departamento[col].astype("category")
    gdf_departamento[col + "_code"] = categories.cat.codes
    encoded_layers[col] = gdf_departamento[[col + "_code", "geometry"]]
    value_maps[col] = dict(enumerate(categories.cat.categories))

# --- Rasterize each categorical column as a band --- #
bands = []
for col in categorical_cols:
    shapes = (
        (geom, value)
        for geom, value in zip(
            encoded_layers[col]["geometry"], encoded_layers[col][col + "_code"]
        )
    )
    raster = rasterize(
        shapes=shapes,
        out_shape=(height, width),
        transform=transform,
        fill=-1,  # NODATA value
        dtype="int16",
    )
    bands.append(raster)

# --- Write multiband raster --- #
with rasterio.open(
    output_raster,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=len(bands),
    dtype="int16",
    crs=gdf_departamento.crs,
    transform=transform,
) as dst:
    for i, raster in enumerate(bands, start=1):
        dst.write(raster, i)
        dst.set_band_description(i, categorical_cols[i - 1])

print(f"\n✅ Raster file saved: {output_raster}")

# --- Optional: Save category mappings --- #
mapping_file = f"category_mappings_{departamento.replace(' ', '_')}.json"
with open(mapping_file, "w", encoding="utf-8") as f:
    json.dump(value_maps, f, ensure_ascii=False, indent=4)

print(f"📄 Category mappings saved: {mapping_file}")

# --- Execution time --- #
end_time = time.time()
print(f"\n⏱️ Execution time: {end_time - start_time:.2f} seconds")
