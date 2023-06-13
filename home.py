import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import timedelta
from datetime import datetime
import plotly.graph_objs as go
import random

st.set_page_config(page_title="Parametros", layout="wide")

@st.cache_data
def f0(d0, enam):
    d0 = pd.read_excel(d0)
    d0['empresa'] = enam
    return d0


garaycam = f0('parametros_garaycam.xlsm', 'garaycam')
marprima = f0('parametros_marprima.xlsm', 'marprima')
camaronera = pd.concat([garaycam,marprima])

empresa = st.sidebar.selectbox(
    "Filtrar por empresa",
    ("garaycam", "marprima", "total")
)



@st.cache_data
def f1(d0):
    d0 = d0[d0["oxigeno"]>0]
    d0 = d0[d0["fecha"]>=(max(d0["fecha"])-timedelta(days=120))]
    d0["horario"] = d0["horario"].str.lower()

    tdx = pd.to_timedelta(np.random.randint(2,4, size=len(d0)), unit='h')
    tdy = pd.to_timedelta(np.random.randint(0,59, size=len(d0)), unit='m')
    d0['fecha_hora']= pd.to_datetime(d0[['fecha','hora']].astype(str).agg(' '.join,1))-tdx-tdy
    d0['hora'] = pd.Series(d0['fecha_hora']).dt.hour
    d0['horario'] = np.where(d0['hora']<12,"madrugada", "tarde")
    return d0



if empresa == "garaycam":
    dw = camaronera[camaronera['empresa']=="garaycam"]
elif empresa =="marprima":
    dw = camaronera[camaronera['empresa']=="marprima"]
else:
    dw = camaronera

dx = f1(dw)
dx = dx[(dx['oxigeno']>0) & (dx['oxigeno']<20)]
dx = dx[['fecha','horario', 'oxigeno']].groupby(['fecha','horario']).agg({'oxigeno':['mean','std']}).reset_index()
dx.columns=['fecha', 'horario', 'ox_mean', 'ox_std']
dx['ox_max'] = round(dx['ox_mean']+(1.645*dx['ox_std']),3)
dx['ox_min'] = round(dx['ox_mean']-(1.645*dx['ox_std']),3)


dy = f1(dw)
dy = dy[(dy['temperatura']>10) & (dy['temperatura']<40)]
dy = dy[['fecha','horario', 'temperatura']].groupby(['fecha','horario']).agg({'temperatura':['mean','std']}).reset_index()
dy.columns=['fecha', 'horario', 't_mean', 't_std']
dy['t_max'] = round(dy['t_mean']+(1.645*dy['t_std']),3)
dy['t_min'] = round(dy['t_mean']-(1.645*dy['t_std']),3)


dz = f1(dw)
dz = dz[(dz['disco_secchi']>5) & (dz['disco_secchi']<80)]
dz = dz[['fecha','horario', 'disco_secchi']].groupby(['fecha','horario']).agg({'disco_secchi':['mean','std']}).reset_index()
dz.columns=['fecha', 'horario', 't_mean', 't_std']
dz['t_max'] = round(dy['t_mean']+(1.645*dz['t_std']),3)
dz['t_min'] = round(dy['t_mean']-(1.645*dz['t_std']),3)




col1, col2 = st.columns(2)

with col1:
    fig = px.line(dx,
                 y=['ox_min', 'ox_max'],
                 x= "fecha",
                 color="horario",
                 markers=False,
                 title="Oxigeno")

    st.plotly_chart(fig,theme="streamlit", use_container_width=True )
   

with col2:
   fig = px.line(dy,
                 y=['t_min', 't_max'],
                 x= "fecha",
                 color="horario",
                 markers=False,
                 title="Temperatura")
   st.plotly_chart(fig,theme="streamlit", use_container_width=True )


col3, col4 = st.columns(2)

with col3:
    fig = px.line(dz,
                 y=['t_min', 't_max'],
                 x= "fecha",
                 color="horario",
                 markers=False,
                 title="Turbidez")

    st.plotly_chart(fig,theme="streamlit", use_container_width=True )



go.Scatter()