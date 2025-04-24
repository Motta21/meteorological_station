import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Verifica se o arquivo existe
csv_path = './data/DATA.csv'
if not os.path.exists(csv_path):
    st.error("O arquivo CSV não foi encontrado no diretório especificado.")
else:
    # Carrega o CSV
    df = pd.read_csv(csv_path, sep=';', names=["DataHora", "Valores"])

    # Verifica se há valores na coluna 'Valores'
    if df['Valores'].isnull().any():
        st.warning("Há valores nulos na coluna 'Valores'. Certifique-se de que os dados estejam corretos.")
    
    # Garante que todos os valores são strings antes de separar
    df['Valores'] = df['Valores'].astype(str)
    df[['Temperatura', 'Umidade', 'Pressao']] = df['Valores'].str.split(",", expand=True).astype(float)
    df.drop(columns="Valores", inplace=True)

    # Convertendo datas
    df["DataHora"] = pd.to_datetime(df["DataHora"], format="%d/%m/%Y %H:%M")
    df.set_index("DataHora", inplace=True)

    # Pegando datas inicial e final para o título
    data_inicial = df.index.min().strftime("%d %b %Y")
    data_final = df.index.max().strftime("%d %b %Y")

    # Filtra dados por período selecionado
    data_selecionada = st.date_input("Selecione o período", [df.index.min(), df.index.max()])
    df_filtrado = df.loc[data_selecionada[0]:data_selecionada[1]]

    # ----------- GRÁFICO 1: TEMPERATURA -----------
    fig_temp = go.Figure()

    fig_temp.add_trace(go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['Temperatura'],
        mode='lines',
        name='Temperatura (°C)',
        line=dict(color='red')
    ))

    fig_temp.update_layout(
        title=f"Temperatura (°C) — {data_inicial} até {data_final}",
        xaxis=dict(
            title='Data',
            rangeslider=dict(visible=True),
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
        x=df_filtrado.index,
        y=df_filtrado['Umidade'],
        mode='lines',
        name='Umidade Relativa (%)',
        line=dict(color='blue')
    ))

    fig_umid.update_layout(
        title=f"Umidade Relativa (%) — {data_inicial} até {data_final}",
        xaxis=dict(
            title='Data',
            rangeslider=dict(visible=True),
            type='date',
            showgrid=True
        ),
        yaxis=dict(title='Umidade (%)', showgrid=True),
        template='plotly_white',
        height=400
    )

    # ----------- GRÁFICO 3: PRESSÃO -----------
    fig_press = go.Figure()

    fig_press.add_trace(go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['Pressao'],
        mode='lines',
        name='Pressao (hPa)',
        line=dict(color='green')
    ))

    fig_press.update_layout(
        title=f"Pressao (hPa) — {data_inicial} até {data_final}",
        xaxis=dict(
            title='Data',
            rangeslider=dict(visible=True),
            type='date',
            showgrid=True
        ),
        yaxis=dict(title='Pressao (hPa)', showgrid=True),
        template='plotly_white',
        height=400
    )

    # ----------- STREAMLIT WEB APP -----------
    def main():
        st.title("Meteorologic Station Web")
        st.header("Gráfico de Temperatura")
        st.plotly_chart(fig_temp, use_container_width=True)
        st.header("Gráfico de Umidade")
        st.plotly_chart(fig_umid, use_container_width=True)
        st.header("Gráfico de Pressão")
        st.plotly_chart(fig_press, use_container_width=True)

    main()
