from pandas.core.frame import DataFrame
from pywebio import session
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
from datetime import date
import SessionState
from pywebio.input import *
import datetime
from datetime import timedelta
import os
import beepy as beep
from github import Github
import requests
import io
from io import BytesIO
#Comentado porque ahora se leeran desde el github
#df_customer = pd.read_csv('clientes.csv')
#df_structure = pd.read_csv('estructura.csv')
#df_costos =  pd.read_csv('costos.csv')
#df_ruta =  pd.read_csv('rutas.csv')

url_customer = "https://raw.githubusercontent.com/robalejandrogon/files/main/clientes.csv" # Make sure the url is the raw version of the file on GitHub
download_customer = requests.get(url_customer).content
df_customer = pd.read_csv(io.StringIO(download_customer.decode('utf-8')))
url_structure = "https://raw.githubusercontent.com/robalejandrogon/files/main/estructura.csv" # Make sure the url is the raw version of the file on GitHub
download_structure = requests.get(url_structure).content
df_structure = pd.read_csv(io.StringIO(download_structure.decode('utf-8')))
url_costos = "https://raw.githubusercontent.com/robalejandrogon/files/main/costos.csv" # Make sure the url is the raw version of the file on GitHub
download_costos = requests.get(url_costos).content
df_costos = pd.read_csv(io.StringIO(download_costos.decode('utf-8')))
url_ruta = "https://raw.githubusercontent.com/robalejandrogon/files/main/rutas.csv" # Make sure the url is the raw version of the file on GitHub
download_ruta = requests.get(url_ruta).content
df_ruta = pd.read_csv(io.StringIO(download_ruta.decode('utf-8')))

def upload_to_github(content):
    token = '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'
    g = Github(token)
    GITHUB_REPO = "files"
    repo = g.get_user().get_repo(GITHUB_REPO)
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    #with open('myfile.txt', 'r') as file:
    #    content = file.read()

    # Upload to github
    git_prefix = 'folder1/'
    git_file = 'myfile.txt'
    print(f'all_files {all_files}')
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", ''.join(content), contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')


if 'pedidos' not in st.session_state:
    st.session_state['pedidos']=['Pollo','Pescado','Salmón','Camarones','E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw','Atun']
if 'variacion' not in st.session_state:
    st.session_state['variacion']=['Sin carbo','Colitis','Sin sal', 'Sin chile','Otro * especificar']
if 'clientes' not in st.session_state:
    st.session_state['clientes'] = df_customer['NOMBRE '].tolist()

session_state = SessionState.get(df=df_structure)

#customers = df_customer['NOMBRE '].tolist()

#variacion
#variacion= ['Sin carbo','Colitis','Sin sal', 'Sin chile','Otro * especificar']

#ruta
#ruta = ['R1','R2','Local']
ruta = ['R1A','R1C','R1V','R2A','R2C','R2V']

#pedidos
#pedidos=['Pollo','Pescado','Salmón','Camarones','E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw']

session_state = SessionState.get(df=df_structure)

#Title
#table = pd.DataFrame({'Id':['-'],'Nombre':['-'],'Pedido':['-'],'Variación':['-'],'Ruta':['-'],'Desayuno':['-'],'Snack':['-'],'Meridna':['-'],'Cena':['-']})


st.title('SGPA')

image = Image.open('image_1.png')
today = date.today()

#Description
st.markdown("""
Aplicación para gestión de ordenes y pedidos.
""")

#Side header
st.sidebar.markdown(today)
st.sidebar.image(image)
my_form = st.sidebar.form(key = "form1")
new_customer = my_form.text_input('Nuevo cliente', '-')
submitted0 = my_form.form_submit_button('Agregar nuevo cliente .')
if submitted0:
    st.session_state['clientes'].append(new_customer)
    st.success('Nuevo Cliente agregado')
selected_customer = my_form.selectbox('Nombre:',st.session_state['clientes'])

#my_form2 = st.sidebar.form(key="form2")
new_pedido = my_form.text_input('Nuevo pedido', '-')
submitted1 = my_form.form_submit_button('Agregar nuevo pedido.')
if submitted1:
    st.session_state['pedidos'].append(new_pedido)
    st.success('Nuevo pedido agregado')
selected_pedido = my_form.selectbox('Pedido:',st.session_state['pedidos'])

#my_form3 = st.sidebar.form(key="form3")
new_variacion = my_form.text_input('Nuevo variacion', '-')
submitted2 = my_form.form_submit_button('Agregar nueva variacion.')
if submitted2:
    st.session_state['variacion'].append(new_variacion)
    st.success('Nueva variación agregado')
selected_variacion= my_form.selectbox('Variación',st.session_state['variacion'])

#my_form4 = st.sidebar.form(key="form4")
selected_ruta = my_form.selectbox('Ruta:',ruta)
desayuno = my_form.number_input('Desayuno',0)
snack = my_form.number_input('Snack',0)
merienda = my_form.number_input('Merienda', 0)
cena = my_form.number_input('Cena', 0)
submitted3 = my_form.form_submit_button('Agregar')
submitted4 = my_form.form_submit_button('Editar')
submitted5 = my_form.form_submit_button('Eliminar')
submitted_reinicio = my_form.form_submit_button('reiniciar')
uploaded_file = my_form.file_uploader("Subir reportes diarios")


def add_new_customer():
    y=pd.DataFrame({'Cliente':[selected_customer],
                    'Pedido':[selected_pedido],
                    'Variación':[selected_variacion],
                    'Ruta':[selected_ruta],
                    'Desayuno':[int(desayuno)],
                    'Snack':[int(snack)],
                    'Merienda':[int(merienda)],
                    'Cena':[int(cena)]})
    session_state.df = session_state.df.append(y,ignore_index=True)
    st.success('Cliente agregado')

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
    if selected_customer in session_state.df.Cliente.tolist():
        st.warning('Cliente ya registrado')
    else:
        add_new_customer()

if submitted4:
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Pedido'] = selected_pedido
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Variación'] = selected_variacion
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Ruta'] = selected_ruta
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Desayuno'] = desayuno
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Snack'] = snack
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Merienda'] = merienda
    session_state.df.loc[session_state.df['Cliente']==selected_customer,'Cena'] = cena
    st.success('Cliente actualizado')

if submitted5:
    i = session_state.df.loc[session_state.df['Cliente']==selected_customer,:].index
    session_state.df.drop(i,inplace=True)
    session_state.df.reset_index(inplace=True)
    session_state.df.drop('index',axis=1,inplace=True)
    st.success('Cliente eliminado')

if submitted_reinicio:
    more_lines = [
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n",
    str(0)+"\n"]
    #commented next 3 lines
    #file1 = open('myfile.txt', 'w')
    #file1.writelines(more_lines)
    #file1.close()
    upload_to_github(more_lines)
    session_state = SessionState.get(df=df_structure)

st.dataframe(session_state.df)
file = st.file_uploader("Subir reportes para generar reporte semanal", type=['csv'],accept_multiple_files=True)
if not file:
    st.write("Upload a .csv or .xlsx file to get started")
st.write(file)
print(f'File : {file}')
with st.container():
    col1,col2,col3,col4,col5= st.columns(5)
    submitted4 = col1.button('Gráfica')
    submitted5 = col2.button('Actualizar')
    submitted6 = col3.button('Reporte diario')
    submitted7 = col4.button('Reporte semanal')
    submitted8 = col5.button('Ordenar por ruta')

if submitted8:
    #ruta = ['R1A','R1C','R1V','R2A','R2C','R2V']
    session_state.df['Ruta'] = pd.Categorical(session_state.df['Ruta'], ['R1A','R1C','R2A','R2C','R1V','R2V'])
    session_state.df.sort_values("Ruta",inplace=True)

if submitted4:
    st.bar_chart(session_state.df['Pedido'].value_counts())

if submitted5:
    platillos_pollo_normal = len(session_state.df.loc[(session_state.df.Pedido=='Pollo') & 
                                                  (
                                                      (session_state.df['Variación']=='Sin carbo') |
                                                      (session_state.df['Variación']=='Colitis') |
                                                      (session_state.df['Variación']=='Sin chile') |
                                                      (session_state.df['Variación']=='Otro * especificar')
                                                      ),
                                                      'Pedido'])

    platillos_pollo_sin_sal = len(session_state.df.loc[(session_state.df.Pedido=='Pollo') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Pedido'])

    pescado_sin_sal = len(session_state.df.loc[(session_state.df.Pedido=='Pescado') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Pedido'])
    
    pescado_normal = len(session_state.df.loc[(session_state.df.Pedido=='Pescado') & 
                                                  (
                                                      (session_state.df['Variación']=='Sin carbo') |
                                                      (session_state.df['Variación']=='Colitis') |
                                                      (session_state.df['Variación']=='Sin chile') |
                                                      (session_state.df['Variación']=='Otro * especificar')
                                                      ),
                                                      'Pedido'])

    salmon_sin_sal = len(session_state.df.loc[(session_state.df.Pedido=='Salmón') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Pedido'])

    salmon_normal = len(session_state.df.loc[(session_state.df.Pedido=='Salmón') & 
                                                  (
                                                      (session_state.df['Variación']=='Sin carbo') |
                                                      (session_state.df['Variación']=='Colitis') |
                                                      (session_state.df['Variación']=='Sin chile') |
                                                      (session_state.df['Variación']=='Otro * especificar')
                                                      ),
                                                      'Pedido'])
    
    camarones_sin_sal = len(session_state.df.loc[(session_state.df.Pedido=='Camarones') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Pedido'])

    camarones_normal = len(session_state.df.loc[(session_state.df.Pedido=='Camarones') & 
                                                  (
                                                      (session_state.df['Variación']=='Sin carbo') |
                                                      (session_state.df['Variación']=='Colitis') |
                                                      (session_state.df['Variación']=='Sin chile') |
                                                      (session_state.df['Variación']=='Otro * especificar')
                                                      ),
                                                      'Pedido'])
    
    atun_sin_sal = len(session_state.df.loc[(session_state.df.Pedido=='Atun') & 
                                                  (session_state.df['Variación']=='Sin sal'),
                                                      'Pedido'])

    atun_normal = len(session_state.df.loc[(session_state.df.Pedido=='Atun') & 
                                                  (
                                                      (session_state.df['Variación']=='Sin carbo') |
                                                      (session_state.df['Variación']=='Colitis') |
                                                      (session_state.df['Variación']=='Sin chile') |
                                                      (session_state.df['Variación']=='Otro * especificar')
                                                      ),
                                                      'Pedido'])
    #'E.Buffalo','E. Carnes Frias','E. Dliz','E. Cesar','Hamb Normal','Hamb Chilaca','Hamb Champiñones','Hamb Haw'
    e_buffalo = len(session_state.df.loc[(session_state.df.Pedido=='E.Buffalo'),
                                                      'Pedido'])
    e_carnes_frias = len(session_state.df.loc[(session_state.df.Pedido=='E. Carnes Frias'),
                                                      'Pedido'])
    d_liz = len(session_state.df.loc[(session_state.df.Pedido=='E. Dliz'),
                                                      'Pedido'])
    e_cesar = len(session_state.df.loc[(session_state.df.Pedido=='E. Cesar'),
                                                      'Pedido'])
    h_normal = len(session_state.df.loc[(session_state.df.Pedido=='Hamb Normal'),
                                                      'Pedido'])
    h_chilaca = len(session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca'),
                                                      'Pedido'])
    h_champ = len(session_state.df.loc[(session_state.df.Pedido=='Hamb Chilaca'),
                                                      'Pedido'])
    h_haw = len(session_state.df.loc[(session_state.df.Pedido=='Hamb Haw'),
                                                      'Pedido'])
    desayuno = session_state.df['Desayuno'].sum()
    print(f'Desayuno {desayuno}')

    snack= session_state.df['Snack'].sum()

    merienda= session_state.df['Merienda'].sum()

    cena= session_state.df['Cena'].sum()

    ensaladas = e_buffalo  + e_carnes_frias + d_liz + e_cesar 
    platillos_normales = platillos_pollo_normal + pescado_normal + salmon_normal  + camarones_normal  + atun_normal
    platillos_sin_sal = platillos_pollo_sin_sal + pescado_sin_sal + salmon_sin_sal + camarones_sin_sal + atun_normal 
    hamburguesas = h_normal + h_chilaca + h_champ + h_haw
    platillos_totales = desayuno + snack+ merienda+ cena+ platillos_pollo_normal + platillos_pollo_sin_sal + pescado_sin_sal + pescado_normal + salmon_sin_sal + salmon_normal + camarones_sin_sal + camarones_normal + atun_sin_sal + atun_normal +e_buffalo +e_carnes_frias + d_liz + e_cesar + h_normal + h_chilaca + h_champ + h_haw
    print(f'platillos totales {platillos_totales}')
    print(f'platillos normales {platillos_normales}')
    print(f'platillos sin sal {platillos_sin_sal}')
    print(f'Hamburguesas {hamburguesas}')
    print(f'Ensalada {ensaladas}')
    more_lines = [str(platillos_pollo_normal)+"\n",
    str(platillos_pollo_sin_sal)+"\n",
    str(pescado_sin_sal)+"\n",
    str(pescado_normal)+"\n",
    str(salmon_sin_sal)+"\n",
    str(salmon_normal)+"\n",
    str(camarones_sin_sal)+"\n",
    str(camarones_normal)+"\n",
    str(atun_sin_sal)+"\n",
    str(atun_normal)+"\n",
    str(e_buffalo)+"\n",
    str(e_carnes_frias)+"\n",
    str(d_liz)+"\n",
    str(e_cesar)+"\n",
    str(h_normal)+"\n",
    str(h_chilaca)+"\n",
    str(h_champ)+"\n",
    str(h_haw)+"\n",
    str(desayuno)+"\n",
    str(snack)+"\n",
    str(merienda)+"\n",
    str(cena)+"\n",
    str(ensaladas)+"\n",
    str(hamburguesas)+"\n",
    str(platillos_normales)+"\n",
    str(platillos_sin_sal)+"\n",
    str(platillos_totales)+"\n",
    ]
    #commented next 3 lines
    #file1 = open('myfile.txt', 'w')
    #file1.writelines(more_lines)
    #file1.close()
    upload_to_github(more_lines)
    beep.beep(1)

if submitted6:
    df_merge= session_state.df.merge(df_costos,on='Pedido',how='left')
    df_merge = df_merge.rename(columns={'COSTO':'Costo platillo'})
    df_merge = df_merge.merge(df_ruta,on='Ruta',how='left')
    df_merge = df_merge.rename(columns={'COSTO_R':'Costo ruta'})
    df_merge['Costo desayuno'] = df_merge['Desayuno'] * df_costos.loc[df_costos['Pedido']=='Desayuno','COSTO'].values
    df_merge['Costo snack'] = df_merge['Snack'] * df_costos.loc[df_costos['Pedido']=='Snack','COSTO'].values
    df_merge['Costo merienda'] = df_merge['Merienda'] * df_costos.loc[df_costos['Pedido']=='Merienda','COSTO'].values
    df_merge['Costo cena'] = df_merge['Cena'] * df_costos.loc[df_costos['Pedido']=='Cena','COSTO'].values
    df_merge['Costo total'] = df_merge['Costo ruta']+df_merge['Costo platillo'] + df_merge['Costo desayuno'] + df_merge['Costo snack'] + df_merge['Costo merienda']+df_merge['Costo cena']
    df_merge['Date'] = today
    df_merge = df_merge.rename(columns={'Desayuno':'# Desayuno'})
    df_merge = df_merge.rename(columns={'Snack':'# Snack'})
    df_merge = df_merge.rename(columns={'Merienda':'# Merienda'})
    df_merge = df_merge.rename(columns={'Cena':'# Cena'})
    df_merge_final = df_merge[['Date','Cliente','Pedido','Variación','Ruta','# Desayuno','# Snack','# Merienda','# Cena','Costo ruta','Costo platillo','Costo desayuno','Costo snack','Costo merienda','Costo cena','Costo total']]
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
    print('Boton reporte semanal')
    #folder = 'reportes'
    #files= []
    #today = date.today()
    #for file in os.listdir(folder):
    #    print(f'File: {file}')
    #    if (pd.to_datetime(file[8:-4]) <= today)and (pd.to_datetime(file[8:-4])  >=  today - datetime.timedelta(days=7)):
    #        files.append(os.path.join(folder,file))
    dfs=[]
    #for file_path in files:
    for file_path in file:
        print('Filepath {file_path}')
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
            print(row['Costo desayuno'])
            #x.loc[index,'Costo desayuno'] = row['Costo desayuno']- 20
            x.loc[index,'Costo desayuno'] = 280
        if row['# Cena']== 5:
            print(row['Costo cena'])
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

