import streamlit as st
import pandas as pd
import io
import requests
import matplotlib.pyplot as plt
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
df_filtrado["Real-time vehicle counting 2"]=df_filtrado["Real-time vehicle counting"]*2.0



st.title("Dinamic columns visualization")

# Opción para seleccionar qué columnas mostrar (además de 'a')
columnas_opcionales = ["Real-time vehicle counting", "Real-time vehicle counting 2"]
seleccionadas = st.multiselect(
    "Select additional columns to show ( 'Time' column is always showed):",
    opciones := columnas_opcionales,
    default=["Real-time vehicle counting"]
)

# Mostrar DataFrame con la columna 'a' + las seleccionadas
columnas_a_mostrar = ['Time'] + seleccionadas
st.dataframe(df_filtrado[columnas_a_mostrar])
# Mostrar resultados
df_filtrado["Time"]=df_filtrado["Time"].apply(GetDateFromString)
opciones_y = st.multiselect(
    "Select column(s) to show on the Y axis",
    options=["Real-time vehicle counting", "Real-time vehicle counting 2"],
    default=["Real-time vehicle counting"]
)

# Validar si se seleccionó al menos una
if opciones_y:
    fig, ax = plt.subplots()
    for col in opciones_y:
        ax.plot(df_filtrado['Time'], df_filtrado[col], label=col)
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Count")
    ax.set_title("Plot of selected columns")
    ax.legend()
    ax.tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)
else:
    st.warning("Choose at least one column to show.")