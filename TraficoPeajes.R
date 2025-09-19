# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)

# URL base
url <- "https://www.datos.gov.co/resource/8yi9-t44c.json"

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

# Convertir las columnas de fecha (si existen)
if ("desde" %in% names(df)) {
  df$desde <- as_date(df$desde)
}
if ("hasta" %in% names(df)) {
  df$hasta <- as_date(df$hasta)
}

# Ver estructura y guardar CSV
str(df)
head(df)
#write.csv(df, "D:/Descargas/data.csv", row.names = FALSE)
