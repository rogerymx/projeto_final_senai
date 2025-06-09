import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('database/airplane.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS airplane (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMPRESA_SIGLA TEXT,
    EMPRESA_NOME TEXT,
    EMPRESA_NACIONALIDADE TEXT,
    ANO INTEGER,
    MÊS INTEGER,
    AEROPORTO_DE_ORIGEM_SIGLA TEXT,
    AEROPORTO_DE_ORIGEM_NOME TEXT,
    AEROPORTO_DE_ORIGEM_UF TEXT,
    AEROPORTO_DE_ORIGEM_REGIÃO TEXT,
    AEROPORTO_DE_ORIGEM_PAÍS TEXT,
    AEROPORTO_DE_ORIGEM_CONTINENTE TEXT,
    AEROPORTO_DE_DESTINO_SIGLA TEXT,
    AEROPORTO_DE_DESTINO_NOME TEXT,
    AEROPORTO_DE_DESTINO_UF TEXT,
    AEROPORTO_DE_DESTINO_REGIÃO TEXT,
    AEROPORTO_DE_DESTINO_PAÍS TEXT,
    AEROPORTO_DE_DESTINO_CONTINENTE TEXT,
    NATUREZA TEXT,
    GRUPO_DE_VOO TEXT,
    PASSAGEIROS_PAGOS INTEGER,
    PASSAGEIROS_GRÁTIS INTEGER,
    CARGA_PAGA_KG REAL,
    CARGA_GRÁTIS_KG REAL,
    CORREIO_KG REAL,
    ASK REAL,
    RPK REAL,
    ATK REAL,
    RTK REAL,
    COMBUSTÍVEL_LITROS REAL,
    DISTÂNCIA_VOADA_KM REAL,
    DECOLAGENS INTEGER,
    CARGA_PAGA_KM REAL,
    CARGA_GRATIS_KM REAL,
    CORREIO_KM REAL,
    ASSENTOS INTEGER,
    PAYLOAD REAL,
    HORAS_VOADAS REAL,
    BAGAGEM_KG REAL
);
''')

conn.commit()

cursor.execute("SELECT COUNT(*) FROM airplane")
if cursor.fetchone()[0] == 0:
    df_airplanes = pd.read_csv('database/airplanes.csv')
    df_airplanes.to_sql('airplane', conn, if_exists='append', index=False)



def air ():
    st.write('Avião')
    st.sidebar.divider()
    st.sidebar.markdown("""
        <h1 style="
            text-align:center;
            font-size:28px;
            color:white;
            text-shadow: 2px 2px 4px black;
        ">
            Filtros
        </h1>
    """, unsafe_allow_html=True)
    st.sidebar.selectbox("Selecione: ", ['Carro', 'Avião'], key="carro_select")

    teste = pd.read_sql_query('''
        Select * from airplane
    ''',conn)
    st.dataframe(teste)
    