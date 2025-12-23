# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)

# URL base (nuevo recurso)
url <- "https://www.datos.gov.co/resource/68qj-5xux.json"

res <- GET(url)


# Parsear JSON
ubication_data <- fromJSON(
  content(res, "text", encoding = "UTF-8"),
  flatten = TRUE
)

ubication_data
