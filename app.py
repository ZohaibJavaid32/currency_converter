import streamlit as st
import requests

st.set_page_config(page_title="Currency Converter", layout="centered")

# ------------------ UI HEADER ------------------ #
st.title("💱 Currency Converter")
st.markdown("Convert currencies in real-time using live exchange rates.")

# ------------------ CURRENCY LIST ------------------ #
currencies = {
    "USD 🇺🇸": "USD",
    "EUR 🇪🇺": "EUR",
    "GBP 🇬🇧": "GBP",
    "INR 🇮🇳": "INR",
    "PKR 🇵🇰": "PKR",
    "AED 🇦🇪": "AED",
    "SAR 🇸🇦": "SAR",
    "JPY 🇯🇵": "JPY",
    "CAD 🇨🇦": "CAD",
    "AUD 🇦🇺": "AUD",
    "CNY 🇨🇳": "CNY"
}

currency_names = list(currencies.keys())

# ------------------ SESSION STATE ------------------ #
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ INPUTS ------------------ #
amount = st.number_input("Enter Amount", min_value=0.0, value=1.0)

col1, col2 = st.columns(2)

with col1:
    from_curr_display = st.selectbox("From", currency_names, index=0)

with col2:
    to_curr_display = st.selectbox("To", currency_names, index=4)

from_currency = currencies[from_curr_display]
to_currency = currencies[to_curr_display]

# ------------------ SWAP BUTTON ------------------ #
if st.button("🔄 Swap"):
    st.session_state.from_curr = to_currency
    st.session_state.to_curr = from_currency
    st.rerun()

# ------------------ API FUNCTION ------------------ #
@st.cache_data(ttl=3600)
def get_rates(base):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url)
    return response.json()

# ------------------ AUTO CONVERT ------------------ #
if amount > 0:
    try:
        data = get_rates(from_currency)
        rate = data["rates"][to_currency]
        result = amount * rate

        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        st.info(f"1 {from_currency} = {rate:.4f} {to_currency}")

        # Save history
        st.session_state.history.append(
            f"{amount} {from_currency} → {result:.2f} {to_currency}"
        )

    except:
        st.error("⚠️ Error fetching exchange rates")

# ------------------ HISTORY ------------------ #
if st.session_state.history:
    st.markdown("### 📜 Conversion History")
    for item in reversed(st.session_state.history[-5:]):
        st.write(item)

# ------------------ CLEAR HISTORY ------------------ #
if st.button("🗑 Clear History"):
    st.session_state.history = []
    st.rerun()

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.markdown("Made by Zohaib 🚀")