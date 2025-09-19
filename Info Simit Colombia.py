import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import re

# Extraer información sobre las infracciones directamente desde el simit de Colombia

url_comparendos = "https://www.comparendossimit.com/infracciones-de-transito-colombia/"

encabezado = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Este encabezado puede ser genérico sin embargo hay que indagar si presenta modificaciones según caso de uso

datos = requests.get(url_comparendos, headers=encabezado)

datos2 = html.fromstring(datos.text)
soup = bs(datos.text, "html.parser")
cods = []
# Encuentra todos los elementos con la clase "mtr-cell-content"
codigos = soup.find_all(class_="mtr-cell-content")
for codigo in codigos:
    l = codigo.text  # Usa el atributo text, no una función
    cods.append(l)
# print(cods)

tripleta = [cods[i : i + 3] for i in range(3, len(cods), 3)]

Costos = pd.DataFrame(tripleta, columns=["CÓDIGO", "TIPO DE INFRACCIÓN", "VALOR"])


# Para casos funcionales, es mejor mantener la primera columna siempre de 3 carácteres
# Función para formatear los valores de la primera columna
def formatear_codigo(valor):
    partes = re.match(r"([A-Za-z]+)(\d+)", valor)
    if partes:
        prefijo = partes.group(1)
        numero = int(partes.group(2))
        if numero < 10:
            numero_formateado = f"0{numero}"
        else:
            numero_formateado = str(numero)
        return f"{prefijo}{numero_formateado}"
    return valor


# Aplicar la función a la primera columna del DataFrame
Costos["CÓDIGO"] = Costos["CÓDIGO"].apply(formatear_codigo)

Costos.info()

Costos.head()
