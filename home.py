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
            margin: 0;
        ">
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
        <div style='
            text-align:center;
            font-size:28px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        '>Equipe</div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
        <ul style="
            font-size:18px;
            color:white;
            text-shadow: 1px 1px 3px black;
            line-height:1.8;
            padding-left: 20px;
            margin-bottom: 30px;
            list-style-type: '👤 ';
        ">
            <li><strong>Guilherme</strong></li>
            <li><strong>Pedro</strong></li>
            <li><strong>Roger</strong></li>
            <li><strong>Willian</strong></li>
        </ul>
    """, unsafe_allow_html=True)


    st.divider()
    st.markdown("""
        <div style="
            font-size: 18px;
            line-height: 1.8;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p><strong>Estamos desenvolvendo um dashboard de performance</strong> voltado para apoiar decisões estratégicas da empresa <strong>LogCar Air &amp; Mobility</strong>.</p>
            <p>O sistema visa reunir e visualizar de forma clara e interativa dados <strong>aéreos</strong> (voos, passageiros, carga, combustível) e <strong>terrestres</strong> (modelos de carros, consumo, aceleração etc.), com indicadores e análises que permitam:</p>
            <ul style="margin-left: 20px;">
                <li>Identificar ineficiências operacionais</li>
                <li>Comparar desempenho por empresa, modelo ou região</li>
                <li>Simular cenários de integração modal</li>
                <li>Dar suporte à renovação da frota com base em dados</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:10px;" />
    """, unsafe_allow_html=True)

    st.markdown(bannerFooter_html, unsafe_allow_html=True)