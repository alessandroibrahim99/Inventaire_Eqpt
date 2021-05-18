# # -*- coding: utf-8 -*-
# """
# Created on Wed Mar 24 15:23:18 2021

# @author: alessandro.ibrahim
# """
import base64
from io import BytesIO

import streamlit as st
import pandas as pd
###from plotly.offline import iplot
#import plotly.graph_objs as go
#import plotly.express as px
#fig = go.Figure()


###LOGO
st.write("")
col1, mid, col2 = st.beta_columns([1,1,20])
with col1:
    st.image('pom1.jpg', width=250)
with col2:
    st.write('')
    
#######

####Data Load    
csv_file_state = 'Liste_Eqpt_Sites.csv'





###Search by JOB
#Dashboard Sidebar with State list

@st.cache
def load_data(nrows):
    data = pd.read_csv(csv_file_state)
    return data

df = load_data(100000) 
df1 = load_data(100000)
#df = df.loc[df['Active'] == 'Y']
dfstate = df
df1 = df

df1=df1.fillna("")
df=df.fillna("")





######
st.sidebar.title("Equip.Inventory - By Job or Name")

State_list = st.sidebar.selectbox('Choose your Job (ex:20.0378 or ROBERVAL )', sorted(dfstate.Job.unique()), index=0)#[:40000])
#Class_listN = st.sidebar.selectbox('Job Name', list(dfstate[dfstate.Job == State_list].Act_Loc_Name.unique()), index=0)
Class_list = st.sidebar.selectbox('Class Name', list(dfstate[dfstate.Job == State_list].EquipClassName.unique()))
Class_listt = st.sidebar.selectbox('Sub-Class Name', list(dfstate[dfstate.EquipClassName == Class_list].EquipSousClassName.unique()), index=0)


#State_list = st.sidebar.selectbox('Choose your Job (ex:20.0378)', sorted(dfstate.Job.unique()), index=0)#[:40000])
#Class_list = st.sidebar.selectbox('Class Name', list(dfstate[dfstate.Job == State_list].EquipClassName.unique()))

# Select a State from sidebar to update this chart
st.title("""Equip.Inventory - By Job
 	""")

newdf = dfstate[dfstate['Job'] == State_list]



###########
#First table
# Select a State from sidebar to update this chart

st.markdown("""Number of Equipments by Job""")

newdf = dfstate[dfstate['Job'] == State_list]
df = newdf


def get_table():
    datatable = df.groupby(["Job"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable

newdf1 = get_table()
newdf1.set_index('Job', inplace=True)
newdf1.columns = ['Nb.of Equipments']

st.dataframe(newdf1)
##############

###########
#Second first table

st.markdown("""Number of Equipments by Job & Class""")


def get_table():
    datatable = df.groupby(["Job","EquipClassName"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable

newdf1 = get_table()


df = newdf1
df.sort_values('Equip. Code')
df.set_index('Job', inplace=True)

newdf1 = df
newdf1.columns = ['Class Name','Nb. of Equipments']
st.dataframe(newdf1)
############################


###########
#third table

st.markdown("""Equipment Inventory  List - Detailed Version
 	""")

df = newdf


def get_table():
    datatable = df[['Job', 'EquipClassName','EquipSousClassName', 'Equip. Code','Equip. Name', 'Equip. Desc', 'Start Date', 'Brand', 'Model', 'Year', 'Serial #']].sort_values(by=['Job'], ascending=False)
    
    return datatable

df = get_table()

df.set_index('Job', inplace=True)
df.columns = ['Class Name','EquipSousClassName', 'Equip. Code','Equip. Name', 'Equip. Desc','Start Date', 'Brand', 'Model', 'Year', 'Serial #']
st.dataframe(df)
###########

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file - Detailed Version</a>' # decode b'abc' => abc

df = df # your dataframe
st.markdown(get_table_download_link(df), unsafe_allow_html=True)
###########



# #---------------------

#Dashboard Sidebar with State list
st.sidebar.title("Equip.Inventory - By Class Name")
#State_list1 = st.sidebar.selectbox('Class Name (ex:Laser Rotatif)', df1.EquipClassName)#[:80000])
State_list1 = st.sidebar.selectbox('Class Name (ex: Camionnette)', sorted(df1.EquipClassName.unique()), index=0)#[:40000])
Class_list1 = st.sidebar.selectbox('Sub-Class Name', list(df1[df1.EquipClassName == State_list1].EquipSousClassName.unique()), index=0)#, index=0)#[:40000])


###Search by Class
# Select a State from sidebar to update this chart
st.title("""Equip.Inventory - By Class Name
 	""")

###########
#First1 table
st.markdown("""Number of Equipments by Class - All Jobs""")
newdf = df1[df1['EquipClassName'] == State_list1 ]# & df1[df1['EquipClassName'] == Class_list1 ])


df = newdf


def get_table():
    datatable = df.groupby(["EquipClassName"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable

newdf1 = get_table()
newdf1.set_index('EquipClassName', inplace=True)


newdf1.columns = ['Nb.of Equipments']
st.dataframe(newdf1)



###########

###########
#First table
st.markdown("""Number of Equipments by Class - All Jobs""")
newdf = df1[df1['EquipClassName'] == State_list1 ]


df = newdf


def get_table():
    datatable = df.groupby(["EquipClassName"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable

newdf1 = get_table()
newdf1.set_index('EquipClassName', inplace=True)


newdf1.columns = ['Nb.of Equipments']
st.dataframe(newdf1)



###########
#Second table
st.markdown("""Number of Equipments by Class & Job - All Jobs""")


def get_table1():
    datatable1 = df.groupby(["EquipClassName","Job"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable1

newdf1 = get_table1()


df1 = newdf1
df1.sort_values('Equip. Code')
df1.set_index('EquipClassName', inplace=True)

newdf1 = df1
newdf1.columns = ['Job','Nb.of Equipments']
st.dataframe(newdf1)



###########
#Third table - Map

def get_table2():
    datatable2 = df.groupby(["EquipClassName","Job", "lat", "lon"], as_index=False, sort=False)["Equip. Code"].count()
    
    return datatable2

newdf2 = get_table2()
st.map(newdf2)


