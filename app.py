import streamlit as st

st.set_page_config(page_title="Insurance Quote Tool", layout="centered")

# Password protection
PASSWORD = "kittenpoodle"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Enter Password")
    pw = st.text_input("Password", type="password")
    if st.button("Submit"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Incorrect password")
    st.stop()

st.title("Insurance Quote Tool")

# Styling
st.markdown("""
    <style>
        .result-box {
            font-weight: bold;
            font-size: 1.2rem;
            margin-top: 20px;
        }
        .stButton>button {
            height: 3em;
            width: 6em;
            margin: 5px;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Constants for pricing
male_ia_prices = {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}}
female_ia_prices = {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}

male_tl_prices = {
    46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41,
    56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93
}

female_tl_prices = {
    46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35,
    56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67
}

male_sh_prices = {
    **{a: 9 for a in range(18, 41)}, **{41: 14, 42: 14, 43: 15, 44: 15, 45: 16},
    46: 17, 47: 18, 48: 19, 49: 20, 50: 21, 51: 26, 52: 26, 53: 28, 54: 29, 55: 30,
    56: 32, 57: 33, 58: 35, 59: 37, 60: 38, 61: 50, 62: 53, 63: 58, 64: 67
}

female_sh_prices = {
    18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16,
    27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21,
    36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25,
    46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44,
    56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62
}

final_expense_prices = {
    age: {"Male": male, "Female": female} for age, male, female in [
        (65, 80, 64), (66, 85, 68), (67, 89, 72), (68, 94, 76),
        (69, 99, 80), (70, 103, 84), (71, 110, 89), (72, 116, 95),
        (73, 123, 101), (74, 129, 107), (75, 136, 112), (76, 144, 120),
        (77, 152, 128), (78, 160, 137), (79, 168, 145), (80, 176, 153)
    ]
}

# Number input grid
st.markdown("### Enter Age")
age_input = st.text_input("", max_chars=2, key="age_input", label_visibility="collapsed")
if not age_input:
    age_input = ""

col1, col2, col3 = st.columns(3)
for row in [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]:
    cols = st.columns(len(row))
    for i, num in enumerate(row):
        if cols[i].button(str(num)):
            age_input += str(num)
            st.experimental_rerun()

# Clear Button
if st.button("Clear"):
    age_input = ""
    st.experimental_rerun()

# Gender Buttons and Calculation
def generate_quote(age, gender):
    age = int(age)
    if 18 <= age <= 45:
        plan = "IA"
        price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        return f"**{plan}${price} | SH${sh}\nBUNDLE${bundle}**"
    elif 46 <= age <= 64:
        plan = "TL"
        price = male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        return f"**{plan}${price} | SH${sh}\nBUNDLE${bundle}**"
    elif 65 <= age <= 80:
        fe_price = final_expense_prices[age][gender]
        return f"**FE${fe_price}**"
    else:
        return "**Invalid age**"

colM, colF = st.columns(2)
if colM.button("Male") and age_input.isdigit():
    st.markdown(generate_quote(age_input, "Male"), unsafe_allow_html=True)
if colF.button("Female") and age_input.isdigit():
    st.markdown(generate_quote(age_input, "Female"), unsafe_allow_html=True)
