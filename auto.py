import sqlite3
import pandas as pd
import streamlit as st
import database

def auto (conn,cursor):
    df_automoveis = pd.read_csv('database/automobile.csv')
    
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
        Select * from automoveis
    ''',conn)
    st.dataframe(teste)