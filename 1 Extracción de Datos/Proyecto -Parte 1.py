import pyodbc
import pandas as pd
import logging
import re
import os
import requests
from bs4 import BeautifulSoup
import yfinance as yf  # Importa yfinance para descargar datos históricos

# Configuración de logging
logging.basicConfig(filename='carga_datos.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Definir los parámetros de conexión
server = 'LAPTOP-QAAK1ECU\\SQLEXPRESS'  # Asegúrate de usar \\ para escapar el backslash en el nombre del servidor
database = 'Project'
username = 'anrodriguezq'
password = 'andres17'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def extraccion_datos_url(url):
    try:
        wikipedia = requests.get(url)
        soup = BeautifulSoup(wikipedia.text, 'html.parser')
        data = soup.find_all("table")[0]
        df_S_P500 = pd.read_html(str(data))[0]
        df_S_P500 = df_S_P500[['Símbolo', 'Seguridad', 'Sector GICS', 'Ubicación de la sede', 'Fundada']].rename(
            columns={"Seguridad": "Company", "Símbolo": "Symbol",
                     "Sector GICS": "Sector", "Ubicación de la sede": "Headquarters", "Fundada": "Fecha_fundada"})
        return df_S_P500
    except Exception as e:
        logging.error(f"Error al procesar y guardar datos de S&P 500: {e}")
        return None

def extract_and_transform_data(df, period):
    try:
        logging.info(f'Extrayendo y transformando datos para el período {period}')
        dat = []
        for i in df['Symbol']:
            da = yf.download(i, period=period)
            da['Symbol'] = i
            dat.append(da)
        data = pd.concat(dat)
        df = data[['Symbol', 'Close']].reset_index()
        df.dropna(inplace=True)
        logging.info('Datos extraídos y transformados exitosamente')
        return df
    except Exception as e:
        logging.error(f'Error extrayendo o transformando datos para {df}: {e}')
        return None

# URL para extraer datos de S&P 500
url = 'https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500'

try:
    # Extraer datos desde la URL y guardar en CSV
    df = extraccion_datos_url(url)
    datos = extract_and_transform_data(df, "3mo")
    if datos is not None:
        # Establecer conexión con la base de datos
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Asegurar que los nombres de las columnas no tengan espacios adicionales
        df.columns = df.columns.str.strip()

        # Iterar sobre las filas del DataFrame y insertar en la tabla CompanyProfiles
        for index, row in df.iterrows():
            symbol = row['Symbol']
            company = row['Company']
            sector = row['Sector']
            headquarters = row['Headquarters']
            fecha_fundada = row['Fecha_fundada']

            # Extraer solo el año de fundación utilizando expresiones regulares
            try:
                match = re.search(r'\d{4}', str(fecha_fundada))
                if match:
                    year_founded = match.group()
                else:
                    year_founded = None
            except Exception as e:
                logging.error(f"Error al extraer el año de fundación para {symbol}: {str(e)}")
                year_founded = None

            # Insertar los datos en la base de datos
            insert_query = '''
            INSERT INTO CompanyProfiles (Symbol, Company, Sector, Headquarters, Fecha_fundada)
            VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_query, symbol, company, sector, headquarters, year_founded)
            conn.commit()

            logging.info(f"Inserción exitosa en CompanyProfiles: {symbol} - {company}")

        logging.info("Datos insertados correctamente en la tabla CompanyProfiles.")

        # Iterar sobre las filas del DataFrame datos y insertar en la tabla Companies
        for index, row in datos.iterrows():
            date = row['Date'].strftime('%Y-%m-%d')  # Formatear la fecha como string
            symbol = row['Symbol']
            close = row['Close']

            # Insertar los datos en la base de datos
            insert_query = '''
            INSERT INTO Companies (Date, Symbol, [Close])
            VALUES (?, ?, ?)
            '''
            cursor.execute(insert_query, date, symbol, close)
            conn.commit()

            logging.info(f"Inserción exitosa en Companies: {date} - {symbol}")

        logging.info("Datos insertados correctamente en la tabla Companies.")

except Exception as e:
    logging.error(f"Error en la carga de datos: {str(e)}")

finally:
    # Cerrar la conexión
    cursor.close()
    conn.close()

