library(rvest)
library(tidyverse)

urlImbd <- "https://www.imdb.com/title/tt2861424/awards/"

pag1 <- read_html(urlImbd)

año <- pag1 %>%
  html_elements(".ipc-metadata-list-summary-item__t") %>%
  html_text2() %>%
  {sapply(strsplit(., " "), "[[", 1)}

resultado <- pag1 %>%
  html_elements(".ipc-metadata-list-summary-item__t") %>%
  html_text2() %>%
  {sapply(strsplit(., " "), "[[", 2)}

premiacion <- pag1 %>%
  html_elements(".ipc-metadata-list-summary-item__t") %>%
  html_text2() %>%
  sapply(function(x) paste(strsplit(x, " ")[[1]][3:length(strsplit(x, " ")[[1]])], collapse = " "))

categoria <- pag1 %>%
  html_elements(".ipc-metadata-list-summary-item__li.awardCategoryName") %>%
  html_text2()

nominaciones <- data.frame(año, resultado, premiacion, categoria)
