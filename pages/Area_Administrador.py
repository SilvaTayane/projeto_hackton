import streamlit as st
from mapa import *
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Disk Denúncia",
                   page_icon="🖥️")

st.image('./images/logo-cyber-edux.jpeg')

# st.sidebar.image("./images/icone-cyber-edux.jpeg", use_column_width=True)
st.sidebar.header("Área do Administrador")

st.title("Área do Administrador")
st.write("Esta área do site é exclusiva para administradores. Somente usuários autorizados têm permissão para acessá-la. Se você não é um administrador, por favor, retorne à página principal.")

# horizontal menu
selected2 = option_menu(None, ["Histórico de denúncia", "Login Adm"],
                        icons=['a', "list-task"],
                        menu_icon="cast", default_index=0, orientation="horizontal")


if selected2 == "Histórico de denúncia":
    exibir_mapa_reclamacoes()

elif selected2 == "Login Adm":
    st.text_input("Usuário")
    st.text_input("Senha:")
    st.button("Login")
