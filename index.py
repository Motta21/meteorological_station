import streamlit as st
import time 
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def carregar_dados():
    try:
        df = pd.read_csv('data/DATA.csv', sep=';', names=["DataHora", "Valores"])

        # Garantir que a coluna 'Valores' é string
        df['Valores'] = df['Valores'].str.replace('"', '', regex=True)

        # Separando colunas
        df[['Temperatura', 'Umidade', 'Pressao']] = df['Valores'].str.split(",", expand=True).astype(float)
        df.drop(columns="Valores", inplace=True)

        # Convertendo data
        df["DataHora"] = pd.to_datetime(df["DataHora"], format="%d/%m/%Y %H:%M")
        df.set_index("DataHora", inplace=True)

        return df
    except FileNotFoundError:
        st.error("Arquivo 'DATA.csv' não encontrado na pasta 'data/'.")
    except Exception as e:
        st.error(f"Erro ao carregar ou processar os dados: {e}")
    return None

    

def main():
    st.title("Dados da Estação Meteorológica de Baixo Custo")

    df = carregar_dados()
    if df is None:
        st.stop()  # Para a execução do Streamlit com segurança
  # Interrompe a execução se der erro nos dados
 


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
        xaxis=dict(title='Data', rangeslider=dict(visible=True), type='date', showgrid=True),
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
        xaxis=dict(title='Data', rangeslider=dict(visible=True), type='date', showgrid=True),
        yaxis=dict(title='Umidade (%)', showgrid=True),
        template='plotly_white',
        height=400
    )

    # ----------- GRÁFICO 3: PRESSÃO -----------
    fig_press = go.Figure()
    fig_press.add_trace(go.Scatter(
        x=df.index,
        y=df['Pressao'],
        mode='lines',
        name='Pressão (hPa)',
        line=dict(color='green')
    ))
    fig_press.update_layout(
        title=f"Pressão (hPa) — {data_inicial} até {data_final}",
        xaxis=dict(title='Data', rangeslider=dict(visible=True), type='date', showgrid=True),
        yaxis=dict(title='Pressão (hPa)', showgrid=True),
        template='plotly_white',
        height=400
    )

    # Exibição dos gráficos
    st.header("Gráfico de Temperatura")
    st.plotly_chart(fig_temp, use_container_width=True)

    st.header("Gráfico de Umidade")
    st.plotly_chart(fig_umid, use_container_width=True)

    st.header("Gráfico de Pressão")
    st.plotly_chart(fig_press, use_container_width=True)

main()
