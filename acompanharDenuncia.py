import streamlit as st


def acompanhar_denuncia():
    login = st.toggle('Anônimo')
    if login == False:
        st.write("Digite seu CPF para fazer LOGIN")
        cpf = st.text_input('CPF: ')
    if login == True:
        id = st.text_input('ID: ')
    st.button("Login")
