import sqlite3
import pandas as pd
import streamlit as st
import database
import plotly.express as px
import plotly.graph_objects as go

banner_html = """
    <div style="
        position: relative;
        height: 200px;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
    ">
        <!-- Imagem de fundo -->
        <div style="
            background-image: url('https://png.pngtree.com/back_origin_pic/00/02/73/012889c34d373a30eb52240c1d2992e6.jpg');
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
            </h1>
        </div>
    </div>
    """
def auto (conn,cursor):
    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:36px;
            color:white;
            text-shadow: 2px 2px 4px black;
        ">
             Carros 
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
""", unsafe_allow_html=True)
    st.markdown(banner_html, unsafe_allow_html=True)
    st.markdown("""
    <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
""", unsafe_allow_html=True)

    df_automoveis = pd.read_sql_query('''Select * from automoveis''',conn)
    
    st.sidebar.divider()
    st.sidebar.markdown("""
        <h1 style="
            text-align:center;
            font-size:28px;
        ">
            Filtros
        </h1>
    """, unsafe_allow_html=True)

    montadora_selec = st.sidebar.multiselect(
    "Montadora",
    options=sorted(df_automoveis['montadora'].unique()),
    default=None
    )

    ano_selec = st.sidebar.multiselect(
    "Ano do Carro",
    options=sorted(df_automoveis['ano_modelo'].unique()),
    default=None
    )

    origem_selec = st.sidebar.multiselect(
    "Pais de Origem",
    options=sorted(df_automoveis['origem'].unique()),
    default=None
    )

    modelo_selec = st.sidebar.multiselect(
    "Modelo Carros",
    options=sorted(df_automoveis['nome'].unique()),
    default=None
    )

    if modelo_selec:
        df_automoveis = df_automoveis[df_automoveis['nome'].isin(modelo_selec)]

    if montadora_selec:
        df_automoveis = df_automoveis[df_automoveis['montadora'].isin(montadora_selec)]

    if ano_selec:
        df_automoveis = df_automoveis[df_automoveis['ano_modelo'].isin(ano_selec)]
        
    if origem_selec:
        df_automoveis = df_automoveis[df_automoveis['origem'].isin(origem_selec)]
    
    
        
    tab_geral, tab_paises, tab_motorizacao, tab_database = st.tabs([
            "Visão geral", "Países", "Motorização","Database"
        ])

    dashboard = pd.read_sql_query('SELECT * FROM automoveis', conn)

    with tab_geral:
        st.markdown("""
            <h1 style="
                text-align:center;
                font-size:36px;
                color:white;
                text-shadow: 2px 2px 4px black;
            ">
                Resumo Executivo
            </h1>
        """, unsafe_allow_html=True)

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
        st.divider()
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Carros", len(df_automoveis))
            st.metric("Média do Ano", round(df_automoveis['ano_modelo'].mean(), 0))
        
        with col2:
            st.metric("Consumo Médio (MPG)", round(df_automoveis['gpm'].mean(), 2))
            st.metric("Carro Mais Econômico", (df_automoveis.loc[df_automoveis['gpm'].idxmax(), 'nome']).upper())

        with col3:
            st.metric("Potência Média (HP)", round(df_automoveis['cavalos'].mean(), 2))
            st.metric("Carro Mais Potente", (df_automoveis.loc[df_automoveis['cavalos'].idxmax(), 'nome']).upper())


    with tab_motorizacao: 
        st.markdown("""
        <h1 style="
            text-align:center;
            font-size:36px;
            color:white;
            text-shadow: 2px 2px 4px black;
        ">
            Motorização
        </h1>
    """, unsafe_allow_html=True)
    st.divider()
    
    cursor.execute("DROP VIEW IF EXISTS eficiencia;")
    cursor.execute('''CREATE VIEW IF NOT EXISTS eficiencia AS
                            SELECT nome, gpm, cilindrada, cavalos, peso, aceleracao
                            FROM automoveis
                            ORDER BY gpm DESC;''')
    df_eficiencia = pd.read_sql_query('SELECT * FROM eficiencia', conn)

    numeric_cols = df_eficiencia.select_dtypes(include=['number']).columns
        
    df_eficienciaR = df_eficiencia.copy()
    df_eficienciaR[numeric_cols] = df_eficienciaR[numeric_cols].applymap(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
        )
        
    html_table = df_eficienciaR.style.set_table_styles([
            {'selector': 'table', 'props': [('width', '100%'), ('table-layout', 'fixed')]},
            {'selector': 'th', 'props': [('text-align', 'center')]},
            {'selector': 'td', 'props': [('text-align', 'center')]},
            {'selector': 'th:nth-child(1), td:nth-child(1)', 'props': [('width', '10%')]},
            {'selector': 'th:nth-child(2), td:nth-child(2)', 'props': [('width', '30%')]},
            {'selector': 'th:nth-child(3), td:nth-child(3)', 'props': [('width', '30%')]},
            {'selector': 'th:nth-child(4), td:nth-child(4)', 'props': [('width', '30%')]},
            ]).to_html(index=False)
            
    st.markdown(
        f"""
        <div style="overflow:auto; border:1px solid #ddd; padding:10px; border-radius:10px; max-height:400px">
            {html_table}
        </div>
        """,
        unsafe_allow_html=True
    )    
    
    nomes_selecionados = st.multiselect(
        "Selecione os nomes para comparar no gráfico radar:",
        df_automoveis['nome'].tolist(),
        default=df_automoveis['nome'].tolist()[:2]  
    )
    
    if nomes_selecionados:
        categorias = ['cilindrada', 'cavalos', 'peso', 'aceleracao']
        
        df_normalizado = df_automoveis.copy()
        for categoria in categorias:
            if categoria == 'aceleracao':
                df_normalizado[categoria] = 1 - (
                    (df_automoveis[categoria] - df_automoveis[categoria].min()) / 
                    (df_automoveis[categoria].max() - df_automoveis[categoria].min())
                )
            else:
                df_normalizado[categoria] = (
                    (df_automoveis[categoria] - df_automoveis[categoria].min()) / 
                    (df_automoveis[categoria].max() - df_automoveis[categoria].min())
                )
        
        fig = go.Figure()
        
        for nome in nomes_selecionados:
            dados = df_normalizado[df_normalizado['nome'] == nome].iloc[0]
            valores = [dados[c] for c in categorias]
            
            fig.add_trace(go.Scatterpolar(
                r=valores + [valores[0]],  
                theta=categorias + [categorias[0]],
                fill='toself',
                name=nome
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]  
                )
            ),
            showlegend=True,
            title="Comparação dos modelos por características"
        )
        
        st.plotly_chart(fig)

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
        
        # Identifica todas as colunas numéricas
        numeric_cols = df_automoveis.select_dtypes(include=['number']).columns
        
        # Cria uma cópia e formata os valores para 2 casas decimais
        df_automoveisR = df_automoveis.copy()
        df_automoveisR[numeric_cols] = df_automoveisR[numeric_cols].applymap(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
        )
        
        # Gera a tabela HTML com estilos
        html_table = df_automoveisR.style.set_table_styles([
            {'selector': 'table', 'props': [('width', '100%'), ('table-layout', 'fixed')]},
            {'selector': 'th', 'props': [('text-align', 'center')]},
            {'selector': 'td', 'props': [('text-align', 'center')]},
            {'selector': 'th:nth-child(1), td:nth-child(1)', 'props': [('width', '10%')]},
            {'selector': 'th:nth-child(2), td:nth-child(2)', 'props': [('width', '30%')]},
            {'selector': 'th:nth-child(3), td:nth-child(3)', 'props': [('width', '30%')]},
            {'selector': 'th:nth-child(4), td:nth-child(4)', 'props': [('width', '30%')]},
        ]).to_html(index=False)
        
        st.markdown(
            f"""
            <div style="overflow:auto; border:1px solid #ddd; padding:10px; border-radius:10px; max-height:400px">
                {html_table}
            """,
            unsafe_allow_html=True
        )

    with tab_paises:
            mapa_de_cores = {
                'usa': '#0ce3e8',
                'japan': "#9B59B6",
                'europe': '#5DADE2'
            }

            st.markdown("""
                <h1 style="
                    text-align:center;
                    font-size:36px;
                    color:white;
                    text-shadow: 2px 2px 4px black;
                ">
                    Resumo Países
                </h1>
            """, unsafe_allow_html=True)
            st.divider()

            pais_de_origem = dashboard['origem'].value_counts()
            f1 = px.pie(pais_de_origem, values=pais_de_origem.values, names=pais_de_origem.index, title="Distribuição de Carros por Origem")

            consumo_medio = df_automoveis.groupby('origem')['gpm'].mean().reset_index()
            f2 = px.bar(consumo_medio, x='origem', y='gpm', title='Eficiência Média (MPG) por Origem', color='origem', color_discrete_map=mapa_de_cores)

            col4, col5 = st.columns(2)
            with col4:
                st.plotly_chart(f1, use_container_width=True)
            with col5:
                st.plotly_chart(f2, use_container_width=True)
