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


def encaminhar_orgao_responsavel(Município, option):
    if Município.lower() in ['cuiabá', 'cuiaba']:
        if option in ['Vazamentos', 'Esgotos a céu aberto']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: Águas Cuiaba")
        elif option in ['Buracos nas vias']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: Infraestrutura de Cuiabá")
        elif option in ['Fiação elétrica', 'Falta de internet']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: Energisa de Cuiabá")
        elif option in ['Lixo acumulado', 'Poda de árvores']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: limpurb de Cuiabá")
        elif option in ['Outros']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão a Analise da Prefeitura de Cuiabá")
    else:
        if option in ['Vazamentos', 'Esgotos a céu aberto']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: DAE De Varzéa Grande")
        elif option in ['Buracos nas vias']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: Infraestrutura De Varzéa Grande")
        elif option in ['Fiação elétrica', 'Falta de internet']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: Energisa De Varzéa Grande")
        elif option in ['Lixo acumulado', 'Poda de árvores']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão: limpurb De Varzéa Grande")
        elif option in ['Outros']:
            st.success(
                "Sua denuncia foi encaminhada para o Orgão a Analise da Prefeitura De Varzéa Grande")


def criar_formulario_denuncia():
    con = sqlite3.connect('denuncia.db')
    cur = con.cursor()

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
        if on:
            nome_completo = 'anonimo'
            cpf = 'anonimo'
        else:
            nome_completo = st.text_input('Nome Completo:')
            cpf = st.text_input('CPF: ')

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

        st.success("Formulario enviado com sucesso!")

        encaminhar_orgao_responsavel(Município, option)

        cont_pessoa = cur.execute('''Select count(id_pessoa) from pessoa''')
        cont_pessoa = cont_pessoa.fetchone()[0]

        if on:
            st.success('Acompanhe sua denuncia Usando o Seu ID: ',
                       cont_pessoa+1)
        else:
            st.success('Acompanhe sua denuncia Usando o Seu CPF')

        cur.execute('''insert into pessoa(nome_completo,cpf)
                    values (?,?)''', (nome_completo, cpf))
        pessoa_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        cur.execute('''insert into denuncia(tipo_denuncia,comentario)
                    values (?,?)''', (option, comentario))
        denuncia_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        coordenadas = obter_coordenadas(endereco)

        cur.execute('''insert into local(endereco, ponto_de_referencia,latitude,longitude)
                    values (?,?,?,?)''', (endereco, ponto_referencia, coordenadas[0], coordenadas[1]))
        local_id = con.execute('SELECT last_insert_rowid()').fetchone()[0]

        cur.execute('''insert into faz(id_pessoa, id_denuncia)
                    values (?,?)''', (pessoa_id, denuncia_id))

        cur.execute('''insert into pertence(id_local, id_denuncia)
                    values (?,?)''', (local_id, denuncia_id))
        con.commit()
        con.close()
