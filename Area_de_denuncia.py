# main.py
import streamlit as st
from streamlit_option_menu import option_menu
from formularios import *
from acompanharDenuncia import *

st.set_page_config(page_title="Disk Denúncia",
                   page_icon="🖥️")

st.image('./images/logo-cyber-edux.jpeg')

# st.sidebar.image("./images/icone-cyber-edux.jpeg", use_column_width=True)
st.sidebar.header("Área de denúncia")

st.title("Seja Bem-vindo(a)")
st.write("Denunciar é fácil! Basta clicar no botão Fazer Denúncia, contar pra gente o que está acontecendo, e nós cuidaremos do resto. Vamos garantir que sua denúncia chegue às autoridades certas para que eles possam resolver o problema.")

# horizontal menu
selected2 = option_menu(None, ["Fazer Denúncia", "Acompanhar Denúncia"],
                        icons=['a', "list-task"],
                        menu_icon="cast", default_index=0, orientation="horizontal")


if selected2 == "Fazer Denúncia":
    criar_formulario_denuncia()

elif selected2 == "Acompanhar Denúncia":
    acompanhar_denuncia()
