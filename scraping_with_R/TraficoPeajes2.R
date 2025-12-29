# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(tidyr)
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
df1 <- bind_rows(all_data)

# Asegurar que 'anio' sea numérico
if ("anio" %in% names(df1)) {
  df1$anio <- as.integer(df1$anio)
}
df1 <- df1 |>
  select(
    estacion_de_peaje,
    anio,
    mes,
    codigo_estacion,
    departamento,
    starts_with(c("trafico", "evasores", "exentos"))
  )

# deleting columns
df2 <- df1 |>
  select(-ends_with('_total'))

# Pivoting

df2 <- df2 |>
  pivot_longer(
    cols = c(
      starts_with("trafico_efectivo_"),
      starts_with("evasores_unidad_"),
      starts_with("exentos_ley_787_2002_")
    ),
    names_to = c(".value", "categoria"),
    names_pattern = "(trafico_efectivo|evasores_unidad|exentos_ley_787_2002)_(.*)"
  ) |>
  mutate(
    across(
      c(trafico_efectivo, evasores_unidad, exentos_ley_787_2002),
      ~ replace_na(as.numeric(.x), 0)
    )
  )

# Revisar estructura
str(df1)
str(df2)
head(df2)

# Guardar CSV si lo necesitas
# write.csv(df, "D:/Descargas/data_tcfu_jngt.csv", row.names = FALSE)
