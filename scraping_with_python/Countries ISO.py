import pandas as pd
import requests

# URL del archivo CSV
url = "https://gist.githubusercontent.com/ideaalab/7caf20bc8fd6c625163927e2d478e05f/raw/b49e20c16ed35e3295c0442d4b85a13eea645cee/paises.csv"

# Realiza la solicitud GET
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Guarda el contenido de la respuesta en un archivo local
    with open("paises.csv", "wb") as f:
        f.write(response.content)
    print("El archivo se ha descargado correctamente como 'paises.csv'")

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv("paises.csv")

    # Muestra una muestra del DataFrame (las primeras 5 filas)
    print("Muestra del contenido del archivo CSV:")
    print(df.head())
else:
    print("No se pudo descargar el archivo. Código de estado:", response.status_code)

df.to_csv("D:\Descargas\countries.csv", index=False)
