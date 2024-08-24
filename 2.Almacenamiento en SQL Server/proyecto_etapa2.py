import pyodbc
import pandas as pd
import logging
import re

# Configuración de logging
logging.basicConfig(filename='carga_datos.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Parametros para la conexion al servidor
server = 'LAPTOP-QAAK1ECU\\SQLEXPRESS'
database = 'Proyecto'
username = 'anrodriguezq'
password = 'andres17'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    logging.info("Conectando a los archivos csv...")
#conexion a los archivos csv en el disco local
    df = pd.read_csv('C:\\Users\\anfer\\OneDrive\\Documentos\\bootcamp\\Nueva carpeta 2\\proyecto etapa 3\\precios\\lista_S_P500.csv')
    datos = pd.read_csv('C:\\Users\\anfer\\OneDrive\\Documentos\\bootcamp\\Nueva carpeta 2\\proyecto etapa 3\\precios\\precios_S_P500.csv')
    
    logging.info("Leyendo archivo CSV...")
    if datos is not None:
#se eliminan los posibles espacios que hayan en los titulos de las columnas de los archivos csv
        df.columns = df.columns.str.strip()
        datos.columns = datos.columns.str.strip()
        
        logging.info(f"DataFrame headers: {list(datos.columns)}")
#se cambia el tipo de datos de la columna del archivo precios_S_P500.csv' por float ,ya que presenta
#problemas  al ser ingresada en la base de datos      
        datos['Close'] = datos['Close'].astype(float)
 
 #se abre la conexion a la base de datos        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
  #  Se usa el comando for index, row in df.iterrows()  para iterar sobre cada fila de un DataFrame de pandas, 
  # y dentro del bucle se asignan los valores de columnas específicas de cada fila a variables individuales para su procesamiento.  
        for index, row in df.iterrows():
            symbol = row['Symbol']
            company = row['Company']
            sector = row['Sector']
            headquarters = row['Headquarters']
            fecha_fundada = row['Fecha_fundada']
  #Se usa una expresion regular para encontrar 4 digitos de la columna fecha_fundada del archivo lista_S_P500.csv
  # para evitar problemas en la carga de esta 
            try:
                match = re.search(r'\d{4}', str(fecha_fundada))
                if match:
                    year_founded = match.group()
                else:
                    year_founded = None
            except Exception as e:
                logging.error(f"Error al extraer el año de fundación para {symbol}: {str(e)}")
                year_founded = None
 #Funcion para insertar datos a la base de datos CompanyProfiles 
            insert_query = '''
            IF NOT EXISTS (SELECT 1 FROM CompanyProfiles WHERE Symbol = ?)
            BEGIN
                INSERT INTO CompanyProfiles (Symbol, Company, Sector, Headquarters, Fecha_fundada)
                VALUES (?, ?, ?, ?, ?)
            END
            '''
            cursor.execute(insert_query, symbol, symbol, company, sector, headquarters, year_founded)
            conn.commit()

            logging.info(f"Inserción exitosa en CompanyProfiles: {symbol} - {company}")

        logging.info("Datos insertados correctamente en la tabla CompanyProfiles.")

        logging.info("Insertando registros en la tabla Companies...")
        for index, row in datos.iterrows():
            date = row['Date']
            symbol = row['Symbol']
            close = row['Close']

#Funcion para insertar datos a la base de datos Companies 
            insert_query = '''
            IF NOT EXISTS (SELECT 1 FROM Companies WHERE Date = ? AND Symbol = ?)
            BEGIN
                INSERT INTO Companies (Date, Symbol, [Close])
                VALUES (?, ?, ?)
            END
            '''
            cursor.execute(insert_query, date, symbol, date, symbol, close)
            conn.commit()

            logging.info(f"Inserción exitosa en Companies: {date} - {symbol}")

        logging.info("Datos insertados correctamente en la tabla Companies.")

except Exception as e:
    logging.error(f"Error en la carga de datos: {str(e)}")

finally:
    try:
#se cierra loa coneccion a la base de datos 
        cursor.close()
        conn.close()
        logging.info("Conexión cerrada.")
    except Exception as e:
        logging.error(f"Error al cerrar la conexión: {str(e)}")
