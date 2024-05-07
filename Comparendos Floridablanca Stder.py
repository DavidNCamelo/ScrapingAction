import pandas as pd
import requests
from io import StringIO

#Definir función de extracción con scrapíng puesto que entraremos a varios links
#Adicional la API de datos.gov.co (Socrata) tiene un límite de 1000 filas, por lo cuál se debe ingresar por 
#peticiones a través de filtros

def exported(base_url, treat_serial_as_str=False):
    #Acceder al link desado
    response = requests.get(base_url)
    # Obtener el año actual
    current_year = pd.to_datetime("today").year

    # Crear una lista para almacenar los DataFrames por año
    dataframes = []

    # Iterar a través de los años desde 2019 hasta el año actual
    for year in range(2019, current_year + 1):
        # Construir la URL para el año actual
        year_url = f"{base_url}?$where=fecha between '{year}-01-01T00:00:00' and '{year}-12-31T00:00:00'&$limit=10000000"
        # Realizar una solicitud GET a la URL y obtener el contenido del CSV
        response = requests.get(year_url)

        # Crear un DataFrame a partir del contenido del CSV
        df = pd.read_csv(StringIO(response.text))

        # Agregar el DataFrame a la lista
        dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    data = pd.concat(dataframes, ignore_index=True)
    data.columns = map(str.upper, data.columns)
    data["FECHA"] = pd.to_datetime(data["FECHA"])

    return data

#Como hay un documento con el campo de fecha nombrado de forma diferente, es necesario "duplicar" la función para poder
#interactuar con este

def exported2(base_url):
    #Acceder al link desado
    response = requests.get(base_url)
    # Obtener el año actual
    current_year = pd.to_datetime("today").year

    # Crear una lista para almacenar los DataFrames por año
    dataframes = []

    # Iterar a través de los años desde 2019 hasta el año actual
    for year in range(2019, current_year + 1):
        # Construir la URL para el año actual
        year_url = f"{base_url}?$where=fecha_comp between '{year}-01-01T00:00:00' and '{year}-12-31T00:00:00'&$limit=10000000"
        # Realizar una solicitud GET a la URL y obtener el contenido del CSV
        response = requests.get(year_url)

        # Crear un DataFrame a partir del contenido del CSV
        df = pd.read_csv(StringIO(response.text))

        # Agregar el DataFrame a la lista
        dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    data = pd.concat(dataframes, ignore_index=True)
    data.columns = map(str.upper, data.columns)
    data["FECHA_COMP"] = pd.to_datetime(data["FECHA_COMP"])

    return data

#Documento 1, con información disponible desde el 2022 y casi llegando a fecha actual del 2024
url = "https://www.datos.gov.co/resource/e7nm-5ibv.csv"
#Implementar función creada para extraer la información y crear dataframe
comparendos1 = exported(url)

#La primera extracción transforma carácteres especiales en _, por lo que se renombran para mayor facilidad de uso y distinción
comparendos1 = comparendos1.rename(columns={"INFRACCI_N": "INFRACCION",
                                            "LUGAR_INFRACCI_N": "LUGAR INFRACCION"})

#Con la intención de juntar los 3 documentos en un solo dataframe, en éste se crea un index para identificar 
#los comparendos de forma única, basados en la fecha en que se impusieron
comparendos1["fcid"] = comparendos1["FECHA"].astype(str).str.replace('-', '').astype(int)

#comparendos1.info()
# Inicializar un contador para agregar caracteres numéricos únicos
contador = 1

# Función para generar el índice único basado en la fecha y el contador
def generar_id(fecha):
    global contador
    id_unico = str(fecha) + str(contador).zfill(4)
    contador += 1
    return id_unico
#Action

# Aplicar la función a la columna 'fcid creado para la nueva columna 'COMPARENDO'
comparendos1['COMPARENDO'] = comparendos1['fcid'].apply(generar_id)

#Agregar una columna en nulos, que puede interesar dado que estás disponible en los otros 2 archivos
comparendos1["PLACA"] = None

#Poner en mayúsculas los valores de las siguientes columnas, para unificar formatos con los demás documentos
comparendos1["SERVICIO"] = comparendos1["SERVICIO"].str.upper()
comparendos1["ESTADO"] = comparendos1["ESTADO"].str.upper()

#Seleccionar columnas deseadas y de interés
comparendos1 = comparendos1[["COMPARENDO", "FECHA", "CLASE", "SERVICIO", "ESTADO", "INFRACCION", "PLACA"]]

#Documento 2, con información disponible desde el 2020
url2 = "https://www.datos.gov.co/resource/rfag-apa4.csv"
#Implementar función creada para extraer la información y crear dataframe
comparendos2 = exported(url2)

#Agregar columnas requeridas y llenar con valores nulos para incluirlas dentro del documento final
comparendos2["CLASE"] = None
comparendos2["ESTADO"] = None
comparendos2["SERVICIO"] = None

#Seleccionar columnas desdeadas
comparendos2 = comparendos2[["COMPARENDO", "FECHA", "CLASE", "SERVICIO", "ESTADO", "INFRACCION", "PLACA"]]

#Documento 3, con información del 2021
url3 = "https://www.datos.gov.co/resource/wmr7-xdpj.csv"
#Implementar función creada para extraer la información y crear dataframe
comparendos3 = exported2(url3)

#Renombrar columnas deseadas para normalizarlas acorde a los demás archivos
comparendos3 = comparendos3.rename(columns= {"FECHA_COMP": "FECHA",
                                             "NRO_COMPARENDO": "COMPARENDO"})
#Seleccionar columnas deseadas
comparendos3 = comparendos3[["COMPARENDO", "FECHA", "CLASE", "SERVICIO", "ESTADO", "INFRACCION", "PLACA"]]

full_doc = pd.concat([comparendos2, comparendos3, comparendos1], ignore_index= True)

full_doc.info()

#full_doc.head()