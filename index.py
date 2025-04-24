import streamlit as st
import time 
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Upa o arquivo CSV
#uploaded_file = st.file_uploader("Escolha o arquivo CSV", type=["csv", "xls"])
#if uploaded_file is not None:
#    # Para CSV
#    if uploaded_file.name.endswith(".csv"):
#        df = pd.read_csv(uploaded_file, sep=';', names=["DataHora", "Valor"])
#    # Para Excel
#    elif uploaded_file.name.endswith(".xls") or uploaded_file.name.endswith(".xlsx"):
#        df = pd.read_excel(uploaded_file, names=["DataHora", "Valor"])
#    
#    st.write("Prévia dos dados:")
#    st.dataframe(df)

# Caminho do CSV
df = pd.read_csv('./data/DATA.CSV.cvs', sep=';', names=["DataHora", "Valores"])

# Separando colunas
df[['Temperatura', 'Umidade', 'Pressao']] = df['Valores'].str.split(",", expand=True).astype(float)
df.drop(columns="Valores", inplace=True)

# Convertendo data
df["DataHora"] = pd.to_datetime(df["DataHora"], format="%d/%m/%Y %H:%M")
df.set_index("DataHora", inplace=True)

# Pegando datas inicial e final para o título
data_inicial = df.index.min().strftime("%d %b %Y")
data_final = df.index.max().strftime("%d %b %Y")

# ----------- GRÁFICO 1: TEMPERATURA -----------
fig_temp = go.Figure()

fig_temp.add_trace(go.Scatter(
    x=df.index,
    y=df['Temperatura'],
    mode='lines',
    name='Temperatura (°C)',
    line=dict(color='red')
))

fig_temp.update_layout(
    title=f"Temperatura (°C) — {data_inicial} até {data_final}",
    xaxis=dict(
        title='Data',
       # rangeslider=dict(visible=True),
        type='date',
        showgrid=True
    ),
    yaxis=dict(title='Temperatura (°C)', showgrid=True),
    template='plotly_white',
    height=400
)

# ----------- GRÁFICO 2: UMIDADE -----------
fig_umid = go.Figure()

fig_umid.add_trace(go.Scatter(
    x=df.index,
    y=df['Umidade'],
    mode='lines',
    name='Umidade Relativa (%)',
    line=dict(color='blue')
))

fig_umid.update_layout(
    title=f"Umidade Relativa (%) — {data_inicial} até {data_final}",
    xaxis=dict(
        title='Data',
       # rangeslider=dict(visible=True),
        type='date',
        showgrid=True
    ),
    yaxis=dict(title='Umidade (%)', showgrid=True),
    template='plotly_white',
    height=400
)

# ----------- GRÁFICO 3: PRESS -----------
fig_press = go.Figure()

fig_press.add_trace(go.Scatter(
    x=df.index,
    y=df['Pressao'],
    mode='lines',
    name='Pressao (hPa)',
    line=dict(color='green')
))

fig_press.update_layout(
    title=f"Pressao (hPa) — {data_inicial} até {data_final}",
    xaxis=dict(
        title='Data',
       # rangeslider=dict(visible=True),
        type='date',
        showgrid=True
    ),
    yaxis=dict(title='Pressao (hPa)', showgrid=True),
    template='plotly_white',
    height=400
)


# Mostrar os dois
#fig_temp.show()
#fig_umid.show()
#fig_press.show()

def main():
    st.title("Meteorologic Station Web")

    st.header("Grafico de Temperatura")
    st.plotly_chart(fig_temp, use_container_width=True)
    st.header("Grafico de Umidade")
    st.plotly_chart(fig_umid, use_container_width=True)
    st.header("Grafico de Pressao")
    st.plotly_chart(fig_press, use_container_width=True)

main()