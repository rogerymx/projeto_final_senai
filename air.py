import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

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

cursor.execute("DROP VIEW IF EXISTS avioes_desempenho")
# cursor.execute('''CREATE VIEW IF NOT EXISTS avioes_desempenho AS
# SELECT  EMPRESA_NOME, ANO, MES, AEROPORTO_DE_ORIGEM_SIGLA, AEROPORTO_DE_ORIGEM_NOME, AEROPORTO_DE_ORIGEM_REGIÃO, AEROPORTO_DE_DESTINO_SIGLA, AEROPORTO_DE_DESTINO_NOME,
#         AEROPORTO_DE_DESTINO_REGIÃO, NATUREZA, PASSAGEIROS_PAGOS + PASSAGEIROS_GRÁTIS AS PASSAGEIROS, CARGA_PAGA_KG + CARGA_GRÁTIS_KG + CORREIO_KG AS CARGA, GRUPO_DE_VOO, 
#         ASK, RPK, ATK, RTK, COMBUSTÍVEL_LITROS, DECOLAGENS, HORAS_VOADAS
# FROM airplane;
# ''')


def air ():
    paleta_monocromatica = ["#10676D", "#1899A4", "#52B6BC", "#8CD3D5", "#C5E9EA"]

    st.markdown("""
    <h1 style="
        text-align:center;
        font-size:36px;
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
    if empresa_selec:
        df_avioes = df_avioes[df_avioes['EMPRESA_NOME'].isin(empresa_selec)]

    natureza_selec = st.sidebar.multiselect(
    "Natureza do Voo",
    options=sorted(df_avioes['NATUREZA'].unique()),
    default=None
    )

    if natureza_selec:
        df_avioes = df_avioes[df_avioes['NATUREZA'].isin(natureza_selec)]


    mes_selec = st.sidebar.multiselect(
    "Mês do Voo",
    options=sorted(df_avioes['MÊS'].unique()),
    default=None
    )

    if mes_selec:
        df_avioes = df_avioes[df_avioes['MÊS'].isin(mes_selec)]

    aeroporto_origem_select = st.sidebar.multiselect(
    "País de Origem do Voo",
    options=sorted(df_avioes['AEROPORTO_DE_ORIGEM_PAÍS'].unique()),
    default=None
    )

    if aeroporto_origem_select:
        df_avioes = df_avioes[df_avioes['AEROPORTO_DE_ORIGEM_PAÍS'].isin(aeroporto_origem_select)]


    # ano_selec = st.sidebar.multiselect(
    # "Ano do Carro",
    # options=sorted(df_avioes['ANO'].unique()),
    # default=None
    # )

    
    tab_geral, tab_desempenho, tab_motorizacao, tab_database = st.tabs([
            "Visão geral", "Desempenho", "Motorização","Database"
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
        
    with tab_desempenho:    
        st.markdown("""
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Desempenho
            </h1>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)

        with col1:
            df_agrupado = df_avioes.groupby('EMPRESA_SIGLA').agg({
                'RPK': 'mean',
                'ASK': 'mean'
            }).reset_index()

            df_agrupado['OCUPACAO'] = (df_agrupado['RPK'] / df_agrupado['ASK']) * 100 
            df_agrupado['OCUPACAO'] = df_agrupado['OCUPACAO'].round(2)

            df_agrupado = df_agrupado.sort_values('OCUPACAO', ascending=False).head(5)

            fig = px.bar(df_agrupado, x='EMPRESA_SIGLA', y=['OCUPACAO'], 
                title='Taxa de Ocupação Média por Empresa', 
                barmode='group',
                color_discrete_sequence=paleta_monocromatica) # <--- AQUI

            fig.update_traces(
                text=df_agrupado['OCUPACAO'].apply(lambda x: f'{x:.1f}%'), # Dica: formatar com 1 casa decimal
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(
                    size=16,
                    color='white', # Cor branca para melhor contraste com as barras escuras
                    family='Arial, sans-serif'
                )
            )

            st.plotly_chart(fig)
        with col2:
            query_decolagens_mes = 'SELECT MÊS, SUM(DECOLAGENS) as DECOLAGENS FROM airplane GROUP BY MÊS'
            media_mes = pd.read_sql_query(query_decolagens_mes, conn)

            # 2. Define 'MÊS' como o índice do DataFrame
            media_mes = media_mes.set_index('MÊS')

            # 3. Cria um índice completo de 1 a 12 e aplica ao DataFrame
            # Meses existentes mantêm seus dados, meses ausentes são criados com o valor 0.
            indice_anual_completo = pd.Index(range(1, 5), name='MÊS')
            media_mes = media_mes.reindex(indice_anual_completo, fill_value=0)

            # 4. Transforma o índice 'MÊS' de volta em uma coluna para usar no Plotly Express
            media_mes = media_mes.reset_index()

            # 5. Cria e exibe o gráfico de barras (seu código aqui já estava correto)
            fig = px.bar(
                media_mes, 
                x='MÊS', 
                y='DECOLAGENS', 
                title='Total de Decolagens por Mês',
                text_auto=True # Dica: Adiciona o valor no topo de cada barra
            )
            fig.update_traces(
                marker_color='#129990',          # Define a nova cor escura para as barras
                textfont_color='white'           # Garante que o texto dentro da barra seja branco para contraste
            )

            st.plotly_chart(fig, use_container_width=True)

            
        df_carga = df_avioes.groupby('EMPRESA_SIGLA').agg({
            'ATK': 'mean',
            'RTK': 'mean'
        }).reset_index()

        df_carga['OCUPACAO'] = (df_carga['RTK'] / df_carga['ATK']) * 100 
        df_carga['OCUPACAO'] = df_carga['OCUPACAO'].round(2)

        df_carga = df_carga.sort_values('OCUPACAO', ascending=False).head(5)

        fig1 = px.bar(df_carga, x='EMPRESA_SIGLA', y=['OCUPACAO'], 
            title='Taxa de Ocupação Média por Empresa', 
            barmode='group',
            color_discrete_sequence=paleta_monocromatica) # <--- AQUI

        fig1.update_traces(
            text=df_carga['OCUPACAO'].apply(lambda x: f'{x:.1f}%'), # Dica: formatar com 1 casa decimal
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(
                size=16,
                color='white', # Cor branca para melhor contraste com as barras escuras
                family='Arial, sans-serif'
            )
        )
        st.plotly_chart(fig1)
        
        df_carga2 = pd.read_sql_query('''SELECT EMPRESA_NOME, SUM(CARGA_PAGA_KG), SUM(CARGA_GRÁTIS_KG), SUM(CORREIO_KG), SUM(COMBUSTÍVEL_LITROS)  FROM airplane 
                                        GROUP BY EMPRESA_NOME''', conn)
        df_carga2 = df_carga2[df_carga2['SUM(COMBUSTÍVEL_LITROS)'] > 0]
        st.dataframe(df_carga2)

    with tab_motorizacao:
        st.markdown(""" 
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Motorização
            </h1>
        """, unsafe_allow_html=True)
        
        st.divider()

        st.markdown("### Consumo de Combustível por KM (por Empresa)")

        df_consumo_empresa = df_avioes[(df_avioes['COMBUSTÍVEL_LITROS'] > 0) & (df_avioes['DISTÂNCIA_VOADA_KM'] > 0)]
        df_consumo_empresa['COMBUSTIVEL_POR_KM'] = df_consumo_empresa['COMBUSTÍVEL_LITROS'] / df_consumo_empresa['DISTÂNCIA_VOADA_KM']

        df_consumo = df_consumo_empresa.groupby('EMPRESA_NOME')['COMBUSTIVEL_POR_KM'].mean().reset_index()

        fig = px.bar(
            df_consumo.sort_values('COMBUSTIVEL_POR_KM', ascending=True),
            x='COMBUSTIVEL_POR_KM',
            y='EMPRESA_NOME',
            orientation='h',
            labels={'EMPRESA_NOME': 'Empresa', 'COMBUSTIVEL_POR_KM': 'Litros por KM'},
            height=500
        )
        fig.update_traces(marker_color='#147D85')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Relação entre Distância Voada e Combustível Consumido")

        fig_scatter = px.scatter(
            df_consumo_empresa,
            x='DISTÂNCIA_VOADA_KM',
            y='COMBUSTÍVEL_LITROS',
            color='EMPRESA_NOME',
            labels={
                'DISTÂNCIA_VOADA_KM': 'Distância Voada (KM)',
                'COMBUSTÍVEL_LITROS': 'Combustível Consumido (Litros)',
                'EMPRESA_NOME': 'Empresa'
            },
            title='Dispersão: Distância Voada x Combustível Consumido',
            height=500,
            hover_data=['ANO', 'MÊS']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab_database:
        st.markdown(""" 
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Database
            </h1>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.dataframe(df_avioes)        
