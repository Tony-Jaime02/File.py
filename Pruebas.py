#pip install streamlit-card 
#IMPORTAR LIBRERIAS 

import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.plotting import figure
import plotly.graph_objects as go
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from PIL import Image
from datetime import datetime
from plotly.subplots import make_subplots

#LINEA DE DIVISION

text = '''

---

'''

#FECHA ACTUAL
fecha= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#mesAct = [int(fecha[0:4])]
#yearAct = [int(fecha[5:7])]

#LEER DATASET
dfTempXML = pd.read_csv('TEMPXMLFILEDATA.csv', encoding='utf8')
dfTempXML_filter = dfTempXML.loc[:, [
  'XMLFILEID', 'CUSTOMERID', 'TRANSACTIONID', 'INVOICETYPE', 'CREATEDTAXID',
  'PRODUCTDESC', 'VAT', 'VATAMT', 'TOTALBEFORTAX', 'TOTALAFTERTAX', 'FILETYPE',
  'DATE'
]]

dfCustomer=pd.read_csv('CUSTOMERMASTER.csv', encoding = 'latin_1')
dfCustomer_filter = dfCustomer.loc[:, ['CUSTOMERID', 'TAXID','FIRSTNAME', 'CITY', 'COMPANYNAME', 'COUNTRY', 'REGIME']]

dfTact = pd.read_csv('TRANSACTIONMASTER.csv', encoding='latin_1')
dfTact_filter = dfTact.loc[:,['TAXID', 'ACCOUNT', 'DESCRIPTION', 'TRANSACTIONDATETIME', 'DEBITAMOUNT', 'CREDITAMOUNT']]

filtro_rfc = st.sidebar.selectbox(
    'RFC',
    dfCustomer_filter[dfCustomer_filter['TAXID'].isin(dfTempXML_filter.groupby('CREATEDTAXID').count().reset_index()['CREATEDTAXID'].tolist())].groupby('TAXID').count().reset_index()['TAXID'].tolist()

)

if len(filtro_rfc)>0:
    dfTempXML_filter = dfTempXML_filter[dfTempXML_filter['CREATEDTAXID'] == filtro_rfc]
    dfCustomer_filter = dfCustomer_filter[dfCustomer_filter['TAXID'] == filtro_rfc]

    
    
#FECHAS    
dfTempXML_filter['MONTH'] = pd.DatetimeIndex(dfTempXML_filter['DATE']).month#12
dfTempXML_filter['YEAR'] = pd.DatetimeIndex(dfTempXML_filter['DATE']).year#2022
dfTempXML_filter['DAY'] = pd.DatetimeIndex(dfTempXML_filter['DATE']).day#01


dfTact_filter['YEAR'] = pd.DatetimeIndex(dfTact_filter['TRANSACTIONDATETIME']).year
dfTact_filter['MONTH'] = pd.DatetimeIndex(dfTact_filter['TRANSACTIONDATETIME']).month
dfTact_filter['DAY'] = pd.DatetimeIndex(dfTact_filter['TRANSACTIONDATETIME']).day


#Dataset nuevo
dfTempXML_2 = dfTempXML_filter
dfTempXML_3 = dfTempXML_filter

dfTact_1 = dfTact_filter
dfTact_2 = dfTact_filter



#Sidebar

#CENTRAR IMAGEN TONY
#image = Image.open('usericon.png')
#st.sidebar.markdown("# Home")
#st.sidebar.image(image, width = 200)

nombre = dfCustomer_filter['FIRSTNAME']
rfc = dfCustomer_filter['TAXID']

st.sidebar.markdown("<p style=font-size:20px;'text-align: center; font-weight: bold;font-family:Trebuchet MS>"+nombre.values[0]+"</p>", unsafe_allow_html=True)

st.sidebar.markdown("<p style=font-size:18px; font-weight: bold;font-family:Trebuchet MS;>"+rfc.values[0]+"</p>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:350%; color: #4973C9;'>Bienvenido/a a Contaayuda</h1>", unsafe_allow_html=True)

st.markdown(text)

st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:180%; color: #000000;'>El mejor lugar para consultar tu información financiera</h1>", unsafe_allow_html=True)

#FILTROS
filtro_year = st.sidebar.multiselect(
    '🔸FILTRO DE AÑO',
    dfTempXML_filter.groupby('YEAR').count().reset_index()['YEAR'].tolist(),
    default=dfTempXML_filter.groupby('YEAR').count().reset_index()['YEAR'].tolist()[0]
)
        
filtro_month = st.sidebar.multiselect(
    '🔸FILTRO DE MES',
    dfTempXML_filter[dfTempXML_filter['YEAR'].isin(filtro_year)].groupby('MONTH').count().reset_index()['MONTH'].tolist(),
)

filtro_fact = st.sidebar.multiselect(
    '🔸TIPOS DE FACTURAS',
    dfTempXML_filter[dfTempXML_filter['YEAR'].isin(filtro_year) & dfTempXML_filter['MONTH'].isin(filtro_month)].groupby('INVOICETYPE').count().reset_index()['INVOICETYPE'].tolist()
)

#Aplicacion de filtros
if len(filtro_year)>0:
    dfTempXML_filter = dfTempXML_filter[dfTempXML_filter['YEAR'].isin(filtro_year)]

if len(filtro_month)>0:
    dfTempXML_filter = dfTempXML_filter[dfTempXML_filter['MONTH'].isin(filtro_month)]

if len(filtro_fact)>0:
    dfTempXML_filter = dfTempXML_filter[dfTempXML_filter['INVOICETYPE'].isin(filtro_fact)]

#DEBUGGEO
#st.dataframe(dfTempXML_filter)
#st.dataframe(dfCustomer_filter)

#INCOME PER YEAR
income = dfTempXML_2[dfTempXML_2['YEAR'].isin(filtro_year)]
income2 = income[income['INVOICETYPE'] == 'ingreso']['TOTALAFTERTAX'].sum()

#INCOME PER MONTH AND YEAR
incomeMonth = dfTempXML_2[dfTempXML_2['INVOICETYPE'] == 'ingreso']
incomeMonth2 = incomeMonth[incomeMonth['YEAR'].isin(filtro_year)]
incomeMonth3 = incomeMonth2[incomeMonth2['MONTH'].isin(filtro_month)]['TOTALAFTERTAX'].sum()

#VAT PAID PER YEAR
paid = dfTempXML_2[dfTempXML_2['YEAR'].isin(filtro_year)]
paid2 = paid[paid['INVOICETYPE'] == 'egreso']['TOTALAFTERTAX'].sum()

dfyear = dfTempXML_2[dfTempXML_2['YEAR'].isin(filtro_year)]
dfmonth = dfyear[dfyear['MONTH'].isin(filtro_month)]

#INGRESOS Y EGRESOS ANUALES
ingreso = dfyear[dfyear['INVOICETYPE'] == 'ingreso']
egreso = dfyear[dfyear['INVOICETYPE'] == 'egreso']

#INGRESOS Y EGRESOS MENSUALES
ingreso_month = dfmonth[dfmonth['INVOICETYPE'] == 'ingreso']
egreso_month = dfmonth[dfmonth['INVOICETYPE'] == 'egreso']


#GRAFICAS

#PIE TIPOS DE FACTURAS
dfPIE_FACTS = dfTempXML_filter.groupby('INVOICETYPE')['CREATEDTAXID'].count()
fig = px.pie(dfPIE_FACTS, values='CREATEDTAXID', names=dfPIE_FACTS.index, color_discrete_sequence = ['#1A2447','#4973C9','#CFDCFF','#FEFEFE'])

#BARRAS INGRESOS Y EGRESOS

#INGRESOS Y EGRESOS ANUALES
fig2 = go.Figure()

fig2.add_trace(
    go.Bar(
        name = 'Ingresos anuales',
        x=ingreso['MONTH'],
        y=ingreso['TOTALAFTERTAX']
    )
)

fig2.add_trace(
    go.Bar(
        name = 'Egresos anuales',
        x=egreso['MONTH'],
        y=egreso['TOTALAFTERTAX']
    )
)
#INGRESOS Y EGRESOS ANUALES
fig2.update_layout(
    xaxis_title = "Mes",
    yaxis_title = "Total"
)

#INGRESOS Y EGRESOS MENSUALES
fig3 = go.Figure()

fig3.add_trace(
    go.Bar(
        name = 'Ingresos del mes',
        x=ingreso_month['DAY'],
        y=ingreso_month['TOTALAFTERTAX']
    )
)

fig3.add_trace(
    go.Bar(
        name = 'Egresos del mes',
        x=egreso_month['DAY'],
        y=egreso_month['TOTALAFTERTAX']
    )
)

fig3.update_layout(
    xaxis_title = "Dia",
    yaxis_title = "Total"
)

#RESUMEN DE FINANZAS filtradas
st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:200%; color: #4973C9;'>◽Resumen de finanzas</h1>", unsafe_allow_html=True)

col1F, col2F, col3F = st.columns(3)
with col1F:
    st.write("<h4 style='text-align: center; color: #00000;'>Ingreso anual</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #4973C9;'>$"+str(income2.round(2))+" MXN</h1>", unsafe_allow_html=True)

with col2F:
    st.write("<h4 style='text-align: center; color: #00000;'>Ingreso mensual</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #4973C9;'>$"+str(incomeMonth3.round(2))+" MXN</h1>", unsafe_allow_html=True)

with col3F:
    st.write("<h4 style='text-align: center; color: #00000;'>Impuestos anuales</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #4973C9;'>$"+str(paid2.round(2))+" MXN</h1>", unsafe_allow_html=True)

st.markdown(text)

st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:200%; color: #4973C9;'>◽Gráficos</h1>", unsafe_allow_html=True)

#IMPUESTOS dfTempXML_3
#st.dataframe(dfTempXML_3)
dfTempXML_3 = dfTempXML_3[(dfTempXML_3['VAT'] == 'IVA')]
#st.dataframe(dfTempXML_3)

dfTotal = dfTempXML_3[(dfTempXML_3['VAT'] == 'IVA')].pivot_table(
    index=['CREATEDTAXID'],
    columns=['YEAR', 'MONTH'],
    values='VATAMT',
    aggfunc=np.sum,
    dropna=False
)

dfTotalYear = dfTempXML_3[(dfTempXML_3['VAT'] == 'IVA') & dfTempXML_3['YEAR'].isin(filtro_year)].pivot_table(
    index=['CREATEDTAXID'],
    columns=['YEAR', 'MONTH'],
    values='VATAMT',
    aggfunc=np.sum,
    dropna=False
)

dfTotal = dfTotal.fillna(0)
dfTotalYear = dfTotalYear.fillna(0)

acum = 0
X = []
y = []
Xacum = []
mes = 0

acumT = 0
XT = []
yT = []
XacumT = []
mesT = 0


for i in(dfTotal.columns):  
    acumT += dfTotal[i]
    nowT = dfTotal[i]
    mesT += 1
    XacumT.append(acumT[filtro_rfc])
    XT.append(nowT[filtro_rfc])
    yT.append(mesT)

for i in(dfTotalYear.columns):  
    acum += dfTotalYear[i]
    now = dfTotalYear[i]
    mes += 1
    Xacum.append(acum[filtro_rfc])
    X.append(now[filtro_rfc])
    y.append(mes)
   

fig4 = make_subplots(rows=1, cols=2, start_cell="bottom-left")
fig4.add_trace(go.Scatter(x=yT, y=XT, name='IVA total', line=dict(color='blue', width=4)), row=1, col=1)
fig4.add_trace(go.Scatter(x=yT, y=XacumT, name='Impuestos totales', line=dict(color='red', width=4)), row=1, col=2)
fig4.update_layout(xaxis_title='Meses', yaxis_title='Impuestos')

fig5 = make_subplots(rows=1, cols=2, start_cell="bottom-left")
fig5.add_trace(go.Scatter(x=y, y=X, name='IVA mensual', line=dict(color='blue', width=4)), row=1, col=1)
fig5.add_trace(go.Scatter(x=y, y=Xacum, name='Impuestos totales', line=dict(color='red', width=4)), row=1, col=2)
fig5.update_layout(xaxis_title='Meses', yaxis_title='Impuesto IVA', width=1100, height=900) 

#TABS
tab1, tab2= st.tabs(["Facturas", "Impuestos"])

with tab1:
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>Facturas💲</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=False)
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>Ingresos y egresos anuales</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=False)
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>Ingresos y egresos mensuales</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=False)

with tab2:
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>Impuestos IVA pagados</h1>", unsafe_allow_html=True)
    st.dataframe(dfTotal)
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>Impuestos totales</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig4)
    st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:150%; color: #000000;'>IVA Anual</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=False)

    
st.markdown(text)

#FINANZAS ACUMULADAS

dfTact_12 = dfTact_1[dfTact_1['YEAR'].isin(filtro_year)]

data5 = dfTact_12.groupby('MONTH')[['DEBITAMOUNT','CREDITAMOUNT']].sum()
fig6= go.Figure()
fig6=fig6.add_trace(go.Line(x=data5.index, y=data5['DEBITAMOUNT'],name="Egresos")) # fill down to xaxis
fig6=fig6.add_trace(go.Line(x=data5.index, y=data5['CREDITAMOUNT'],name="Ingresos")) # fill to trace0 y
fig6=fig6.update_layout(xaxis_title="Meses", yaxis_title="Total",)

#FINANZAS ACUMULADAS
st.write("<h1 style='text-align: left;font-family:Trebuchet MS;font-size:200%; color: #4973C9;'>◽Finanzas acumuladas</h1>", unsafe_allow_html=True)

st.write("<h3 style='text-align: left; color: #FEFEFE;font-size:150%; color: #000000;'>Credito y debito anual</h1>", unsafe_allow_html=True)
st.plotly_chart(fig6)
st.write("<h3 style='text-align: left; color: #FEFEFE;font-size:150%; color: #000000;'>Transacciones realizadas durante el año</h1>", unsafe_allow_html=True)
st.write(dfTact_12[['ACCOUNT', 'DESCRIPTION', 'TRANSACTIONDATETIME']])