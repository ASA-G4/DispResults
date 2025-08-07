import streamlit as st
import pandas as pd
import io
import requests
from datetime import datetime, timedelta

dateFormats = ['%Y-%m-%d %H:%M:%S.%f',
              '%Y-%m-%d %H:%M:%S',
              '%Y-%m-%d %H:%M',
              '%Y-%m-%d %H',
              '%Y-%m-%d']

def GetDateFromString(value: str) -> datetime:
   '''
   Convert the string date to a datetime tuple
   allowed formats 
   ('%Y-%m-%d %H:%M:%S.%f',
   '%Y-%m-%d %H:%M:%S',
   '%Y-%m-%d %H:%M',
   '%Y-%m-%d %H',
   '%Y-%m-%d')
   ``value: `` date string E.G. '10/20/2022 12:30:00'
   '''
   return datetime.strptime(value, GetDateFormat(value))


def GetStringFromDate(value: datetime, format: str) -> str:
   '''
   ``Convert`` the ``datetime`` tuple ``to`` a ``string`` date 
   allowed formats.
   ('%Y-%m-%d %H:%M:%S.%f',
   '%Y-%m-%d %H:%M:%S',
   '%Y-%m-%d %H:%M',
   '%Y-%m-%d %H',
   '%Y-%m-%d')
   ``value: `` datetime tupple.
   ``format: `` output format you need.
   '''
   return value.strftime(format)
def GetStringFromDateHM(value: datetime) -> str:
   '''
   ``Convert`` the ``datetime`` tuple ``to`` a ``string`` date 
   allowed formats.
   ('%Y-%m-%d %H:%M:%S.%f',
   '%Y-%m-%d %H:%M:%S',
   '%Y-%m-%d %H:%M',
   '%Y-%m-%d %H',
   '%Y-%m-%d')
   ``value: `` datetime tupple.
   ``format: `` output format you need.
   '''
   return value.strftime(dateFormats[2])

def GetDateFormat(value: str) -> str:
   '''
   From a given date or datetime string retrieve the dateformat.
   ``This is usefull to convert dates in string to datetime tuples.``
   ``value:`` date or datetime in string format 
   '''
   for dateFormat in dateFormats:
      try:
         datetime.strptime(value, dateFormat)
         return dateFormat
      except ValueError:
         continue
   return False

@st.cache_data(ttl=3600)
def descargar_datos():
    file_id = "1DEIZnjwUrQ2_EkjlB8jvsSPlfZ3y1elc"
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url)
    response.raise_for_status()  # lanza error si falla la descarga

    # Leer el contenido como archivo CSV
    return pd.read_csv(io.StringIO(response.text))  
# Cargar CSV
df = descargar_datos()
df1=df
df1["Time"]=df1["Time"].apply(GetDateFromString)
df1["Time"]=df1["Time"].apply(GetStringFromDateHM)
# Mostrar los datos
st.title("Real-time display of vehicle counts.")
st.write("Complete data:", df1)
df["Time"]=pd.to_datetime(df["Time"])
# Selección de rango de fechas
min_date = df["Time"].min()
max_date = df["Time"].max()+pd.Timedelta(days=1)

fecha_inicio = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
fecha_fin = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)

# Filtrado
df_filtrado = df[(df["Time"] >= pd.to_datetime(fecha_inicio)) & (df["Time"] <= pd.to_datetime(fecha_fin))]
df_filtrado["Time"]=df_filtrado["Time"].apply(GetStringFromDateHM)
# Mostrar resultados
st.write("Filtered data:", df_filtrado)
st.line_chart(df_filtrado)