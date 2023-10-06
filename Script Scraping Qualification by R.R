library(rvest)
library(tidyverse)

base_url <- "https://www.imdb.com/title/tt2861424/episodes"  # URL de la página principal

#Como se está haciendo barrido por categoría de temporadas
#Se usará este como elemtento de navegación horizontal
season <- 1 #Temporada incial
max_season <- 5 #Temporadad donde se desea terminar de exportar data
titulos <- c() #Vector de almacenamiento de datos de título del capítulo
calificacioness <- c() #Vector de almacenamiento de calificación obtenida
votos <- c() #Vector de almacenamiento de votos recibidos

while (season <= max_season) { #Inicio de comando de navegación
  
  url <- paste0(base_url,"/?season=",season) #Conformación de url completa de navegación
  page <- read_html(url) #Conversión y lectura correcta de html
  
  #Extraer títulos de capitulos
  titulo <- page %>% 
    html_elements("h4") %>% #Esta es la sección html que contiene lo que deseamos
    html_text2() %>%
    gsub("\\.", "", .) %>%  #Reemplazar el punto intermedio por nada para mantener
                            #limpio el texto
    {sapply(strsplit(., " ∙"), "[[", 1)} %>% #El nombre del título se hace innecesario
                                        #Se busca el separador y selecciona
                                        #la parte a extraer
    gsub("S(\\d)E(\\d)", "S0\\1E0\\2", .)
  titulos <- c(titulos, titulo) #guardar datos consecutivos
  
  #Extraer calificación obtenida e IMBD
  calificaciones <- page %>%
    html_elements(".sc-1318654d-12") %>% #Sección html que contiene lo que deseamos
    html_text2() %>%
    {gsub("\\Rate", "", .)} %>% #Eliminar Rate del contenido
    {gsub("\\(", "", .)} %>% #Eliminar el primer paréntesis del contenido
    {gsub("\\)", "", .)} #Eliminar el segundo paréntesis del contenido
  
  calificaciones <- strsplit(calificaciones, " ") #Separar elmentos desde el espacio
  
  calificacioness <- c(calificacioness, sapply(calificaciones, "[[", 1))
  
  votos <- c(votos, sapply(calificaciones, "[[", 2))
  
  season <- season + 1 #ir a la siguiente temporada
}
#Crear dataframe con los datos exportados
titycalif <- data.frame(titulos, calificacioness, votos)