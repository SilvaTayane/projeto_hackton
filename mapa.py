# mapa.py
import streamlit as st
import streamlit_folium
import folium
import sqlite3
from formularios import *
import pandas as pd
import io

def create_excel_report(report_data):
    buffer = io.BytesIO()

    # Salvar DataFrame para Excel
    report_data.to_excel(buffer, index=False, sheet_name="Relatório de Denúncias")

    # Retornar os dados do Excel
    buffer.seek(0)
    return buffer.read()



def exibir_mapa_reclamacoes():
    con = sqlite3.connect('denuncia.db')
    cur = con.cursor()

    st.header("Historico de denuncias")

    mapa = folium.Map(location=[-15.6010, -56.0974],
                      zoom_start=12)


    coordenadas = cur.execute("select latitude,longitude from local")
    coordenadas = coordenadas.fetchall()

    for coord in coordenadas:
        folium.Marker(location=coord).add_to(mapa)

    st_folium = streamlit_folium.st_folium(mapa, width=800, height=600)

    with st.expander("Relatório"):
        cont_denun = cur.execute("select count(id_denuncia) from denuncia").fetchone()[0]
        st.write(f"Quantidade de denuncias: {cont_denun}")

        """'Vazamentos', 'Esgotos a céu aberto', 'Buracos nas vias', 'Fiação elétrica',
                'Lixo acumulado', 'Falta de internet', 'Poda de árvores', 'Outros'"""

        cont_vazamento = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Vazamentos';''').fetchone()[0]

        cont_esgoto = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Esgotos a céu aberto';''').fetchone()[0]
        
        cont_buraco = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Buracos nas vias';''').fetchone()[0]
        
        cont_fiacao = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Fiação elétrica';''').fetchone()[0]
        cont_lixo = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Lixo acumulado';''').fetchone()[0]
        cont_internet = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Falta de internet';''').fetchone()[0]
        cont_poda = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Poda de árvores';''').fetchone()[0]
        cont_outros = cur.execute('''
                                SELECT COUNT(tipo_denuncia)
                                FROM denuncia
                                WHERE tipo_denuncia = 'Outros';''').fetchone()[0]
        
        chart_data = pd.DataFrame({
            'Tipo de Denúncia': ['Vazamentos', 'Esgotos a céu aberto', 'Buracos nas vias', 'Fiação elétrica', 'Lixo acumulado', 'Falta de internet', 'Poda de árvores', 'Outros'],
            'Contagem': [cont_vazamento, cont_esgoto, cont_buraco, cont_fiacao, cont_lixo, cont_internet, cont_poda, cont_outros]
        })

        # Criando o gráfico de barras usando o Streamlit
        st.bar_chart(chart_data.set_index('Tipo de Denúncia'))






        report_data = pd.DataFrame({
            'Tipo de Denúncia': ['Vazamentos', 'Esgotos a céu aberto', 'Buracos nas vias', 'Fiação elétrica', 'Lixo acumulado', 'Falta de internet', 'Poda de árvores', 'Outros'],
            'Contagem': [cont_vazamento, cont_esgoto, cont_buraco, cont_fiacao, cont_lixo, cont_internet, cont_poda, cont_outros]
        })

        # Adicionando informações adicionais ao relatório, se necessário
        report_data['Descrição'] = [
            'Problemas relacionados a vazamentos de água.',
            'Situações de esgotos a céu aberto.',
            'Buracos nas vias públicas que precisam de reparo.',
            'Questões relacionadas à fiação elétrica.',
            'Acúmulo de lixo em áreas públicas.',
            'Problemas de falta de internet na região.',
            'Solicitações de poda de árvores.',
            'Outros problemas não categorizados.'
        ]

        # Exibindo o DataFrame no Streamlit
        st.write(report_data)

        excel_data = create_excel_report(report_data)
        st.download_button(
            label="Baixar Relatório Excel",
            data=excel_data,
            file_name="relatorio_denuncias.xlsx",
            key="download_button"
        )

    con.commit()
    con.close()
    