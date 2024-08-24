# Analisis de acciones del índice S&P 500
Este proyecto analiza datos financieros del índice S&P 500  en cuatro fases: extracción de datos y precios de cotización , almacenamiento en SQL Server, creación de un dashboard en Power BI con KPIs y bookmarks, y clusterización de las acciones según su volatilidad para identificar patrones similares entre las empresas.

## Requisitos
- Python 3.x
- Librerías: `pandas`, `pyodbc`, `scikit-learn`, `requests`, `BeautifulSoup`, `yfinance`, `logging`, `Altair`.
- Power BI Desktop
- SQL Server

## Estructura del proyecto


**Primera fase: "1: Extracción de datos"**  
Esta carpeta contiene un script llamado `proyecto_etapa1`, el cual permite extraer los datos de las empresas y guardarlos en archivos CSV. También incluye un archivo de texto llamado `requirements.txt`, que contiene las librerías necesarias para usar el script, y la carpeta `data`, que almacena los productos generados por el script `proyecto_etapa1`.

**Segunda fase: "2: Almacenamiento de datos en SQL Server"**  
Esta carpeta contiene un archivo SQL llamado `Base de datos`, que define la estructura de la base de datos para almacenar los archivos CSV producidos en la primera fase. Además, incluye un script llamado `proyecto_etapa2`, el cual permite insertar los datos de los CSV en las bases de datos creadas con el archivo SQL. También incluye un archivo de texto `requirements.txt`, que contiene las librerías necesarias para usar el script de esta fase, y la carpeta `data`, que almacena los productos generados por el script `proyecto_etapa2`.

**Tercera fase: "3: Creación del dashboard en Power BI"**  
Esta carpeta contiene un archivo de Power BI ,llamado `proyecto_etapa3`, con un dashboard que presenta análisis de métricas estadísticas de los datos de las empresas del índice S&P 500.

**Cuarta fase: "4: Clusterización de las Acciones"**  
Esta carpeta contiene un script llamado `proyecto_etapa4`, que analiza las empresas del índice S&P 500, desglosa las métricas de volatilidad y, con base en ellas, divide las acciones de las empresas en tres grupos mediante un proceso de clusterización, con su respectivo análisis.

## Instrucciones de Instalación y Uso


**Paso 1: Configuración del Entorno Virtual**

1. **Crear un entorno virtual:**

   Para crear un entorno virtual, se debe abrir la terminal (o símbolo del sistema) y navegar hasta la carpeta donde se desea crear el proyecto. Luego, se ejecuta el comando correspondiente para crear el entorno virtual.

2. **Activar el entorno virtual:**
   - En Windows, se debe ejecutar un comando en la terminal para activar el entorno virtual.
   - En macOS/Linux, se utiliza un comando diferente para activarlo.

3. **Instalar las librerías necesarias utilizando pip:**

   Es importante asegurarse de que el entorno virtual esté activado antes de instalar las librerías necesarias, como pandas, numpy, matplotlib, seaborn, scikit-learn, sqlalchemy, pyodbc, requests, y beautifulsoup4.


4. **Usar los parámetros para activar la función `etl_process`:**

   Se configuran los argumentos de **ticker** (link de S&P 500 de wikipedia) y **period** para guardar la lista de las empresas y los precios transformados del S&P 500 en archivos CSV.

**Paso 2: Carga de Datos (LOAD) a SQL Server**

1. **Cargar la base de datos en SQL Server:**

   Se cargan las bases de datos en SQL Server para almacenar los datos de las empresas del S&P 500, incluyendo los datos de perfil de empresa y precios históricos.

2. **Conectar y cargar los datos a SQL Server usando pyodbc:**

   Se utiliza **pyodbc** para cargar los datos transformados en la base de datos de SQL Server, configurando los parámetros del servidor SQL con las bases de datos, por medio de los archivos CSV.

**Paso 3: Desarrollo del Dashboard en Power BI**

1. **Configurar Power BI Desktop e importar los datos desde SQL Server:**

   Se debe abrir Power BI Desktop y conectarse a la base de datos SQL Server para seleccionar las tablas necesarias para el análisis.

**Paso 4: Clusterización de Empresas del S&P 500**

1. **Configurar el entorno de trabajo en Google Colab:**

   Se accede a Google Colab desde una cuenta de Google y se carga el script de la fase 4.

2. **Instalar y cargar las librerías necesarias en Google Colab:**

   En la primera celda del cuaderno, se instalan las librerías necesarias como pandas, numpy, matplotlib, seaborn, altair, y scikit-learn.

3. **Importar el archivo CSV con precios diarios y realizar la clusterización:**

   Se carga el archivo CSV con los precios históricos y se calculan métricas de volatilidad utilizando pandas. Luego, se aplica un modelo de clusterización (K-means) utilizando scikit-learn.


## Fases del Proyecto

**Fase 1: Extracción de Datos**
- Obtención de datos de empresas del S&P 500 desde Wikipedia.
- Descarga de los precios de cotización del último año.

**Fase 2: Almacenamiento en SQL Server**
- Carga de los datos limpios en una base de datos SQL Server.

**Fase 3: Dashboard en Power BI**
- Creación de un dashboard interactivo con KPIs, tooltips y bookmarks.

**Fase 4: Clusterización de las Acciones**
- Agrupamiento de las acciones en clusters según indicadores de volatilidad.

