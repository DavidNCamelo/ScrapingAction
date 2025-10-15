#Realizar la extracción del excel de divipola del dane a través de R

#Llamar liberías necesarias
library(httr)
library(readxl)

#Llamar la ubicación del archivo en la página del dane
#Considerando su origen en https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/?cod=112
#Con el respectivo "href" del árbol html del archivo deseado
url <- "https://geoportal.dane.gov.co/descargas/divipola/DIVIPOLA_Municipios.xlsx"

#En caso de ser necesario implementar los headers requeridos en scraping
headers <- c(
  "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
)

#Revisar que el response esté correcto
response <- GET(url, add_headers(headers))
#response
#Tranformar el contenido en raw para eectos de extracción
contenido <- content(response, as = "raw")

#Crear el archivo virtual para evitar descarga en equipo local
tmpfile <- tempfile(fileext = ".xlsx")
writeBin(contenido, tmpfile)

#crear el dataframe con el excel generado
municipios <- read_xlsx(tmpfile, sheet = 1, range = "A11:G1132")
municipios
