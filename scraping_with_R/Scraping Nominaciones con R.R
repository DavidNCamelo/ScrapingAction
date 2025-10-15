library(rvest)
library(tidyverse)

#Link de wikipedia información nominaciones
urlwiki <- "https://es.wikipedia.org/wiki/Rick_y_Morty"

pag <- read_html(urlwiki)

tabla <- pag %>%
  html_nodes(".wikitable.sortable") %>%
  html_table(header = TRUE)

tabla <- bind_rows(tabla)
tabla <- tabla %>%
  select(-Ref.)

# Encuentra las filas que contienen "Temporada #"
filas_temporada <- grepl("Temporada \\d+", tabla$Año)

# Obtén los índices de las filas que contienen "Temporada #"
indices_temporada <- which(filas_temporada)

# Encuentra las filas que no contienen "Temporada #"
filas_nominaciones <- !filas_temporada

# Cree un vector de temporadas que se ajuste al número de filas de nominaciones
temporadas <- rep(
  tabla$Año[indices_temporada],
  times = diff(c(indices_temporada, length(tabla$Año) + 1))
)

# Agrega una columna "Temporada" con los valores correspondientes
tabla$Temporada <- temporadas[seq_along(filas_nominaciones)]


# Elimina las filas que contienen "Temporada #"
tabla <- tabla[filas_nominaciones, ]
