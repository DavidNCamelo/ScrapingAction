# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)

# URL base
url <- "https://www.datos.gov.co/resource/68qj-5xux.json"

# Parámetros iniciales
limit <- 1000
offset <- 0
all_data <- list()

repeat {
  # Hacer la solicitud GET
  res <- GET(url, query = list("$limit" = limit, "$offset" = offset))
  
  # Verificar código de estado
  if (status_code(res) != 200) {
    message("Error en la solicitud: ", status_code(res))
    break
  }
  
  # Parsear el contenido como lista
  data <- fromJSON(content(res, "text", encoding = "UTF-8"), flatten = TRUE)
  
  # Salir del bucle si no hay datos
  if (length(data) == 0) {
    break
  }
  
  # Agregar al acumulador
  all_data <- append(all_data, list(data))
  
  # Incrementar offset
  offset <- offset + limit
}

# Combinar todos los bloques de datos en un solo data frame
df <- bind_rows(all_data)

# Ver los nombres de las columnas
print(colnames(df))

# Filtrar columnas deseadas
df2 <- df[c("nombre_peaje", "ubicaci_n", "c_digo_peaje", "c_digo_tramo", "latitud", "longitud")]

# Revisar si el filtrado funcionó
print(colnames(df2))

# Ver muestra
print(head(df2))
