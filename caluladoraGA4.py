import streamlit as st
import pandas as pd
import locale

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Simulador de Investimento GA4 360",
    page_icon="📊",
    layout="centered"
)

# --- FUNÇÕES DE CÁLCULO ---

def format_currency(value):
    """Formata um número como moeda (R$)."""
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(value, grouping=True, symbol=True)
    except locale.Error:
        return f"R$ {value:,.2f}"

def calculate_ga4_cost(events):
    """
    Calcula o investimento no GA4 360 e determina o NÍVEL DE REFERÊNCIA para o cálculo.
    """
    if events <= 0:
        return 0, "N/A"
    
    if events <= 25:
        cost = 15274.50
        tier_label = "Nível A"
    elif events <= 500:
        base_cost = 15274.50
        overage_events = events - 25
        cost = base_cost + (overage_events * 64.31)
        tier_label = "Nível A"
    elif events <= 2500:
        base_cost = 45821.75
        overage_events = events - 500
        cost = base_cost + (overage_events * 15.27)
        tier_label = "Nível B"
    elif events <= 10000:
        base_cost = 76361.75
        overage_events = events - 2500
        cost = base_cost + (overage_events * 4.07)
        tier_label = "Nível C"
    elif events <= 25000:
        base_cost = 106886.75
        overage_events = events - 10000
        cost = base_cost + (overage_events * 3.06)
        tier_label = "Nível D"
    else:
        base_cost = 152786.75
        overage_events = events - 25000
        cost = base_cost + (overage_events * 3.06)
        tier_label = "Nível E"
        
    return cost, tier_label

# --- INTERFACE DA APLICAÇÃO ---

st.title("📊 Simulador de Custos do GA4 360")
st.markdown("""
Esta ferramenta ajuda a estimar o investimento em Google Analytics 4 360 com base no seu volume de eventos.
""")

with st.sidebar:
    st.header("⚙️ Insira seus dados")
    # O valor inicial agora é 0.0, para o campo começar "vazio".
    monthly_events_input = st.number_input(
        label="Volume de eventos mensais (em milhões)",
        min_value=0.0,
        value=0.0,
        step=10.0,
        help="Informe a quantidade total de eventos que você espera registrar por mês, em milhões."
    )

st.divider()

if monthly_events_input > 0:
    monthly_cost, reference_tier = calculate_ga4_cost(monthly_events_input)
    annual_cost = monthly_cost * 12

    st.subheader("📈 Sua Estimativa de Custo")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Nível de Referência", value=reference_tier)
    with col2:
        st.metric(label="Custo Mensal Estimado", value=format_currency(monthly_cost))
    with col3:
        st.metric(label="Custo Anual Estimado", value=format_currency(annual_cost))

    st.info(f"Para **{monthly_events_input:,.0f} milhões** de eventos, seu custo é calculado usando o **{reference_tier}** como base.".replace(',', '.'))
else:
    # Esta mensagem aparecerá quando a aplicação iniciar, pois o valor será 0.
    st.warning("Por favor, insira um volume de eventos maior que zero na barra lateral para calcular.")

with st.expander("Clique para ver os detalhes do cálculo"):
    st.markdown("""
    O cálculo é feito com base no custo total do nível anterior mais um valor variável para os eventos excedentes.
    O **Nível de Referência** indica qual faixa de preço foi usada como base para o seu cálculo.
    """)
    
    price_data = {
        "Nível": ["A", "B", "C", "D", "E", "F"],
        "Faixa (Milhões)": ["0-25", "25-500", "500-2.500", "2.500-10.000", "10.000-25.000", "> 25.000"],
        "Valor por Milhão Excedente": ["-", format_currency(64.31), format_currency(15.27), format_currency(4.07), format_currency(3.06), format_currency(3.06)],
        "Cálculo do Investimento Mensal": [
            "Valor Fixo de R$ 15.274,50",
            "R$ 15.274,50 + (Eventos - 25M) * R$ 64,31",
            "R$ 45.821,75 + (Eventos - 500M) * R$ 15,27",
            "R$ 76.361,75 + (Eventos - 2.500M) * R$ 4,07",
            "R$ 106.886,75 + (Eventos - 10.000M) * R$ 3,06",
            "R$ 152.786,75 + (Eventos - 25.000M) * R$ 3,06"
        ]
    }
    price_df = pd.DataFrame(price_data)
    st.dataframe(price_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("Esta é uma ferramenta de simulação. Os valores são estimativas e devem ser confirmados com seu representante de vendas.")
