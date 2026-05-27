import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Dashboard Academia",
    layout="wide"
)

# =========================================
# CONEXÃO COM POSTGRESQL
# Senha: 123456
# Banco: academia_dashboard
# =========================================
engine = create_engine(
    "postgresql+psycopg2://postgres:123456@localhost/academia_dashboard"
)

# =========================================
# LEITURA DAS TABELAS
# =========================================
alunos = pd.read_sql(
    "SELECT * FROM alunos",
    engine
)

planos = pd.read_sql(
    "SELECT * FROM planos",
    engine
)

matriculas = pd.read_sql(
    "SELECT * FROM matriculas",
    engine
)

pagamentos = pd.read_sql(
    "SELECT * FROM pagamentos",
    engine
)

# =========================================
# KPIs
# =========================================
total_alunos = alunos.shape[0]

receita_total = pagamentos[
    pagamentos["status_pagamento"] == "Pago"
]["valor_pago"].sum()

matriculas_ativas = matriculas[
    matriculas["status"] == "Ativa"
].shape[0]

media_planos = planos["valor"].mean()

# =========================================
# TÍTULO
# =========================================
st.title("🏋️ Dashboard da Academia")

st.markdown("---")

# =========================================
# KPIs
# =========================================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de Alunos",
    total_alunos
)

col2.metric(
    "Receita Total",
    f"R$ {receita_total:.2f}"
)

col3.metric(
    "Matrículas Ativas",
    matriculas_ativas
)

col4.metric(
    "Média dos Planos",
    f"R$ {media_planos:.2f}"
)

st.markdown("---")

# =========================================
# GRÁFICO 1 - PLANOS MAIS VENDIDOS
# =========================================
query1 = """
SELECT
    p.nome_plano,
    COUNT(*) AS quantidade
FROM matriculas m
JOIN planos p
ON m.id_plano = p.id_plano
GROUP BY p.nome_plano
ORDER BY quantidade DESC
"""

grafico1 = pd.read_sql(query1, engine)

fig1 = px.bar(
    grafico1,
    x="nome_plano",
    y="quantidade",
    text_auto=True,
    title="📊 Planos Mais Vendidos",
    template="plotly_dark"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================================
# GRÁFICO 2 - SITUAÇÃO DOS PAGAMENTOS
# =========================================
query2 = """
SELECT
    status_pagamento,
    COUNT(*) AS total
FROM pagamentos
GROUP BY status_pagamento
"""

grafico2 = pd.read_sql(query2, engine)

fig2 = px.pie(
    grafico2,
    names="status_pagamento",
    values="total",
    title="💰 Situação dos Pagamentos",
    template="plotly_dark"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================
# GRÁFICO 3 - CRESCIMENTO DE ALUNOS
# =========================================
query3 = """
SELECT
    TO_CHAR(data_cadastro, 'YYYY-MM') AS mes,
    COUNT(*) AS total_alunos
FROM alunos
GROUP BY mes
ORDER BY mes
"""

grafico3 = pd.read_sql(query3, engine)

fig3 = px.line(
    grafico3,
    x="mes",
    y="total_alunos",
    markers=True,
    title="📈 Crescimento de Alunos por Mês",
    template="plotly_dark"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("---")

st.success("✅ Dashboard carregado com sucesso!")
