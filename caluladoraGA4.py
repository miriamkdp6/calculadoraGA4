import streamlit as st
import pandas as pd
import locale

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Simulador de Custos GA4 360",
    page_icon="📊",
    layout="centered"
)

# --- FUNÇÕES DE CÁLCULO ---

def format_currency(value):
    """Formata um número como moeda brasileira (R$)."""
    try:
        # Tenta definir a localidade para português do Brasil
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(value, grouping=True, symbol=True)
    except locale.Error:
        # Fallback caso a localidade não esteja disponível
        return f"R$ {value:,.2f}"

def calculate_ga4_cost(monthly_events_in_millions):
    """
    Calcula o custo do GA4 360 com base no volume de eventos mensais.
    A lógica é baseada na tabela de preços de 2025.
    """
    if monthly_events_in_millions <= 0:
        return 0, "N/A"
        
    # Tabela de preços para 2025 (baseada na sua planilha)
    # Para os níveis A-E, o valor é fixo dentro da faixa.
    # Para o nível F, o cálculo é diferente.
    if monthly_events_in_millions <= 25:
        return 15274.50, "Nível A"
    elif monthly_events_in_millions <= 500:
        return 45821.75, "Nível B"
    elif monthly_events_in_millions <= 2500:
        return 76361.75, "Nível C"
    elif monthly_events_in_millions <= 10000:
        return 106886.75, "Nível D"
    elif monthly_events_in_millions <= 25000:
        return 152786.75, "Nível E"
    else:  # Acima de 25.000 milhões de eventos
        # Custo do tier anterior (E) + custo variável do excedente
        base_cost_tier_e = 152786.75
        overage_events = monthly_events_in_millions - 25000
        overage_cost = overage_events * 3.06  # Custo por milhão excedente
        total_cost = base_cost_tier_e + overage_cost
        return total_cost, "Nível F"

# --- INTERFACE DA APLICAÇÃO ---

# Título e introdução
st.title("📊 Simulador de Custos do GA4 360")
st.markdown("""
Esta ferramenta ajuda a estimar o custo do Google Analytics 4 360 com base no seu volume de eventos.
A simulação utiliza a **tabela de preços de 2025** fornecida.
""")

# --- BARRA LATERAL (SIDEBAR) PARA INPUTS ---
with st.sidebar:
    st.header("⚙️ Insira seus dados")
    
    # Usamos o valor da planilha (500M) como padrão
    monthly_events_input = st.number_input(
        label="Volume de eventos mensais (em milhões)",
        min_value=0.0,
        value=500.0,
        step=50.0,
        help="Informe a quantidade total de eventos que você espera registrar por mês, em milhões."
    )

# --- PAINEL PRINCIPAL PARA RESULTADOS ---
st.divider()

if monthly_events_input > 0:
    # Cálculo dos custos
    monthly_cost, price_tier = calculate_ga4_cost(monthly_events_input)
    annual_cost = monthly_cost * 12

    # Exibição dos resultados com st.metric para destaque
    st.subheader("📈 Sua Estimativa de Custo")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Seu Nível de Preço", value=price_tier)
    with col2:
        st.metric(label="Custo Mensal Estimado", value=format_currency(monthly_cost))
    with col3:
        st.metric(label="Custo Anual Estimado", value=format_currency(annual_cost))

    st.info(f"Com um volume de **{monthly_events_input:,.0f} milhões** de eventos por mês, sua empresa se enquadra no **{price_tier}**.".replace(',', '.'))

else:
    st.warning("Por favor, insira um volume de eventos maior que zero na barra lateral.")


# --- DETALHES DA TABELA DE PREÇOS ---
with st.expander("Clique para ver a Tabela de Preços de 2025"):
    st.markdown("""
    A tabela abaixo detalha as faixas de preço usadas para o cálculo. 
    Para os níveis de A a E, o valor mensal é fixo. Para o nível F, o cálculo é baseado no excedente de eventos.
    """)
    
    # Criando um DataFrame para exibir a tabela de forma organizada
    price_data = {
        "Nível": ["A", "B", "C", "D", "E", "F"],
        "Faixa de Eventos (Milhões)": [
            "0 - 25", "26 - 500", "501 - 2.500", "2.501 - 10.000",
            "10.001 - 25.000", "> 25.000"
        ],
        "Valor Fixo Mensal": [
            format_currency(15274.50), format_currency(45821.75), format_currency(76361.75),
            format_currency(106886.75), format_currency(152786.75), "Variável"
        ],
        "Cálculo": [
            "Valor Fixo", "Valor Fixo", "Valor Fixo", "Valor Fixo", "Valor Fixo",
            "Base do Nível E + R$ 3,06 por milhão excedente"
        ]
    }
    price_df = pd.DataFrame(price_data)
    st.dataframe(price_df, use_container_width=True, hide_index=True)

# Rodapé
st.divider()
st.caption("Esta é uma ferramenta de simulação. Os valores são estimativas e devem ser confirmados com seu representante de vendas.")
