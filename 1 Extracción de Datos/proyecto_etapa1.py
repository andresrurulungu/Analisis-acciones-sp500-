import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import os
import logging
from prophet import Prophet

log_dir = './logs'
data_dir = './data'

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

log_filename = os.path.join(log_dir, 'etl_process.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
"""La función `extraccion_datos_url` obtiene datos desde la API de una URL, en este caso, Wikipedia. Utiliza `BeautifulSoup` 
para realizar web scraping y selecciona la primera tabla de la página. Luego,  se renombran las columnas  y se guardan en un archivo CSV llamado `lista_S_P500.csv` en el directorio `data_dir`.
La función retorna los datos para su uso posterior en el proceso ETL."""

def extraccion_datos_url(url):
    try:
        wikipedia = requests.get(url)
        soup = BeautifulSoup(wikipedia.text, 'html.parser')
        data = soup.find_all("table")[0]
        df_S_P500 = pd.read_html(str(data))[0]
        df_S_P500 = df_S_P500[['Símbolo', 'Seguridad', 'Sector GICS', 'Ubicación de la sede', 'Fundada']].rename(columns={
            "Seguridad": "Company",
            "Símbolo": "Symbol",
            "Sector GICS": "Sector",
            "Ubicación de la sede": "Headquarters",
            "Fundada": "Fecha_fundada"
        })
        df_S_P500.to_csv(os.path.join(data_dir, 'lista_S_P500.csv'), index=None, header=True)
        logging.info("Datos de S&P 500 extraídos y guardados en lista_S_P500.csv")
        return df_S_P500
    except Exception as e:
        logging.error(f"Error al procesar y guardar datos de S&P 500: {e}")

""" La función extract_data selecciona una variable llamada ticket (que será el retorno de la función extraccion_datos_url) y una variable llamada period,
que será el periodo de interés. Esta función hará un bucle con las filas de ticket llamadas "Simbolo" para descargar la información de cada fila, que 
representa una empresa del S&P 500, mediante el método download de la librería yfinance, utilizando las variables ticket y period. Luego, unirá la información 
por medio del método append y agregará una columna llamada "Empresa" con el símbolo de la empresa, en un archivo llamado data. """

def extract_data(ticker, period):
    try:
        logging.info(f'Extrayendo datos para {ticker} del último trimestre {period}')
        dat = []
        for i in ticker['Symbol']:
            da = yf.download(i, period=period)
            da['Symbol'] = i
            dat.append(da)
        data = pd.concat(dat)
        logging.info(f'Datos extraídos exitosamente para {ticker}')
        return data
    except Exception as e:
        logging.error(f'Error extrayendo datos para {ticker}: {e}')
        return None

""" La función transform_data utiliza la data anterior, quita el índice de data y lo convierte en una columna y elimina las filas con datos faltantes. """
def transform_data(data):
    try:
        logging.info('Transformando datos')
        df = data[['Close', "Symbol"]].reset_index()
        df = df[['Date', 'Symbol', 'Close']]
        df.dropna(inplace=True)
        logging.info('Datos transformados exitosamente')
        return df
    except Exception as e:
        logging.error(f'Error transformando datos: {e}')
        return None


""" La función load_data guarda la data anterior en el directorio data_dir como un archivo CSV llamado 'precios_S_P500.csv'."""

def load_data(df):
    try:
        filename = os.path.join(data_dir, 'precios_S_P500.csv')
        logging.info(f'Guardando datos transformados en {filename}')
        df.to_csv(filename, index=False)
        logging.info('Datos guardados exitosamente')
    except Exception as e:
        logging.error(f'Error guardando datos: {e}')

""" La función etl_process compacta las funciones extract_data, transform_data y load_data en una sola función.   """
def etl_process(ticker, period):
    data = extract_data(ticker, period)
    if data is not None:
        transformed_data = transform_data(data)
        if transformed_data is not None:
            load_data(transformed_data)
            return transformed_data
    return None

""" Estos son lo parametros para la funcion etl_proccess"""
tickers = extraccion_datos_url("https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500")
period = "3mo"
etl_process(tickers, period)