import sqlite3
import pandas as pd
import streamlit as st
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


def welcome (conn,cursor):
    st.markdown(banner_html, unsafe_allow_html=True)
    st.markdown("""
        <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:10px;" />
    """, unsafe_allow_html=True)

    # Título centralizado com sombra escura (borda)
    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:36px;
        ">
            Bem-vindo
        </h1>
    """, unsafe_allow_html=True)

    # Linha inferior decorativa
    st.markdown("""
        <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
    """, unsafe_allow_html=True)


    # Lista de nomes com fonte branca e borda escura
    st.markdown("""
        <ul style="
            font-size:18px;
            color:white;
            text-shadow: 1px 1px 3px black;
            line-height:1.6;
        ">
            <li>Nome 1</li>
            <li>Nome 2</li>
            <li>Nome 3</li>
            <li>Nome 4</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown("""
    <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:10px;" />
    """, unsafe_allow_html=True)
    st.markdown(bannerFooter_html, unsafe_allow_html=True)