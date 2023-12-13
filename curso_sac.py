import streamlit as st

st.set_page_config(page_title="Smart City")
st.title("Formulário de denúncia")


d = {}
with st.form("Formulário de reclamação:"):
    d['nome'] = st.text_input('Nome Completo:')
    d['telefone'] = st.text_input('Telefone: ')

    option = st.selectbox(
        'Selecione o problema',
        ('Vazamentos', 'Esgotos a céu aberto', 'Buracos nas vias', 'Fiação elétrica', 'Lixo acumulado', 'Falta de internet', 'Poda de árvores', 'Outros'),

        index=None,
        placeholder="-------",
    )
    
    d['endereco'] = st.text_input('Endereço:')
    d['ponto_referencia'] = st.text_input('Ponto de referência:')
    d['comentário'] = st.text_area('Um comentário: ')

    button_pressed = st.form_submit_button('Enviar')
    if button_pressed:
        st.write("Denúncia concluída com sucesso!\n")


