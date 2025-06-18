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

    natureza_selec = st.sidebar.multiselect(
    "Natureza do Voo",
    options=sorted(df_avioes['NATUREZA'].unique()),
    default=None
    )

    if natureza_selec:
        df_avioes = df_avioes[df_avioes['NATUREZA'].isin(natureza_selec)]


    empresa_selec = st.sidebar.multiselect(
    "Nome da Empresa",
    options=sorted(df_avioes['EMPRESA_NOME'].unique()),
    default=None
    )

    if empresa_selec:
        df_avioes = df_avioes[df_avioes['EMPRESA_NOME'].isin(empresa_selec)]



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


    grupo_voo_select = st.sidebar.multiselect(
    "Grupo de Voo",
    options=sorted(df_avioes['GRUPO_DE_VOO'].unique()),
    default=None
    )

    if grupo_voo_select:
        df_avioes = df_avioes[df_avioes['GRUPO_DE_VOO'].isin(grupo_voo_select)]


    def formatar_numero(valor):
        if valor >= 1_000_000_000:
            return f'{valor / 1_000_000_000:.1f}bi'
        elif valor >= 1_000_000:
            return f'{valor / 1_000_000:.1f}mi'
        elif valor >= 1_000:
            return f'{valor / 1_000:.1f}k'
        else:
            return f'{int(valor)}'

    tab_geral, tab_desempenho, tab_combustivel, tab_regiao, tab_database = st.tabs([
            "Visão geral", "Desempenho", "Combustivel", "Região","Database"
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

        
        total_voos = df_avioes['DECOLAGENS'].sum()
        total_combustivel = df_avioes['COMBUSTÍVEL_LITROS'].sum()
        total_passageiros = df_avioes['PASSAGEIROS_PAGOS'].sum() + df_avioes['PASSAGEIROS_GRÁTIS'].sum()
        total_carga_kg = df_avioes['CARGA_PAGA_KG'].sum() + df_avioes['CARGA_GRÁTIS_KG'].sum() + df_avioes['CORREIO_KG'].sum()
        
        voos_domesticos = df_avioes[df_avioes['NATUREZA'] == 'DOMÉSTICA']['DECOLAGENS'].sum()
        voos_internacionais = df_avioes[df_avioes['NATUREZA'] == 'INTERNACIONAL']['DECOLAGENS'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Voos", formatar_numero(total_voos))
            st.metric("Total de Combustível (L)", formatar_numero(total_combustivel))

        with col2:
            st.metric("Voos Domésticos", formatar_numero(voos_domesticos))
            st.metric("Total de Passageiros", formatar_numero(total_passageiros))

        with col3:
            st.metric("Voos Internacionais", formatar_numero(voos_internacionais))
            st.metric("Total de Carga (KG)", formatar_numero(total_carga_kg))
        
        decolPer =((df_avioes.groupby('EMPRESA_SIGLA')['DECOLAGENS'].sum()).sort_values(ascending=False).head(20))

        fig_ano = px.bar(
        x=decolPer.index,
        y=decolPer.values,
        title='Total de Decolagens por Ano (Top 20)',
        labels={'x': 'Ano', 'y': 'Total de Decolagens'},
        text_auto=True  
                )

        fig_ano.update_traces(marker_color='#0ce3e8')


        st.plotly_chart(fig_ano, use_container_width=True)


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
                title='Taxa de Ocupação Média de Passageiros por Empresa (Top 5)', 
                barmode='group',
                color_discrete_sequence=paleta_monocromatica) 

            fig.update_traces(
                text=df_agrupado['OCUPACAO'].apply(lambda x: f'{x:.1f}%'), 
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(
                    size=16,
                    color='white', 
                    family='Arial, sans-serif'
                )
            )

            st.plotly_chart(fig)
        with col2:

            df_carga = df_avioes.groupby('EMPRESA_SIGLA').agg({
                'ATK': 'mean',
                'RTK': 'mean'
            }).reset_index()

            df_carga['OCUPACAO'] = (df_carga['RTK'] / df_carga['ATK']) * 100 
            df_carga['OCUPACAO'] = df_carga['OCUPACAO'].round(2)

            df_carga = df_carga.sort_values('OCUPACAO', ascending=False).head(5)

            fig1 = px.bar(df_carga, x='EMPRESA_SIGLA', y=['OCUPACAO'], 
                title='Taxa de Ocupação Média de Carga por Empresa (Top 5)', 
                barmode='group',
                color_discrete_sequence=paleta_monocromatica) 

            fig1.update_traces(
                text=df_carga['OCUPACAO'].apply(lambda x: f'{x:.1f}%'),
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(
                    size=16,
                    color='white', 
                    family='Arial, sans-serif'
                )
            )
            st.plotly_chart(fig1)

        col1, col2 = st.columns(2)

        with col1:

            market_share_passageiros = df_avioes.groupby('EMPRESA_NOME')['PASSAGEIROS_PAGOS'].sum().reset_index()

            market_share_passageiros = market_share_passageiros.sort_values(by='PASSAGEIROS_PAGOS', ascending=False)

            if len(market_share_passageiros) > 20:
                top_20 = market_share_passageiros.head(20)
                
                outras = pd.DataFrame({
                    'EMPRESA_NOME': ['Outras'],
                    'PASSAGEIROS_PAGOS': [market_share_passageiros.iloc[20:]['PASSAGEIROS_PAGOS'].sum()]
                })
                
                df_para_grafico = pd.concat([top_20, outras], ignore_index=True)
            else:
                df_para_grafico = market_share_passageiros

            fig = px.treemap(
                df_para_grafico, 
                path=[px.Constant("Todas as Empresas"), 'EMPRESA_NOME'], 
                values='PASSAGEIROS_PAGOS',
                title='Market Share das 20 Maiores Empresas (+ Outras)'
            )

            fig.update_traces(textinfo="label+percent root")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            query_decolagens_mes = 'SELECT MÊS, SUM(DECOLAGENS) as DECOLAGENS FROM airplane GROUP BY MÊS'
            media_mes = pd.read_sql_query(query_decolagens_mes, conn)

            media_mes = media_mes.set_index('MÊS')

            indice_anual_completo = pd.Index(range(1, 13), name='MÊS')  
            media_mes = media_mes.reindex(indice_anual_completo, fill_value=0)

            media_mes = media_mes.reset_index()

            fig = px.pie(
                media_mes,
                names='MÊS',                 
                values='DECOLAGENS',        
                title='Distribuição de Decolagens por Mês',
                hole=0.3,                     
                color_discrete_sequence=px.colors.sequential.Teal  
            )

            fig.update_traces(
                textposition='inside',     
                textinfo='percent+label',    
                marker=dict(line=dict(color='white', width=1))  
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab_combustivel:
        st.markdown(""" 
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Combustivel
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
            height=500,
            hover_data=['ANO', 'MÊS']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
   
        df_carga2 = df_avioes.groupby('EMPRESA_NOME').agg({
            'CARGA_PAGA_KG': 'sum',
            'CARGA_GRÁTIS_KG': 'sum',
            'CORREIO_KG': 'sum',
            'COMBUSTÍVEL_LITROS': 'sum'
        }).reset_index()

        st.markdown("### 5 Menores Consumos de Combustível por KG de Carga por Empresa")

        df_carga2['CONSUMO_CARGA'] = df_carga2['COMBUSTÍVEL_LITROS'] / (
            df_carga2['CARGA_PAGA_KG'] + df_carga2['CARGA_GRÁTIS_KG'] + df_carga2['CORREIO_KG']
        )

        df_carga2['CONSUMO_CARGA'] = df_carga2['CONSUMO_CARGA'].replace([float('inf'), -float('inf')], 0)
        df_carga2 = df_carga2.fillna(0)

        df_carga2 = df_carga2[(df_carga2['COMBUSTÍVEL_LITROS'] > 0) & (df_carga2['CONSUMO_CARGA'] > 0)]

        df_top5 = df_carga2.sort_values('CONSUMO_CARGA').head(5)

        fig_consumo = px.bar(
            df_top5,
            x='EMPRESA_NOME',
            y='CONSUMO_CARGA',
            labels={'EMPRESA_NOME': 'Empresa', 'CONSUMO_CARGA': 'Consumo (L/kg)'},
            color='CONSUMO_CARGA',
            color_continuous_scale='Viridis'
        )

        fig_consumo.update_layout(
            xaxis_tickangle=-45,
            margin=dict(t=50, b=100)
        )

        st.plotly_chart(fig_consumo, use_container_width=True)


    with tab_regiao:
        st.markdown(""" 
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Região (Doméstico)
            </h1>
        """, unsafe_allow_html=True)
        
        st.divider()
        df_origem = pd.read_sql_query('SELECT * FROM airplane WHERE AEROPORTO_DE_ORIGEM_REGIÃO NOT NULL', conn)

        df_destino = pd.read_sql_query('SELECT * FROM airplane WHERE AEROPORTO_DE_DESTINO_REGIÃO NOT NULL', conn)
        col1, col2 = st.columns(2)

        with col1:

            df_voos_por_regiao_origem = df_origem.groupby('AEROPORTO_DE_ORIGEM_REGIÃO').size().reset_index(name='Quantidade_Voos')

            # Criar o gráfico de pizza
            fig = px.pie(df_voos_por_regiao_origem, 
                        names='AEROPORTO_DE_ORIGEM_REGIÃO', 
                        values='Quantidade_Voos',
                        title='Quantidade de Voos por Região de Origem')

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)

        with col2:
            df_voos_por_regiao_destino = df_destino.groupby('AEROPORTO_DE_DESTINO_REGIÃO').size().reset_index(name='Quantidade_Voos')

                    # Criar o gráfico de pizza
            fig = px.pie(df_voos_por_regiao_destino, 
                        names='AEROPORTO_DE_DESTINO_REGIÃO', 
                        values='Quantidade_Voos',
                        title='Quantidade de Voos por Região de Destino')

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)

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
