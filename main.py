import sqlite3
import pandas as pd
import streamlit as st
import auto as at
import home as hm
import air as ai
conn = sqlite3.connect('./database/automobile.db')
cursor = conn.cursor()

# def create_tables(conn, cursor):
    # Criação de todas as tabelas necessárias
    
    # Criação da tabela 
cursor.execute('''
CREATE TABLE IF NOT EXISTS automoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    gpm INTEGER NOT NULL,
    cilindros INTEGER NOT NULL,
    cilindrada INTEGER NOT NULL,
    cavalos INTEGER NOT NULL,
    peso INTEGER NOT NULL,
    aceleracao INTEGER NOT NULL,
    ano_modelo INTEGER NOT NULL,
    origem TEXT NOT NULL,
    montadora TEXT NOT NULL
)
''')

cursor.execute("SELECT COUNT(*) FROM automoveis")
if cursor.fetchone()[0] == 0:
    df_automoveis = pd.read_csv('database/automobile.csv')
    df_automoveis['montadora'] = df_automoveis['nome'].str.split(' ').str[0]
    df_automoveis['nome'] = df_automoveis['nome'].str.split(' ').str[1:].str.join(' ')
    df_automoveis_sem_nulos = df_automoveis.dropna()
    df_automoveis_sem_nulos.to_sql('automoveis', conn, if_exists='append', index=False)

opcao = st.sidebar.selectbox("Selecione: ", ['Home','Carro', 'Avião'], key="main_select")

if opcao == 'Carro':
    st.write(opcao)
    at.auto(conn,cursor)
    
elif opcao == 'Avião':
    ai.air()

elif opcao == 'Home':
    hm.welcome(conn,cursor)