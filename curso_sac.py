# formularios.py
import streamlit as st
from geopy.geocoders import Nominatim
import sqlite3


def obter_coordenadas(endereco):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(endereco)

    if location:
        return location.latitude, location.longitude
    else:
        return None


def criar_formulario_denuncia():
    con = sqlite3.connect('denuncia.db')
    cur = con.cursor()

    coordenadas = ()
    button_pressed = False

    st.header("Formulário de Reclamações")

    Endereço = st.text_input('Endereço:')
    Município = st.text_input('Município:')

    endereco = f"{Endereço} {Município}"
    on = st.toggle('Anônimo')

    if st.button("Buscar Endereço") and endereco:
        coordenadas = obter_coordenadas(endereco)

        if coordenadas:
            st.success(f"Endereço encontrado")
        else:
            st.warning("Não foi possível encontrar o endereço fornecido.")

    with st.form(key="Formulário de reclamação:"):
        if on == False:
            nome_completo = st.text_input('Nome Completo:')
            cpf = st.text_input('CPF: ')
        if on == True:
            nome_completo = 'anonimo'
            cpf = 'anonimo'
        option = st.selectbox(
            'Selecione o problema',
            ('Vazamentos', 'Esgotos a céu aberto', 'Buracos nas vias', 'Fiação elétrica',
                'Lixo acumulado', 'Falta de internet', 'Poda de árvores', 'Outros'),
            index=None,
            placeholder="-------",
        )

        ponto_referencia = st.text_input('Ponto de referência:')
        comentario = st.text_input('Comentário: ')

        button_pressed = st.form_submit_button('Enviar')

    if button_pressed:

        cur.execute('''insert into pessoa(nome_completo,cpf)
                    values (?,?)''', (nome_completo, cpf))
        pessoa_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        cur.execute('''insert into denuncia(tipo_denuncia,comentario)
                    values (?,?)''', (option, comentario))
        denuncia_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        cur.execute('''insert into local(endereco, ponto_de_referencia)
                    values (?,?)''', (endereco, ponto_referencia))
        local_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        cur.execute('''insert into faz(id_pessoa, id_denuncia)
                    values (?,?)''', (pessoa_id, denuncia_id))

        cur.execute('''insert into pertence(id_local, id_denuncia)
                    values (?,?)''', (local_id, denuncia_id))
        con.commit()
        con.close()

        if st.button('Denúncia realizada com sucesso!'):
            st.experimental_rerun()
