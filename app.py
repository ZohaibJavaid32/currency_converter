import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", layout="centered")

st.title("💱 Currency Converter")

# Currency list
currencies = [
    "USD", "EUR", "GBP", "INR", "PKR", "AED", "SAR",
    "JPY", "CAD", "AUD", "CNY"
]

# Inputs
amount = st.number_input("Enter Amount", min_value=0.0, value=1.0)

col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From", currencies)

with col2:
    to_currency = st.selectbox("To", currencies)

# API function
def get_exchange_rate(from_curr, to_curr):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_curr]

# Convert button
if st.button("Convert"):
    try:
        rate = get_exchange_rate(from_currency, to_currency)
        result = amount * rate

        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        st.info(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")

        # Store history
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append(
            f"{amount} {from_currency} → {result:.2f} {to_currency}"
        )

    except Exception as e:
        st.error("Error fetching exchange rates")

# Show history
if "history" in st.session_state:
    st.markdown("### 📜 Conversion History")
    for item in reversed(st.session_state.history[-5:]):
        st.write(item)