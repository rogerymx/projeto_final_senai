import sqlite3
import pandas as pd
import streamlit as st
bannerFooter_html = """
<div style="
    position: relative;
    height: 200px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
">
    <!-- Imagem de fundo -->
    <div style="
        background-image: url('https://s1.1zoom.me/big0/475/Passenger_Airplanes_501163.jpg');
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 100%;
        filter: brightness(0.5);
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
    "></div>

    <!-- Texto centralizado -->
    <div style="
        position: relative;
        z-index: 2;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <h1 style="
            color: white;
            font-size: 36px;
            font-family: Arial, sans-serif;
            text-shadow: 2px 2px 4px black;
        ">
            Bem-vindo ao Sistema da Academia
        </h1>
    </div>
</div>
"""

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
    st.markdown("""
    <h1 style="
        text-align:center;
        font-size:36px;
        color:white;
        text-shadow: 2px 2px 4px black;
    ">
            Aviões 
    </h1>
""", unsafe_allow_html=True)
    st.markdown("""
    <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
""", unsafe_allow_html=True)
    st.markdown(bannerFooter_html, unsafe_allow_html=True)

    st.markdown("""
    <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
""", unsafe_allow_html=True)
    st.sidebar.divider()
    st.sidebar.markdown("""
        <h1 style="
            text-align:center;
            font-size:28px;
        ">
            Filtros
        </h1>
    """, unsafe_allow_html=True)
    df_avioes = pd.read_sql_query('''Select * from airplane''',conn)
    # st.dataframe(df_avioes)

    empresa_selec = st.sidebar.multiselect(
    "Nome da Empresa",
    options=sorted(df_avioes['EMPRESA_NOME'].unique()),
    default=None
    )

    natureza_selec = st.sidebar.multiselect(
    "Natureza do Voo",
    options=sorted(df_avioes['NATUREZA'].unique()),
    default=None
    )

    # ano_selec = st.sidebar.multiselect(
    # "Ano do Carro",
    # options=sorted(df_avioes['ANO'].unique()),
    # default=None
    # )

    if empresa_selec:
        df_avioes = df_avioes[df_avioes['EMPRESA_NOME'].isin(empresa_selec)]

    if natureza_selec:
        df_avioes = df_avioes[df_avioes['NATUREZA'].isin(natureza_selec)]

    # if ano_selec:
    #     df_avioes = df_avioes[df_avioes['ano_modelo'].isin(ano_selec)]
    
    tab_geral, tab_paises, tab_motorizacao, tab_database = st.tabs([
            "Visão geral", "Países", "Motorização","Database"
        ])
    
    with tab_geral:
        st.markdown("""
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Resumo Executivo
            </h1>
        """, unsafe_allow_html=True)
        st.divider()
        
        # CSS personalizado para centralizar as métricas
        st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.1);
            padding: 5% 5% 5% 10%;
            border-radius: 5px;
            overflow-wrap: break-word;
        }
        div[data-testid="stMetric"] > div {
            justify-content: center;
        }
        div[data-testid="stMetric"] > div[data-testid="stMetricLabel"] {
            justify-content: center;
        }
        div[data-testid="stMetric"] > div[data-testid="stMetricValue"] {
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Layout das colunas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Voos", f"{int(df_avioes['DECOLAGENS'].sum()):,}")
            st.metric("Total de Combustível Consumido", f"{int(df_avioes['COMBUSTÍVEL_LITROS'].sum()):,} L")

        with col2:
            total_domesticos = df_avioes[df_avioes['NATUREZA'] == 'DOMÉSTICA']
            st.metric("Voos Domésticos", f"{int(total_domesticos['DECOLAGENS'].sum()):,}")
            
            total_passageiros = int(df_avioes['PASSAGEIROS_PAGOS'].sum()) + int(df_avioes['PASSAGEIROS_GRÁTIS'].sum())
            st.metric("Total de Passageiros", f"{total_passageiros:,}")

        with col3:
            total_internacionais = df_avioes[df_avioes['NATUREZA'] == 'INTERNACIONAL']
            st.metric("Voos Internacionais", f"{int(total_internacionais['DECOLAGENS'].sum()):,}")
            
            total_carga = int(df_avioes['CARGA_PAGA_KG'].sum()) + int(df_avioes['CARGA_GRÁTIS_KG'].sum()) + int(df_avioes['CORREIO_KG'].sum())
            st.metric("Total de Carga", f"{total_carga:,} KG")
    with tab_database:
        st.markdown("""
            <h1 style="
                text-align:center;
                font-size:36px;
                color:white;
                text-shadow: 2px 2px 4px black;
            ">
                Database
            </h1>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.dataframe(df_avioes)        
