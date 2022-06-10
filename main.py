import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from datetime import datetime
from datetime import date

today = date.today()
#from PIL import Image

gsheetid = '1ubyAIc1JOWLRXz-vvTmfhbi1-AZALWKkQo8hJkfvVrc'
list_1 = 'menu'

df_dish_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_dish_list = pd.read_csv(df_dish_list_csv)
df_dish_list.set_index('dish_name', inplace=True)
df_dish_list = pd.Series(df_dish_list['dish_id'])

dish_list = df_dish_list.index

    
# Функция приложения
def show_predict_page():
    d = st.date_input("Сегодня:", today)
    st.write('Текущая дата:', d)
    dish_list_radio = st.radio('Меню', dish_list, index=0) 
    cols = st.columns((dish_list.len, 1))
    for i in range(0, dish_list.len):
        dish_list_radio = cols[i].radio('', df_dish_list.index[i], index=0)
# Вызываем приложение
show_predict_page()
