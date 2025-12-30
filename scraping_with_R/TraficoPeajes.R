# Librerías necesarias
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)
library(purrr)
library(stringr)

# URL base
url <- "https://www.datos.gov.co/resource/8yi9-t44c.json"

# Parámetros
limit <- 1000
all_data <- list()

# Rango temporal: 2014 → hoy (por mes)
start_dates <- seq(
  from = as.Date("2014-01-01"),
  to = Sys.Date(),
  by = "month"
)

end_dates <- c(start_dates[-1] - 1, Sys.Date())

# Bucle por rangos de fecha
for (i in seq_along(start_dates)) {
  offset <- 0

  repeat {
    res <- GET(
      url,
      query = list(
        "$limit" = limit,
        "$offset" = offset,
        "$where" = paste0(
          "desde >= '",
          start_dates[i],
          "' AND desde <= '",
          end_dates[i],
          "'"
        )
      )
    )

    if (status_code(res) != 200) {
      message("Error en la solicitud: ", status_code(res))
      break
    }

    data <- fromJSON(
      content(res, "text", encoding = "UTF-8"),
      flatten = TRUE
    )

    if (length(data) == 0) {
      break
    }

    all_data <- append(all_data, list(data))
    offset <- offset + limit
  }
}

# Combinar todos los bloques
df <- bind_rows(all_data)

# Transformaciones que YA tenías
if ("desde" %in% names(df)) {
  df$desde <- as_date(df$desde)
}
if ("hasta" %in% names(df)) {
  df$hasta <- as_date(df$hasta)
}

# Reorganizing columns
df <- df |>
  mutate(
    anio = as.integer(year(desde)),
    mes = str_to_title(month(desde, label = TRUE, abbr = FALSE))
  ) |>
  select(-desde, -hasta)

# Verificación
str(df)
head(df)
#write.csv(df, "D:/Descargas/data.csv", row.names = FALSE)
