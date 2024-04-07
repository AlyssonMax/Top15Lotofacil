import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Indicações de Jogos Lotofácil")
st.title('_Números mais frequentes do_ :blue[LOTOFÁCIL] :money_with_wings:')

# Explicação da criação do app e de como funciona a lógica aplicada
with st.container():
    st.subheader('**JUSTIFICATIVA**')
    st.write('Este síte foi desenvolvido com intuito de aprendizado e não visa prever quais serão os próximos número sorteados. Todas as sequências de 15 números tem a mesma probabilidade de serem sorteadas.')
    st.write('Este aplicativo busca os 10 últimos jogos da lotofácil realizados  no site https://www.somatematica.com.br/lotofacilResultados.php e calcula a frequência que cada número apareceu. No fim da página disponibilizamos os 15 números que mais saíram até agora e os 15 números que saíram até 9 vezes.')
with st.container():

    # URL da página web de onde você quer extrair os números
    url = 'https://www.somatematica.com.br/lotofacilResultados.php'

    # Enviar solicitação HTTP para a página web
    resposta = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida
    if resposta.status_code == 200:
        # Analisar o conteúdo HTML da página
        soup = BeautifulSoup(resposta.text, 'html.parser')

with st.container():
    # Encontrar todas as <div> com o atributo align
    divs = soup.find_all('div', {'align': True})

    # Extrair as linhas de texto de cada <div>
    ultimos_jogos = []
    for div in divs:
        # Separar as linhas de texto usando <br> como separador
        linhas = div.get_text(separator='|').split('|')
        # Filtrar para garantir que apenas linhas com números sejam capturadas
        linhas_de_numeros = [linha for linha in linhas if re.search(r'\d', linha)]
        # Verificar se há exatamente 3 linhas de números
        if len(linhas_de_numeros) == 3:
            # Extrair os números de cada linha
            numeros = re.findall(r'\b\d{2}\b', ' '.join(linhas_de_numeros))
            # Verificar se há exatamente 15 números
            if len(numeros) == 15:
                # Adicionar ao grupo final
                ultimos_jogos.append(', '.join(numeros))
    st.write("---")

with st.container():
    # Imprimir cada grupo de 15 números em uma linha diferente
    st.subheader("Ultimos 10 jogos realizados:", divider='rainbow')
    for jogo in ultimos_jogos:
        st.write(jogo)
    st.write("---")

    # Converter a lista de strings para uma lista de inteiros
    numeros = [int(num) for jogo in ultimos_jogos for num in jogo.split(', ') if int(num) != 0]

    # Contar a frequência de cada número
    frequencias = Counter(numeros)

    # Criar um DataFrame a partir do dicionário de frequências
    df = pd.DataFrame(list(frequencias.items()), columns=['Número', 'Frequência'])

    # Ordenar o DataFrame pelo número
    df = df.sort_values(by='Número')

    # Título dos gráfico
    st.subheader(":yellow[GRÁFICOS:]", divider='rainbow')

    # Usar o Streamlit para criar um gráfico de barras
    st.bar_chart(df.set_index('Número'))
    st.caption(':red[gráfico em barras] :bar_chart:')
    st.write("---")

    # Definir a coluna 'Número' como índice do DataFrame
    df.set_index('Número', inplace=True)

    # Gráfico
    st.scatter_chart(df)
    st.caption(':red[gráfico em pontos] :bar_chart:')
    st.write("---")

with st.container():
    # Encontrar os 5 números mais e menos frequentes
    cinco_mais_frequentes = frequencias.most_common(5)
    cinco_menos_frequentes = frequencias.most_common()[:-6:-1]

    # Imprimir os resultados
    st.subheader(':red[NÚMEROS QUE MAIS SAIRAM]: ', divider='rainbow')
    for numero in cinco_mais_frequentes:
        st.write(f':green[Número]: {numero[0]}, :gray[Frequência]: {numero[1]}')
    st.write("---")

    st.subheader(':red[NÚMEROS QUE MENOS SAIRAM]: ', divider='rainbow')
    for numero in cinco_menos_frequentes:
        st.write(f':green[Número]: {numero[0]}, :gray[Frequência]: {numero[1]}')

    # Crie um dicionário para armazenar a contagem de cada número
    contagem_numeros = {}

with st.container():
    # Separe os números dos jogos e conte as ocorrências
    for jogo in ultimos_jogos:
        numeros = [int(num) for num in jogo.split(', ')]
        for num in numeros:
            contagem_numeros[num] = contagem_numeros.get(num, 0) + 1

    # Ordenar os números pela quantidade de vezes que aparecem, em ordem decrescente
    numeros_ordenados = sorted(contagem_numeros.items(), key=lambda x: x[1], reverse=True)

    # Pegar apenas os 15 números mais frequentes
    quinze_mais_frequentes = numeros_ordenados[:15]

    # Criar uma lista para os números que serão impressos, ignorando os que apareceram 10 vezes
    numeros_para_imprimir = []
    ignorados = set()

    # Iterar sobre os números ordenados
    for numero, quantidade in numeros_ordenados:
        # Se o número já apareceu 10 vezes, ignorá-lo
        if quantidade == 10:
            ignorados.add(numero)
        # Adicionar o número à lista se ele não estiver entre os 15 mais frequentes e não tiver sido ignorado
        elif numero not in ignorados:
            numeros_para_imprimir.append(numero)
        # Parar quando tiver 15 números
        if len(numeros_para_imprimir) == 15:
            break
    st.write("---")
    # Imprimir os 15 números mais frequentes de forma enfileirada
    numeros_finais = ', '.join(str(num[0]) for num in quinze_mais_frequentes)
    st.subheader(":rainbow[Números que mais se repetiram: ]")
    st.subheader(numeros_finais)
    st.write("---")
    # Imprimir os números ajustados de acordo com a nova regra
    numeros_ajustados = ', '.join(str(num) for num in numeros_para_imprimir)
    st.subheader(":rainbow[Números que saíram até 9 vezes: ]")
    st.subheader(numeros_ajustados)
    st.write("---")