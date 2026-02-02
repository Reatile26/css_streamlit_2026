# -*- coding: utf-8 -*-
"""

"""

import streamlit as st

st.write("Hello2")

st.title("Wie kan websites bou, ek kan! met STREAMLIT!")

st.write("Middag, Streamlit!")

st.header("Number selection")

number = st.slider("Pick a jou lekker lucky number", 1, 100)
st.write(f"You picked: {number}")