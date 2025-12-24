# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)

# URL base (nuevo recurso)
url <- "https://www.datos.gov.co/resource/tcfu-jngt.json"

# Parámetros de paginación
limit <- 1000
offset <- 0
all_data <- list()

repeat {
  # Solicitud GET con paginación
  res <- GET(
    url,
    query = list(
      "$limit" = limit,
      "$offset" = offset
    )
  )

  # Verificar estado
  if (status_code(res) != 200) {
    message("Error en la solicitud: ", status_code(res))
    break
  }

  # Parsear JSON
  data <- fromJSON(
    content(res, "text", encoding = "UTF-8"),
    flatten = TRUE
  )

  # Salir si no hay más registros
  if (length(data) == 0) {
    break
  }

  # Acumular
  all_data <- append(all_data, list(data))

  # Avanzar offset
  offset <- offset + limit
}

# Unir todo en un solo data frame
df <- bind_rows(all_data)

# Asegurar que 'anio' sea numérico
if ("anio" %in% names(df)) {
  df$anio <- as.integer(df$anio)
}

# (Opcional) Filtrar desde 2005 por seguridad
df <- df %>%
  filter(is.na(anio) | anio >= 2005)

df <- df |>
  select(
    estacion_de_peaje,
    anio,
    mes,
    codigo_estacion,
    departamento,
    starts_with(c("trafico", "evasores", "exentos"))
  )

# Revisar estructura
str(df)
head(df)

# Guardar CSV si lo necesitas
# write.csv(df, "D:/Descargas/data_tcfu_jngt.csv", row.names = FALSE)
