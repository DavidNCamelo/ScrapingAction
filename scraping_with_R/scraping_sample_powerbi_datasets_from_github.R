# Queda pendiente hacer revisión sobre cómo abrir excel encriptados con power pivot
# Librerías necesarias
library(httr)
library(readxl)

# Es posible cambiar de carpetas a usar
# Después de main/
FOLDER <- c('AdventureWorks%20Sales%20Sample', 'powerbi-service-samples')

# Y los archivos en .xlsx

FILE <- list(
  'AdventureWorks%20Sales%20Sample' = c('AdventureWorks%20Sales%20Sample.xlsx'),
  'powerbi-service-samples' = c(
    'Human%20Resources%20Sample-no-PV.xlsx',
    'IT%20Spend%20Analysis%20Sample-no-PV.xlsx',
    'Opportunity%20Tracking%20Sample%20no%20PV.xlsx',
    'Procurement%20Analysis%20Sample-no-PV.xlsx',
    'Retail%20Analysis%20Sample-no-PV.xlsx',
    'Sales%20and%20Marketing%20Sample-no-PV.xlsx',
    'Supplier%20Quality%20Analysis%20Sample-no-PV.xlsx'
  )
)

# Seleccionar carpeta
selected_folder <- FOLDER[2]

# Seleccionar archivo
selected_file <- FILE[[selected_folder]][2]

# Url base
base_url <- 'https://github.com/microsoft/powerbi-desktop-samples/raw/refs/heads/main/'

# Pegar url completo para seleccionar dataset
final_url <- paste0(base_url, selected_folder, "/", selected_file)

# Obtener respuesta de acceso
res <- GET(final_url)

# Descargar el archivo a un archivo temporal
temp_file <- tempfile(fileext = ".xlsx")
GET(final_url, write_disk(temp_file, overwrite = TRUE))

# Listar hojas disponibles
sheets <- c(excel_sheets(temp_file))

# Leer una hoja específica, necesario para entorno de power bi y poder crear el modelo de datos
df <- read_excel(temp_file, sheet = sheets[2]) # Usa el nombre exacto de la hoja

# Ver los primeros datos
head(df)
