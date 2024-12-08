import streamlit as st
import pandas as pd
import pickle

# Funções para salvar e carregar dados
def salvar_dados(dados, nome_arquivo):
    with open(nome_arquivo, "wb") as f:
        pickle.dump(dados, f)

def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

# Carregar dados ao iniciar
if "materiais" not in st.session_state:
    st.session_state.materiais = carregar_dados("materiais.pkl")
if "receitas" not in st.session_state:
    st.session_state.receitas = carregar_dados("receitas.pkl")

# Sessão 1: Cadastro de Materiais
st.title("Planejamento de Produção e Lucros")
st.sidebar.header("Configurações")

st.sidebar.subheader("Cadastro de Materiais")
nome_material = st.sidebar.text_input("Nome do Material")
preco_material = st.sidebar.number_input("Preço (R$)", min_value=0.0, step=0.01)
rendimento_material = st.sidebar.number_input("Rendimento (quantidade)", min_value=1, step=1)

if st.sidebar.button("Adicionar Material"):
    st.session_state.materiais.append({
        "Nome": nome_material,
        "Preço": preco_material,
        "Rendimento": rendimento_material
    })
    salvar_dados(st.session_state.materiais, "materiais.pkl")
    st.sidebar.success("Material salvo com sucesso!")

st.sidebar.subheader("Materiais Cadastrados")
st.sidebar.write(pd.DataFrame(st.session_state.materiais))

# Sessão 2: Cadastro de Receitas
st.subheader("Cadastro de Receitas")
nome_receita = st.text_input("Nome da Receita")
ingredientes = st.text_area("Ingredientes (ex.: 200g de farinha, 1 lata de leite condensado)")

if st.button("Adicionar Receita"):
    st.session_state.receitas.append({
        "Nome": nome_receita,
        "Ingredientes": ingredientes
    })
    salvar_dados(st.session_state.receitas, "receitas.pkl")
    st.success("Receita salva com sucesso!")

st.write("Receitas Cadastradas:")
st.write(pd.DataFrame(st.session_state.receitas))

# Sessão 3: Planejamento de Produção
st.subheader("Planejamento de Produção")
planejamento = []
for receita in st.session_state.receitas:
    qtd = st.number_input(f"Quantidade de {receita['Nome']} para produzir", min_value=0, step=1)
    planejamento.append({"Receita": receita['Nome'], "Quantidade": qtd})

st.write("Planejamento Atual:")
st.write(pd.DataFrame(planejamento))

# Sessão 4: Resumo Financeiro
st.subheader("Resumo Financeiro")
st.write("Implementação futura: Resumo detalhado com custos e lucros!")

# Botão para reiniciar os dados
st.sidebar.subheader("Gerenciar Dados")
if st.sidebar.button("Limpar Materiais"):
    st.session_state.materiais = []
    salvar_dados([], "materiais.pkl")
    st.sidebar.warning("Todos os materiais foram excluídos!")

if st.sidebar.button("Limpar Receitas"):
    st.session_state.receitas = []
    salvar_dados([], "receitas.pkl")
    st.sidebar.warning("Todas as receitas foram excluídas!")
