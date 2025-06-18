import sqlite3
import pandas as pd
import streamlit as st
import database
import plotly.express as px
import plotly.graph_objects as go
import base64
with open("carro.png", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

banner_html = f"""
<div style="
    position: relative;
    height: 200px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
">
    <div style="
        background-image: url('data:image/png;base64,{img_base64}');
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
            Bem-vindo à Plataforma de Desempenho
        </h1>
    </div>
</div>
"""

def auto (conn,cursor):
    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:36px;
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


    origem_selec = st.sidebar.multiselect(
    "Pais de Origem",
    options=sorted(df_automoveis['origem'].unique()),
    default=None
    )

    if origem_selec:
        df_automoveis = df_automoveis[df_automoveis['origem'].isin(origem_selec)]

    montadora_selec = st.sidebar.multiselect(
    "Montadora",
    options=sorted(df_automoveis['montadora'].unique()),
    default=None
    )

    if montadora_selec:
        df_automoveis = df_automoveis[df_automoveis['montadora'].isin(montadora_selec)]

    modelo_selec = st.sidebar.multiselect(
    "Modelo Carros",
    options=sorted(df_automoveis['nome'].unique()),
    default=None
    )

    if modelo_selec:
        df_automoveis = df_automoveis[df_automoveis['nome'].isin(modelo_selec)]

    ano_selec = st.sidebar.multiselect(
    "Ano do Carro",
    options=sorted(df_automoveis['ano_modelo'].unique()),
    default=None
    )

    if ano_selec:
        df_automoveis = df_automoveis[df_automoveis['ano_modelo'].isin(ano_selec)]
        

    
    
        
    tab_geral, tab_paises, tab_motorizacao, tab_database = st.tabs([
            "Visão geral", "Países", "Motorização","Database"
        ])

    dashboard = pd.read_sql_query('SELECT * FROM automoveis', conn)

    with tab_geral:
        st.markdown("""
            <h1 style="
                text-align:center;
                font-size:36px;
            ">
                Resumo Executivo
            </h1>
        """, unsafe_allow_html=True)

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
            st.metric("Média de cilindradas", round(df_automoveis['cilindrada'].mean()))
        
        with col2:
            st.metric("Consumo Médio (MPG)", round(df_automoveis['gpm'].mean(), 2))
            st.metric("Carro Mais Econômico", (df_automoveis.loc[df_automoveis['gpm'].idxmax(), 'nome']).upper())

        with col3:
            st.metric("Potência Média (HP)", round(df_automoveis['cavalos'].mean(), 2))
            st.metric("Carro Mais Potente", (df_automoveis.loc[df_automoveis['cavalos'].idxmax(), 'nome']).upper())
            
        carros_por_ano = df_automoveis['ano_modelo'].value_counts().sort_index()

        fig_ano = px.bar(
        x=carros_por_ano.index,
        y=carros_por_ano.values,
        title='Total de Carros por Ano',
        labels={'x': 'Ano', 'y': 'Total de Carros'},
        text_auto=True  
                )

        fig_ano.update_traces(marker_color='#0ce3e8')

        st.plotly_chart(fig_ano, use_container_width=True)



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

        nomes_selecionados = st.multiselect(
            "Selecione os nomes para comparar no gráfico radar:",
            df_automoveis['nome'].tolist(),
            default=df_automoveis['nome'].tolist()[:2]  
    )
    
        if nomes_selecionados:
            categorias = ['cilindrada', 'cavalos', 'peso', 'aceleracao']
            
            df_normalizado = dashboard.copy()
            for categoria in categorias:
                if categoria == 'aceleracao':
                    df_normalizado[categoria] = 1 - (
                        (dashboard[categoria] - dashboard[categoria].min()) / 
                        (dashboard[categoria].max() - dashboard[categoria].min())
                    )
                else:
                    df_normalizado[categoria] = (
                        (dashboard[categoria] - dashboard[categoria].min()) / 
                        (dashboard[categoria].max() - dashboard[categoria].min())
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
        
        peso_vs_cavalos = px.scatter(dashboard, x='peso', y='cavalos', color='origem', hover_name='nome', title="Peso vs Cavalos")
        gpm_vs_cavalos = px.scatter(dashboard, x='gpm', y='cavalos', color='origem', hover_name='nome', title="GPM vs Cavalos")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(peso_vs_cavalos, use_container_width=True)
        with col2:
            st.plotly_chart(gpm_vs_cavalos, use_container_width=True)

        st.markdown("### Análise de Potência por Tipo de Motor")
            
        df_automoveis['cilindros'] = df_automoveis['cilindros'].astype(str)
            
        fig_box = px.box(
            df_automoveis.sort_values('cilindros'),
            x='cilindros',
            y='cavalos',
            color='origem', 
            title='Distribuição de Potência (Cavalos) por Número de Cilindros',
            labels={'cilindros': 'Número de Cilindros', 'cavalos': 'Cavalos (HP)'}
            )
        st.plotly_chart(fig_box, use_container_width=True)  

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
        
        numeric_cols = df_automoveis.select_dtypes(include=['number']).columns
        
        df_automoveisR = df_automoveis.copy()
        df_automoveisR[numeric_cols] = df_automoveisR[numeric_cols].map(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
        )
        
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