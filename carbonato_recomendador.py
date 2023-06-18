import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Parametros", layout="wide")

salinidad = st.sidebar.number_input('Salinidad: ', min_value = 0, 
                                    max_value= 40, value = 20)

recambio = st.sidebar.number_input('% Recambio diario: ', min_value = 0, 
                                    max_value= 100, value =10)

alcalinidad = st.sidebar.number_input('Alcalinidad: ', min_value = 0, 
                                    max_value= 500, value=100)




