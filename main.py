import sqlite3
import pandas as pd
import streamlit as st
import auto as at
import home as hm
import air as ai
from PIL import Image
import base64
from io import BytesIO
st.set_page_config(layout="wide",)

def img():
    imagem = Image.open("./logo.png")
    imagem_redimensionada = imagem.resize((200, 200))

    buffered = BytesIO()
    imagem_redimensionada.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="data:image/png;base64,{img_base64}" width="150" height="150">'
        f'</div>',
        unsafe_allow_html=True
    )
with st.sidebar:
    img()
    st.divider()

conn = sqlite3.connect('./database/automobile.db')
cursor = conn.cursor()
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


col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.global_opcao = 'Home'
with col2:
    if st.button("Carro"):
        st.session_state.global_opcao = 'Carro'
with col3:
    if st.button("Avião"):
        st.session_state.global_opcao = 'Avião'

if 'global_opcao' not in st.session_state:
    st.session_state.global_opcao = 'Home'

if st.session_state.global_opcao == 'Carro':
    at.auto(conn, cursor)
elif st.session_state.global_opcao == 'Avião':
    ai.air()
elif st.session_state.global_opcao == 'Home':
    hm.welcome(conn, cursor)