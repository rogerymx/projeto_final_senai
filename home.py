import sqlite3
import pandas as pd
import streamlit as st
import base64
with open("carro_aviao.png", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()


def welcome (conn,cursor):

    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:50px;
        ">
            Dashboard LogCar
        </h1>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            width: 100%;
            height: 250px;
            background-image: url('data:image/png;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            border-radius: 10px;
            filter: brightness(0.5);
        ">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <hr style="height:2px; border:none; background-color:#1899A4; margin-top:30px; margin-bottom:30px;" />
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="
            text-align:center;
            font-size:35px;
        ">
            Navegação
        </h1>
    """, unsafe_allow_html=True)


    button_style = """
        <style>
            .home-nav-buttons {
                display: flex;
                justify-content: center;
                margin-bottom: 30px;
            }
            .home-nav-buttons .stButton>button {
                background-color: #1c1c1e;
                color: #A9A9A9;
                border: 1px solid rgba(24, 153, 164, 0.2);
                padding: 10px 24px;
                font-weight: 500;
                border-radius: 10px; /* Borda arredondada para todos */
                transition: all 0.3s ease-in-out;
            }
            .home-nav-buttons .stButton>button:hover {
                background-color: #1899A4;
                color: white;
                border-color: #1899A4;
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    st.markdown('<div class="home-nav-buttons">', unsafe_allow_html=True)
    nav_b1, nav_b2 = st.columns([1,1])

    with nav_b1:
        if st.button("🚗 Carros", use_container_width=True):
            st.session_state.global_opcao = 'Carro'
            st.rerun()

    with nav_b2:
        if st.button("✈️ Aviões", use_container_width=True):
            st.session_state.global_opcao = 'Avião'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <hr style="height:4px; border:none; background-color:#1899A4; margin-top:10px; margin-bottom:30px;" />
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown("""
        <div style="
            border: 1px solid rgba(24, 153, 164, 0.2); 
            background-color: #1c1c1e; 
            border-radius: 10px; 
            padding: 25px; 
            height: 100%;
        ">
            <h3 style="
                color: #1899A4; 
                text-align: center; 
                margin-top: 0; 
                font-weight: 600;
                border-bottom: 1px solid #2e2e2e;
                padding-bottom: 10px;
            ">Equipe</h3>
            <ul style="
                color: #D1D1D6; 
                list-style-position: inside;
                padding-left: 0;
                list-style-type: '👤 '; 
                line-height: 2.5;
            ">
                <li>Guilherme</li>
                <li>Pedro</li>
                <li>Roger</li>
                <li>Willian</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            border: 1px solid rgba(24, 153, 164, 0.2); 
            background-color: #1c1c1e; 
            border-radius: 10px; 
            padding: 25px; 
            height: 100%;
        ">
            <h3 style="
                color: #1899A4; 
                margin-top: 0;
                font-weight: 600;
                border-bottom: 1px solid #2e2e2e;
                padding-bottom: 10px;
            ">Sobre o Projeto</h3>
            <div style="color: #D1D1D6; text-align: justify; line-height: 1.7;">
                <p>Estamos desenvolvendo um dashboard de performance voltado para apoiar decisões estratégicas da empresa <strong>LogCar Air &amp; Mobility</strong>.</p>
                <p>O sistema visa reunir e visualizar de forma clara e interativa dados <strong>aéreos</strong> e <strong>terrestres</strong>, com indicadores e análises que permitam:</p>
                <ul style="padding-left: 20px; margin-top:15px;">
                    <li>Identificar ineficiências operacionais</li>
                    <li>Comparar desempenho por empresa, modelo ou região</li>
                    <li>Simular cenários de integração modal</li>
                    <li>Dar suporte à renovação da frota com base em dados</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <hr style="height:4px; border:none; background-color:#1899A4; margin-top:30px; margin-bottom:10px;" />
    """, unsafe_allow_html=True)