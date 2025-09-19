import geopandas as gpd

# Archivo original con todos los municipios
# Este archivo proviene de https://www.datos.gov.co/Geograf-a/MGN_MPIO_POLITICO/97mf-4j4h
# y https://www.arcgis.com/home/item.html?id=129f3fe8e3424cc7ba3fc19ff1522026
# y fue descargado el 24 de junio de 2024
archivo = "base_data/MGN_MPIO_POLITICO - copia.geojson"

# Cargar los datos
gdf = gpd.read_file(archivo, driver="GeoJSON")

# Definir el departamento que quieres filtrar
departamento = "GUAINÍA"

# Filtrar todos los municipios de ese departamento
gdf_departamento = gdf[gdf["DPTO_CNMBR"] == departamento]

# Guardar como nuevo GeoJSON
salida = f"{departamento}_municipios.geojson"
gdf_departamento.to_file(salida, driver="GeoJSON")

print(f"Archivo guardado en: {salida}")
