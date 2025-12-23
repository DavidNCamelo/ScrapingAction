# Required Libraries
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)
library(tidyr)

# URL base
url <- "https://www.datos.gov.co/resource/68qj-5xux.json"

res <- GET(url)


# JSON
ubication_data <- fromJSON(
  content(res, "text", encoding = "UTF-8"),
  flatten = TRUE
)

ubication_data <- ubication_data |>
  select(
    c_digo_peaje,
    nombre_peaje,
    ubicaci_n,
    sector,
    sentido,
    url_foto.url,
    responsable,
    territorial,
    poste_de_referencia_pr,
    distancia_pr,
    point.coordinates
  ) |>
  mutate(
    longitud = map_dbl(point.coordinates, ~ .x[1]),
    latitud = map_dbl(point.coordinates, ~ .x[2])
  ) |>
  select(-point.coordinates)
