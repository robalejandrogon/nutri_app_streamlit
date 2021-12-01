'''
Project for Nutri Eat
v.12

Developed by R.Gonzalez
'''

import base64
import datetime
from datetime import timedelta
from datetime import date
from github import Github
import io
from io import BytesIO
from logging import PlaceHolder
import mysql.connector
import numpy as np
import os
import pandas as pd
from pandas.core.frame import DataFrame
from PIL import Image
import requests
import SessionState
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from urllib.request import urlopen

@st.cache
def get_data_structure():
    url_structure = "https://raw.githubusercontent.com/robalejandrogon/files/main/estructura.csv"
    download_structure = requests.get(url_structure).content
    df_structure = pd.read_csv(io.StringIO(download_structure.decode('utf-8')))

    url_structure2 = "https://raw.githubusercontent.com/robalejandrogon/files/main/estructura_v2.csv"
    download_structure2 = requests.get(url_structure2).content
    df_structure2 = pd.read_csv(io.StringIO(download_structure2.decode('utf-8')))

    url_ruta = "https://raw.githubusercontent.com/robalejandrogon/files/main/rutas.csv"
    download_ruta = requests.get(url_ruta).content
    df_ruta = pd.read_csv(io.StringIO(download_ruta.decode('utf-8')))

    return df_structure2,df_ruta

@st.cache
def get_picture():
    response = requests.get("https://raw.githubusercontent.com/robalejandrogon/nutri_app_streamlit/main/image_1.png")
    return response

@st.cache()
def get_customer():
    mydb = mysql.connector.connect(
        host="sql555.main-hosting.eu ",
        user="u591727659_robalejandro",
        password="RobalejandroTest1234",
        database="u591727659_test")
    sql="""SELECT cliente FROM clientes"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    clients_list = [x[0] for x in myresult]
    df_customer2 = pd.DataFrame(clients_list,columns=['NOMBRE'])
    mydb.close()
    return df_customer2

@st.cache()
def get_cost():
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql2="""SELECT pedido,costo FROM costos"""

    mycursor3 = mydb.cursor()
    mycursor3.execute(sql2)
    myresult2 = mycursor3.fetchall()
    df_costos = pd.DataFrame(myresult2,columns=['Pedido','Costo'])
    mycursor3.close()
    mydb.close()
    return df_costos

def insert_customer(new_customer):
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql_new_customer = '''INSERT INTO clientes (cliente) VALUES (%s)'''
    values=(new_customer,)
    mycursor2 = mydb.cursor(prepared=True)
    mycursor2.execute(sql_new_customer,values)
    mydb.commit()
    mycursor2.close()
    mydb.close()
    st.session_state['clientes'].append(new_customer)
    st.success('Nuevo Cliente agregado')

def insert_new_pedido(new_pedido,precio_new_pedido):
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql_new_pedido = '''INSERT INTO costos (pedido,costo) VALUES (%s,%s)'''
    values=(new_pedido,int(precio_new_pedido))
    mycursor4 = mydb.cursor(prepared=True)
    mycursor4.execute(sql_new_pedido,values)
    mydb.commit()
    mycursor4.close()
    mydb.close()
    st.session_state['pedidos'].append(new_pedido)
    st.success('Nuevo pedido agregado')

def insert_gramaje(gramaje_pedido):
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql_gramaje = '''INSERT INTO gramaje (gramaje) VALUES (%s)'''
    values=(gramaje_pedido,)
    mycursor2 = mydb.cursor(prepared=True)
    mycursor2.execute(sql_gramaje,values)
    mydb.commit()
    mycursor2.close()
    mydb.close()

def reinicio():
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql = """UPDATE pedidos_v3 SET 
            platillos_pollo_normal= 0,
            platillos_pollo_sin_sal= 0,
            pescado_sin_sal= 0,
            pescado_normal= 0,
            salmon_sin_sal= 0,
            salmon_normal= 0,
            camarones_sin_sal= 0,
            camarones_normal= 0,
            atun_sin_sal= 0,
            atun_normal= 0,
            e_buffalo= 0,
            e_carnes_frias= 0,
            d_liz= 0,
            e_cesar= 0,
            h_normal= 0,
            h_chilaca= 0,
            h_champ= 0,
            h_haw= 0,
            h_normal_pan_thin=0,
            h_normal_pan_margarita=0,
            h_normal_pan_lechuga=0,
            h_chilaca_pan_thin=0,
            h_chilaca_pan_margarita=0,
            h_chilaca_pan_lechuga=0,
            h_champ_pan_thin=0,
            h_champ_pan_margarita=0,
            h_champ_pan_lechuga=0,
            h_haw_pan_thin=0,
            h_haw_pan_margarita=0,
            h_haw_pan_lechuga=0,
            e_buffalo_alitas=0,
            e_buffalo_buffalo=0,
            e_buffalo_mostaza=0,
            e_buffalo_limon_pepper=0,
            e_buffalo_natural=0,
            e_buffalo_bbqs=0,
            e_carnes_frias_alitas=0,
            e_carnes_frias_buffalo=0,
            e_carnes_frias_mostaza=0,
            e_carnes_frias_limon_pepper=0,
            e_carnes_frias_natural=0,
            e_carnes_frias_bbqs=0,
            e_dliz_alitas=0,
            e_dliz_buffalo=0,
            e_dliz_mostaza=0,
            e_dliz_limon_pepper=0,
            e_dliz_natural=0,
            e_dliz_bbqs=0,
            e_cesar_alitas=0,
            e_cesar_buffalo=0,
            e_cesar_mostaza=0,
            e_cesar_limon_pepper=0,
            e_cesar_natural=0,
            e_cesar_bbqs=0,
            desayuno= 0,
            snack= 0,
            merienda= 0,
            cena= 0,
            ensaladas= 0,
            hamburguesas= 0,
            platillos_normales= 0,
            platillos_sin_sal= 0,
            platillos_totales= 0,
            Panini_carnes_frias=0,
            Panini_pollo=0
            WHERE id_pedido= 0"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

def truncate_gramaje():
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    mycursor2= mydb.cursor()
    mycursor2.execute("TRUNCATE TABLE gramaje")
    mycursor2.close()
    mydb.commit()
    mydb.close()

#Reading customers from db

df_costos = get_cost()
df_customer2 = get_customer()
if 'pedidos' not in st.session_state:
    #st.session_state['pedidos']=['Pollo','Pescado','Salmón','Camarones','E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw','Atun']
    st.session_state['pedidos']=df_costos['Pedido'].tolist()
if 'variacion' not in st.session_state:
    st.session_state['variacion']=['Sin carbo','Colitis','Sin sal', 'Sin chile','Pan margarita','Lechuga','Pan thin','Alitas','Buffalo','Mostaza','Limón pepper','Natural','BBQs','Otro * especificar','-']
if 'clientes' not in st.session_state:
    st.session_state['clientes'] = df_customer2['NOMBRE'].tolist()
if 'placeholder' not in st.session_state:
    st.session_state['placeholder'] = '-'

#session_state = SessionState.get(df=df_structure)
df_structure2,df_ruta =  get_data_structure()
session_state = SessionState.get(df=df_structure2)
session_state.df['Ruta'] = pd.Categorical(session_state.df['Ruta'], ['R1A','R1C','R2A','R2C','R1V','R2V','LOCAL','-'])
#customers = df_customer['NOMBRE '].tolist()

#variacion
#variacion= ['Sin carbo','Colitis','Sin sal', 'Sin chile','Otro * especificar']
#https://srv555.main-hosting.eu:7443/files/public_html/bell.wav
#ruta
ruta = ['R1A','R1C','R1V','R2A','R2C','R2V','LOCAL','-']

#pedidos
#pedidos=['Pollo','Pescado','Salmón','Camarones','E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw']

#session_state = SessionState.get(df=df_structure)

st.title('Nutri Eat')
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#'''response = requests.get("https://raw.githubusercontent.com/robalejandrogon/nutri_app_streamlit/main/image_1.png")'''
response = get_picture()
img = Image.open(BytesIO(response.content))

today = date.today()

#Description
#st.markdown("""
#Aplicación para gestión de ordenes y pedidos.
#""")

#Side header
st.sidebar.markdown(today)
st.sidebar.image(img)
#-----------------------------------------------------------------------------------------
my_form = st.sidebar.form(key = "form1")
my_form.header('Cliente', anchor=None)
new_cliente_fill = '-'
new_customer = my_form.text_input('Nuevo cliente', st.session_state['placeholder'] )
submitted0 = my_form.form_submit_button('Agregar nuevo cliente .')
#INSERT INTO clientes (cliente) VALUES ('Hola')
if submitted0:
    if new_customer == '-':
        st.warning('Cliente no valido')
    else:
        insert_customer(new_customer)
        
default_ix = st.session_state['clientes'].index('-')
selected_customer = my_form.selectbox('Nombre:',st.session_state['clientes'],index=default_ix)
my_form.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------

#my_form2 = st.sidebar.form(key="form2")
my_form.header('Pedido', anchor=None)
new_pedido_fill='-'
new_pedido = my_form.text_input('Nuevo pedido', new_pedido_fill)
precio_new_pedido = my_form.text_input('Precio nuevo pedido', new_pedido_fill)
submitted1 = my_form.form_submit_button('Agregar nuevo pedido sencillo.')
if submitted1:
    if new_pedido=='-':
        st.warning('Pedido no valido')
    else:
        insert_new_pedido(new_pedido,precio_new_pedido)

default_ix_pedido = st.session_state['pedidos'].index('-')
selected_pedido = my_form.selectbox('Pedido:',st.session_state['pedidos'],index=default_ix_pedido)
cantidad_pedido = my_form.number_input('Cantidad',min_value=1)
pedido_gramaje_fill='-'
gramaje_pedido = my_form.text_input('Pedido específico con gramaje', pedido_gramaje_fill)
gramaje_pedido_costo = my_form.text_input('Costo pedido especifico/gramaje', pedido_gramaje_fill)
my_form.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------

#my_form3 = st.sidebar.form(key="form3")
my_form.header('Variación', anchor=None)
variacion_fill='-'
new_variacion = my_form.text_input('Nuevo variacion', variacion_fill)
submitted2 = my_form.form_submit_button('Agregar nueva variacion.')
if submitted2:
    if new_variacion=='-':
        st.warning('Variación no valida')
    else:
        st.session_state['variacion'].append(new_variacion)
        st.success('Nueva variación agregado')

default_ix_variacion= st.session_state['variacion'].index('-')
selected_variacion= my_form.selectbox('Variación',st.session_state['variacion'],index=default_ix_variacion)
my_form.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------

#my_form4 = st.sidebar.form(key="form4")
my_form.header('Ruta', anchor=None)
default_ix_ruta = ruta.index('-')
selected_ruta = my_form.selectbox('Ruta:',ruta,index=default_ix_ruta)
my_form.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
my_form.header('Tiempos', anchor=None)
desayuno = my_form.number_input('Desayuno',0)
snack = my_form.number_input('Snack',0)
merienda = my_form.number_input('Merienda', 0)
cena = my_form.number_input('Cena', 0)
my_form.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------

my_form.header('Acciones', anchor=None)
submitted3 = my_form.form_submit_button('Agregar')
id_a_editar = my_form.text_input('id del regitro a editar', '-')
submitted4 = my_form.form_submit_button('Editar')
id_a_eliminar = my_form.text_input('id del regitro a eliminar', '-')
submitted52 = my_form.form_submit_button('Eliminar')
submitted_ruta = my_form.form_submit_button('Ordenar por ruta')
submitted_reinicio = my_form.form_submit_button('reiniciar')

#-----------------------------------------------------------------------------------------

def add_new_customer():
    y=pd.DataFrame({'Cliente':[selected_customer],
                    'Pedido':[selected_pedido],
                    'Cantidad':[cantidad_pedido],
                    'Pedido específico':[gramaje_pedido],
                    'Costo pedido específico':[gramaje_pedido_costo],
                    'Variación':[selected_variacion],
                    'Ruta':[selected_ruta],
                    'Desayuno':[int(desayuno)],
                    'Snack':[int(snack)],
                    'Merienda':[int(merienda)],
                    'Cena':[int(cena)]})
    session_state.df = session_state.df.append(y,ignore_index=True)
    if (gramaje_pedido != '') and (gramaje_pedido !='-'):
        insert_gramaje(gramaje_pedido)
    st.success('Cliente agregado')
#-----------------------------------------------------------------------------------------

if submitted3:
    #y=pd.DataFrame({'Cliente':[selected_customer],
    #                'Pedido':[selected_pedido],
    #                'Variación':[selected_variacion],
    #                'Ruta':[selected_ruta],
    #                'Desayuno':[int(desayuno)],
    #                'Snack':[int(snack)],
    #                'Merienda':[int(merienda)],
    #                'Cena':[int(cena)]})
    #session_state.df = session_state.df.append(y,ignore_index=True)
    #if selected_customer in session_state.df.Cliente.tolist():
    #    st.warning('Cliente ya registrado')
    #else:
    if selected_customer == '-':
        st.warning('Cliente vacio')
    else:
        add_new_customer()

#-----------------------------------------------------------------------------------------

if submitted4:
    if id_a_editar != '-':
        if int(id_a_editar) in session_state.df.index:
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Pedido'] = selected_pedido
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Cantidad'] = cantidad_pedido
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Gramaje'] = gramaje_pedido
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Variación'] = selected_variacion
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Ruta'] = selected_ruta
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Desayuno'] = desayuno
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Snack'] = snack
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Merienda'] = merienda
            #session_state.df.loc[session_state.df['Cliente']==selected_customer,'Cena'] = cena

            session_state.df.loc[int(id_a_editar),'Pedido'] = selected_pedido
            session_state.df.loc[int(id_a_editar),'Cantidad'] = cantidad_pedido
            session_state.df.loc[int(id_a_editar),'Pedido específico'] = gramaje_pedido
            session_state.df.loc[int(id_a_editar),'Costo pedido específico'] = gramaje_pedido_costo
            session_state.df.loc[int(id_a_editar),'Variación'] = selected_variacion
            session_state.df.loc[int(id_a_editar),'Ruta'] = selected_ruta
            session_state.df.loc[int(id_a_editar),'Desayuno'] = desayuno
            session_state.df.loc[int(id_a_editar),'Snack'] = snack
            session_state.df.loc[int(id_a_editar),'Merienda'] = merienda
            session_state.df.loc[int(id_a_editar),'Cena'] = cena
            st.success('Cliente actualizado')
    else:
        st.success('id no válido')
#-----------------------------------------------------------------------------------------

if submitted52:
    if int(id_a_eliminar) in session_state.df.index:
        i = session_state.df.loc[session_state.df['Cliente']==selected_customer,:].index
        #session_state.df.drop(i,inplace=True)
        session_state.df.drop(int(id_a_eliminar),inplace=True)
        session_state.df.reset_index(inplace=True)
        session_state.df.drop('index',axis=1,inplace=True)
        st.success('Cliente eliminado')
    else:
        st.warning('Cliente no registrado')
#-----------------------------------------------------------------------------------------

if submitted_reinicio:
    reinicio()
    if len(session_state.df) > 0:
        truncate_gramaje()
        session_state.df = session_state.df.truncate(after=-1)
    session_state = SessionState.get(df=df_structure2)
    st.success('Pedidos reseteados')
#-----------------------------------------------------------------------------------------

if submitted_ruta:
    #['R1A','R1C','R1V','R2A','R2C','R2V','LOCAL']
    session_state.df['Ruta'] = pd.Categorical(session_state.df['Ruta'], ['R1A','R1C','R1V','R2A','R2C','R2V','LOCAL'])
    session_state.df = session_state.df.sort_values('Ruta')

#-----------------------------------------------------------------------------------------

st.dataframe(session_state.df,width=1500,height=400)

#st.table(session_state.df)
file = st.file_uploader("Subir reportes para generar reporte semanal", type=['csv'],accept_multiple_files=True)
if not file:
    st.write("-")

#-----------------------------------------------------------------------------------------

st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
#with st.container():
col6,col7=st.columns(2)
check_customer = col6.selectbox('Nombre:',session_state.df.Cliente.unique())
PlaceHolder2 = col7.write('')
PlaceHolder3 = col7.write('')
check_flag = col7.checkbox("Ok",False)
button_ckeck = col6.button('Guardar')
if button_ckeck:
    if check_flag:
        if check_customer in session_state.df['Cliente'].tolist():
            session_state.df.loc[session_state.df['Cliente'].str.contains(check_customer),'Check']= 'Ok'
            #count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

#-----------------------------------------------------------------------------------------

st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
with st.container():
    col1,col2,col3,col4,col5= st.columns(5)
    submitted4 = col1.button('Gráfica')
    submitted5 = col2.button('Actualizar')
    submitted6 = col3.button('Reporte diario')
    submitted7 = col4.button('Reporte semanal')
    #submitted8 = col5.button('Ordenar por ruta')



#if submitted8:
#    #ruta = ['R1A','R1C','R1V','R2A','R2C','R2V']
#    session_state.df['Ruta'] = pd.Categorical(session_state.df['Ruta'], ['R1A','R1C','R2A','R2C','R1V','R2V'])
#    session_state.df.sort_values('Ruta',inplace=True)
#-----------------------------------------------------------------------------------------

#if submitted4:
#    st.bar_chart(session_state.df['Pedido'].value_counts())

#-----------------------------------------------------------------------------------------

if submitted5:
    platillos_pollo_normal = session_state.df.loc[(session_state.df.Pedido=='Pollo') & (session_state.df['Variación']!='Sin sal'),
                                                      'Cantidad'].sum()
    platillos_pollo_sin_sal = session_state.df.loc[(session_state.df.Pedido=='Pollo') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Cantidad'].sum()
    pescado_sin_sal = session_state.df.loc[(session_state.df.Pedido=='Pescado') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Cantidad'].sum()
    pescado_normal = session_state.df.loc[(session_state.df.Pedido=='Pescado') & 
                                                  (
                                                      (session_state.df['Variación']!='Sin sal') 
                                                      ),
                                                      'Cantidad'].sum()
    salmon_sin_sal = session_state.df.loc[(session_state.df.Pedido=='Salmón') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Cantidad'].sum()
    salmon_normal = session_state.df.loc[(session_state.df.Pedido=='Salmón') & 
                                                  (
                                                      (session_state.df['Variación']!='Sin sal') 
                                                      ),
                                                      'Cantidad'].sum()
    camarones_sin_sal = session_state.df.loc[(session_state.df.Pedido=='Camarones') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Cantidad'].sum()

    camarones_normal = session_state.df.loc[(session_state.df.Pedido=='Camarones') & 
                                                  (
                                                      (session_state.df['Variación']!='Sin sal') 
                                                      ),
                                                      'Cantidad'].sum()
    
    atun_sin_sal = session_state.df.loc[(session_state.df.Pedido=='Atun') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Cantidad'].sum()

    atun_normal = session_state.df.loc[(session_state.df.Pedido=='Atun') & 
                                                  (
                                                      (session_state.df['Variación']!='Sin sal') 
                                                      ),
                                                      'Cantidad'].sum()
    #'E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw'
    e_buffalo = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo'),
                                                      'Cantidad'].sum()
    e_carnes_frias = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias'),
                                                      'Cantidad'].sum()
    d_liz = session_state.df.loc[(session_state.df.Pedido=='E. Dliz'),
                                                      'Cantidad'].sum()
    e_cesar = session_state.df.loc[(session_state.df.Pedido=='E. Cesar'),
                                                      'Cantidad'].sum()

    h_normal = session_state.df.loc[(session_state.df.Pedido=='Hamb Norma'),
                                                      'Cantidad'].sum()
    h_chilaca = session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca'),
                                                      'Cantidad'].sum()
    h_champ = session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca'),
                                                      'Cantidad'].sum()
    h_haw = session_state.df.loc[(session_state.df.Pedido=='Hamb Haw'),
                                                      'Cantidad'].sum()
    #'Pan margarita','Lechuga','Pan thin'
    h_normal_pan_thin = session_state.df.loc[(session_state.df.Pedido=='Hamb Norma') & (session_state.df['Variación']=='Pan thin') ,
                                                      'Cantidad'].sum()
    h_normal_pan_margarita = session_state.df.loc[(session_state.df.Pedido=='Hamb Norma') & (session_state.df['Variación']=='Pan margarita') ,
                                                      'Cantidad'].sum()  
    h_normal_pan_lechuga = session_state.df.loc[(session_state.df.Pedido=='Hamb Norma') & (session_state.df['Variación']=='Lechuga') ,
                                                      'Cantidad'].sum()
    h_chilaca_pan_thin = session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca') & (session_state.df['Variación']=='Pan thin') ,
                                                      'Cantidad'].sum()
    h_chilaca_pan_margarita = session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca') & (session_state.df['Variación']=='Pan margarita') ,
                                                      'Cantidad'].sum()  
    h_chilaca_pan_lechuga = session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca') & (session_state.df['Variación']=='Lechuga') ,
                                                      'Cantidad'].sum()
    h_champ_pan_thin = session_state.df.loc[(session_state.df.Pedido=='Hamb Champiñones') & (session_state.df['Variación']=='Pan thin') ,
                                                      'Cantidad'].sum()
    h_champ_pan_margarita = session_state.df.loc[(session_state.df.Pedido=='Hamb Champiñones') & (session_state.df['Variación']=='Pan margarita') ,
                                                      'Cantidad'].sum()  
    h_champ_pan_lechuga = session_state.df.loc[(session_state.df.Pedido=='Hamb Champiñones') & (session_state.df['Variación']=='Lechuga') ,
                                                      'Cantidad'].sum()
    h_haw_pan_thin = session_state.df.loc[(session_state.df.Pedido=='Hamb Haw') & (session_state.df['Variación']=='Pan thin') ,
                                                      'Cantidad'].sum()
    h_haw_pan_margarita = session_state.df.loc[(session_state.df.Pedido=='Hamb Haw') & (session_state.df['Variación']=='Pan margarita') ,
                                                      'Cantidad'].sum()  
    h_haw_pan_lechuga = session_state.df.loc[(session_state.df.Pedido=='Hamb Haw') & (session_state.df['Variación']=='Lechuga') ,
                                                      'Cantidad'].sum() 
    #'Alitas','Buffalo','Mostaza','Limón pepper','Natural','BBQs'
    #-----------------------------------------------------------------------
    e_buffalo_alitas = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='Alitas'),
                                                      'Cantidad'].sum()
    e_buffalo_buffalo = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='Buffalo'),
                                                      'Cantidad'].sum()
    e_buffalo_mostaza = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='Mostaza'),
                                                      'Cantidad'].sum()
    e_buffalo_limon_pepper = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='Limón pepper'),
                                                      'Cantidad'].sum()
    e_buffalo_natural = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='Natural'),
                                                      'Cantidad'].sum()
    e_buffalo_bbqs = session_state.df.loc[(session_state.df.Pedido=='E.Buffalo') & (session_state.df['Variación']=='BBQs'),
                                                      'Cantidad'].sum()
    #-----------------------------------------------------------------------
    e_carnes_frias_alitas = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='Alitas'),
                                                      'Cantidad'].sum()
    e_carnes_frias_buffalo = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='Buffalo'),
                                                      'Cantidad'].sum()
    e_carnes_frias_mostaza = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='Mostaza'),
                                                      'Cantidad'].sum()
    e_carnes_frias_limon_pepper = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='Limón pepper'),
                                                      'Cantidad'].sum()
    e_carnes_frias_natural = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='Natural'),
                                                      'Cantidad'].sum()
    e_carnes_frias_bbqs = session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias') & (session_state.df['Variación']=='BBQs'),
                                                      'Cantidad'].sum()
    #-----------------------------------------------------------------------
    e_dliz_alitas = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='Alitas'),
                                                      'Cantidad'].sum()
    e_dliz_buffalo = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='Buffalo'),
                                                      'Cantidad'].sum()
    e_dliz_mostaza = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='Mostaza'),
                                                      'Cantidad'].sum()
    e_dliz_limon_pepper = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='Limón pepper'),
                                                      'Cantidad'].sum()
    e_dliz_natural = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='Natural'),
                                                      'Cantidad'].sum()
    e_dliz_bbqs = session_state.df.loc[(session_state.df.Pedido=='E. Dliz') & (session_state.df['Variación']=='BBQs'),
                                                      'Cantidad'].sum()
    #-----------------------------------------------------------------------
    e_cesar_alitas = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='Alitas'),
                                                      'Cantidad'].sum()
    e_cesar_buffalo = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='Buffalo'),
                                                      'Cantidad'].sum()
    e_cesar_mostaza = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='Mostaza'),
                                                      'Cantidad'].sum()
    e_cesar_limon_pepper = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='Limón pepper'),
                                                      'Cantidad'].sum()
    e_cesar_natural = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='Natural'),
                                                      'Cantidad'].sum()
    e_cesar_bbqs = session_state.df.loc[(session_state.df.Pedido=='E. Cesar') & (session_state.df['Variación']=='BBQs'),                                                'Cantidad'].sum()
    #-----------------------------------------------------------------------
    desayuno = session_state.df['Desayuno'].sum()

    snack= session_state.df['Snack'].sum()

    merienda= session_state.df['Merienda'].sum()

    cena= session_state.df['Cena'].sum()
    #-----------------------------------------------------------------------
    panini_carnes_frias = session_state.df.loc[(session_state.df.Pedido=='Panini carnes frias'),
                                                      'Cantidad'].sum()
    panini_pollo= session_state.df.loc[(session_state.df.Pedido=='Panini pollo'),
                                                      'Cantidad'].sum()                                                  
    #-----------------------------------------------------------------------
    ensaladas = e_buffalo  + e_carnes_frias + d_liz + e_cesar 
    platillos_normales = platillos_pollo_normal + pescado_normal + salmon_normal  + camarones_normal  + atun_normal
    platillos_sin_sal = platillos_pollo_sin_sal + pescado_sin_sal + salmon_sin_sal + camarones_sin_sal + atun_sin_sal 
    hamburguesas = h_normal + h_chilaca + h_champ + h_haw
    platillos_totales = desayuno + snack+ merienda+ cena+ platillos_pollo_normal + platillos_pollo_sin_sal + pescado_sin_sal + pescado_normal + salmon_sin_sal + salmon_normal + camarones_sin_sal + camarones_normal + atun_sin_sal + atun_normal +e_buffalo +e_carnes_frias + d_liz + e_cesar + h_normal + h_chilaca + h_champ + h_haw+panini_carnes_frias+panini_pollo
    mydb = mysql.connector.connect(
    host="sql555.main-hosting.eu ",
    user="u591727659_robalejandro",
    password="RobalejandroTest1234",
    database="u591727659_test")
    sql = """UPDATE pedidos_v3 SET platillos_pollo_normal= %s,platillos_pollo_sin_sal= %s,
            pescado_sin_sal= %s,
            pescado_normal= %s,
            salmon_sin_sal= %s,
            salmon_normal= %s,
            camarones_sin_sal= %s,
            camarones_normal= %s,
            atun_sin_sal= %s,
            atun_normal= %s,
            e_buffalo= %s,
            e_carnes_frias= %s,
            d_liz= %s,
            e_cesar= %s,
            h_normal= %s,
            h_chilaca= %s,
            h_champ= %s,
            h_haw= %s,
            h_normal_pan_thin= %s,
            h_normal_pan_margarita= %s,
            h_normal_pan_lechuga= %s,
            h_chilaca_pan_thin= %s,
            h_chilaca_pan_margarita= %s,
            h_chilaca_pan_lechuga= %s,
            h_champ_pan_thin= %s,
            h_champ_pan_margarita= %s,
            h_champ_pan_lechuga= %s,
            h_haw_pan_thin= %s,
            h_haw_pan_margarita= %s,
            h_haw_pan_lechuga= %s,
            e_buffalo_alitas= %s,
            e_buffalo_buffalo= %s,
            e_buffalo_mostaza= %s,
            e_buffalo_limon_pepper= %s,
            e_buffalo_natural= %s,
            e_buffalo_bbqs= %s,
            e_carnes_frias_alitas= %s,
            e_carnes_frias_buffalo= %s,
            e_carnes_frias_mostaza= %s,
            e_carnes_frias_limon_pepper= %s,
            e_carnes_frias_natural= %s,
            e_carnes_frias_bbqs= %s,
            e_dliz_alitas= %s,
            e_dliz_buffalo= %s,
            e_dliz_mostaza= %s,
            e_dliz_limon_pepper= %s,
            e_dliz_natural= %s,
            e_dliz_bbqs= %s,
            e_cesar_alitas= %s,
            e_cesar_buffalo= %s,
            e_cesar_mostaza= %s,
            e_cesar_limon_pepper= %s,
            e_cesar_natural= %s,
            e_cesar_bbqs= %s,
            desayuno= %s,
            snack= %s,
            merienda= %s,
            cena= %s,
            ensaladas= %s,
            hamburguesas= %s,
            platillos_normales= %s,
            platillos_sin_sal= %s,
            platillos_totales= %s,
            Panini_carnes_frias=%s,
            Panini_pollo=%s WHERE id_pedido= %s"""
    values=(int(platillos_pollo_normal),
            int(platillos_pollo_sin_sal),
            int(pescado_sin_sal),
            int(pescado_normal),
            int(salmon_sin_sal),
            int(salmon_normal),
            int(camarones_sin_sal),
            int(camarones_normal),
            int(atun_sin_sal),
            int(atun_normal),
            int(e_buffalo),
            int(e_carnes_frias),
            int(d_liz),
            int(e_cesar),
            int(h_normal),
            int(h_chilaca),
            int(h_champ),
            int(h_haw),
            int(h_normal_pan_thin),
            int(h_normal_pan_margarita),
            int(h_normal_pan_lechuga),
            int(h_chilaca_pan_thin),
            int(h_chilaca_pan_margarita),
            int(h_chilaca_pan_lechuga),
            int(h_champ_pan_thin),
            int(h_champ_pan_margarita),
            int(h_champ_pan_lechuga),
            int(h_haw_pan_thin),
            int(h_haw_pan_margarita),
            int(h_haw_pan_lechuga),
            int(e_buffalo_alitas),
            int(e_buffalo_buffalo),
            int(e_buffalo_mostaza),
            int(e_buffalo_limon_pepper),
            int(e_buffalo_natural),
            int(e_buffalo_bbqs),
            int(e_carnes_frias_alitas),
            int(e_carnes_frias_buffalo),
            int(e_carnes_frias_mostaza),
            int(e_carnes_frias_limon_pepper),
            int(e_carnes_frias_natural),
            int(e_carnes_frias_bbqs),
            int(e_dliz_alitas),
            int(e_dliz_buffalo),
            int(e_dliz_mostaza),
            int(e_dliz_limon_pepper),
            int(e_dliz_natural),
            int(e_dliz_bbqs),
            int(e_cesar_alitas),
            int(e_cesar_buffalo),
            int(e_cesar_mostaza),
            int(e_cesar_limon_pepper),
            int(e_cesar_natural),
            int(e_cesar_bbqs),
            int(desayuno),
            int(snack),
            int(merienda),
            int(cena),
            int(ensaladas),
            int(hamburguesas),
            int(platillos_normales),
            int(platillos_sin_sal),
            int(platillos_totales),
            int(panini_carnes_frias),
            int(panini_pollo),0)
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    st.success('Contabilizador actualizado')

if submitted6:
    df_merge= session_state.df.merge(df_costos,on='Pedido',how='left')
    df_merge = df_merge.rename(columns={'Costo':'Costo platillo'})
    df_merge = df_merge.merge(df_ruta,on='Ruta',how='left')
    df_merge = df_merge.rename(columns={'COSTO_R':'Costo ruta'})
    df_merge.fillna(0,inplace=True)
    df_merge['Costo pedido específico'] = df_merge['Costo pedido específico'].replace('-','0.0')
    df_merge['Costo pedido específico'] = df_merge['Costo pedido específico'].astype(float)* df_merge['Cantidad']
    df_merge['Costo platillo cantidad'] = df_merge['Costo platillo'] * df_merge['Cantidad']
    df_merge['Costo desayuno'] = df_merge['Desayuno'] * df_costos.loc[df_costos['Pedido']=='Desayuno','Costo'].values
    df_merge['Costo snack'] = df_merge['Snack'] * df_costos.loc[df_costos['Pedido']=='Snack','Costo'].values
    df_merge['Costo merienda'] = df_merge['Merienda'] * df_costos.loc[df_costos['Pedido']=='Merienda','Costo'].values
    df_merge['Costo cena'] = df_merge['Cena'] * df_costos.loc[df_costos['Pedido']=='Cena','Costo'].values
    df_merge['Costo total'] = df_merge['Costo ruta']+ df_merge['Costo platillo cantidad'] + df_merge['Costo desayuno'] + df_merge['Costo snack'] + df_merge['Costo merienda'] + df_merge['Costo cena'] + df_merge['Costo pedido específico']
    df_merge['Date'] = today
    df_merge = df_merge.rename(columns={'Desayuno':'# Desayuno'})
    df_merge = df_merge.rename(columns={'Snack':'# Snack'})
    df_merge = df_merge.rename(columns={'Merienda':'# Merienda'})
    df_merge = df_merge.rename(columns={'Cena':'# Cena'})
    df_merge_final = df_merge[['Date','Cliente','Pedido','Variación','Ruta','# Desayuno','# Snack','# Merienda','# Cena','Costo ruta','Costo platillo cantidad','Costo desayuno','Costo snack','Costo merienda','Costo cena','Costo total']]
    nombre = "reporte_"+ str(today)#-datetime.timedelta(days=1))
    #df_merge_final.to_excel(nombre+".xlsx")

    #commented next three lines
    #df_merge_final.to_csv('reportes/'+nombre+".csv")
    
    st.download_button(
        label="Download",
        data=df_merge.to_csv().encode(),
        file_name="reporte_"+ str(today)+".csv",
        mime="text/csv"
    )
    st.dataframe(df_merge)
    st.success('Reporte diario generado')

    

if submitted7:
    #folder = 'reportes'
    #files= []
    #today = date.today()
    #for file in os.listdir(folder):
    #    if (pd.to_datetime(file[8:-4]) <= today)and (pd.to_datetime(file[8:-4])  >=  today - datetime.timedelta(days=7)):
    #        files.append(os.path.join(folder,file))
    dfs=[]
    #for file_path in files:
    for file_path in file:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        dfs.append(df)


    df_final = pd.concat(dfs)
    df_final.reset_index(inplace=True)
    df_final.drop(['Unnamed: 0','index'],axis=1,inplace=True)

    pedido_clientes= {}
    customers = df_final['Cliente'].unique()
    for customer in customers:
        df_customer = df_final.loc[df_final['Cliente']==customer,:].reset_index()
        df_customer.Pedido.value_counts().to_dict()
        pedido_clientes[customer] = df_customer.Pedido

    x = df_final.groupby(['Cliente']).agg({'Pedido':'count',
                                       '# Desayuno':'sum',
                                       '# Snack':'sum',
                                       '# Merienda':'sum',
                                       '# Cena':'sum',
                                       'Costo ruta':'sum',
                                       'Costo platillo':'sum',
                                       'Costo desayuno':'sum',
                                       'Costo snack':'sum',
                                       'Costo merienda':'sum',
                                       'Costo cena':'sum'
                                       }).reset_index()
    for index,row in x.iterrows():
        if row['# Desayuno']== 5:
            #x.loc[index,'Costo desayuno'] = row['Costo desayuno']- 20
            x.loc[index,'Costo desayuno'] = 280
        if row['# Cena']== 5:
            #x.loc[index,'Costo cena'] = row['Costo cena']- 25
            x.loc[index,'Costo cena'] = 400
        
        costo_platillo = row['Costo platillo']
        if row['Pedido'] == 5:
            factor = row['Costo platillo'] //  425
            costo_platillo = 425*factor
            if 'Salmón'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Salmón']])* 50
            if 'Camarones'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Camarones']])* 50
            if 'Atun'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Atun']])* 50
                
        if row['Pedido'] == 4:
            factor = row['Costo platillo'] // 400
            costo_platillo = 400*factor
            if 'Salmón'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Salmón']])* 50
            if 'Camarones'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Camarones']])* 50
            if 'Atun'in pedido_clientes[row['Cliente']]:
                costo_platillo += (pedido_clientes[row['Cliente']['Atun']])* 50
                
        row['Costo platillo'] = costo_platillo

    x['Costo final semanal'] = x['Costo ruta']+x['Costo platillo']+x['Costo desayuno']+ x['Costo snack']+ x['Costo merienda']+x['Costo cena']
    name = 'reportes/reporte_semanal_'+str(today)+'.csv'
    #x.to_csv(name)
    #Agregado
    st.download_button(
        label="Download",
        data=x.to_csv().encode(),
        file_name="reporte_semanal"+ str(today)+".csv",
        mime="text/csv"
    )
    st.success('Reporte semanal generado')

