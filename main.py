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
ln_list = len(dish_list)
    
# Функция приложения
def show_predict_page():
    d = st.date_input("Сегодня:", today)
    st.write('Текущая дата:', d)
    col1, col2 = st.columns(2)
    order_list = []
    for i in range(0, ln_list):
        dish_list_radio = col1.radio(df_dish_list.index[i], [0, 1, 2], index=0, horizontal=True)
        dish_item = [[df_dish_list.index[i]], [dish_list_radio]]
        order_list.append(dish_item)
    order_list = pd.DataFrame(order_list, columns=['Блюдо', 'Количество'])
    order_list = order_list[order_list['Количество'] != 0]
    st.dataframe(data=order_list, width=None, height=None)
# Вызываем приложение
show_predict_page()
