# app resultado de ações
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

def carregar_dados(empresas):
    # Baixa cotações desde 2024 até hoje
    cotacoes_acao = yf.download(empresas, start='2024-01-01')

    print("Shape original:", cotacoes_acao.shape)
    print("Colunas originais:", cotacoes_acao.columns)

    # Seleciona apenas fechamento
    cotacoes_acao = cotacoes_acao["Close"]

    # Se ainda for MultiIndex, pega apenas o ticker
    if isinstance(cotacoes_acao.columns, pd.MultiIndex):
        cotacoes_acao.columns = cotacoes_acao.columns.droplevel(0)

    cotacoes_acao.columns.name = None

    return cotacoes_acao

# Lista de ações
acoes = ["ITUB4.SA", "BBAS3.SA", "VALE3.SA", "ABEV3.SA", "MGLU3.SA", "PETR4.SA", "GGBR4.SA"]

# Carrega os dados
dados = carregar_dados(acoes)

# Verificação: se não veio nenhum dado
if dados.empty:
    st.error("⚠ Não foi possível carregar dados para o período informado.")
else:
    # Debug
    print("Tipo de 'dados':", type(dados))
    print("Primeiras linhas de 'dados':")
    print(dados.head())

    # Texto no Streamlit
    st.write("""
    # App Preço de Ações
    O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
    """)

    # Escolha das ações
    lista_acoes = st.multiselect("Escolha as ações para exibir no gráfico", dados.columns.tolist(), default=dados.columns.tolist())
    print("Ações selecionadas:", lista_acoes)

    # Se não selecionar nada, mostra todas
    if lista_acoes:
        dados_filtrados = dados[lista_acoes]
    else:
        dados_filtrados = dados

    # Plota o gráfico
    st.line_chart(dados_filtrados)

    st.write("""
    # Fim do app
    """)
