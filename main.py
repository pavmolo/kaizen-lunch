import streamlit as st
import os.path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1qZS-Y7NxD15B3rPTGpYIsZfF67ySaBjAEsUEsDIwTdo'
SAMPLE_RANGE_NAME = 'base'

service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()




gsheetid = '1ubyAIc1JOWLRXz-vvTmfhbi1-AZALWKkQo8hJkfvVrc'
list_1 = 'menu'
list_2 = 'team'
df_dish_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
member_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)

df_dish_list = pd.Series(df_dish_list['dish_id'])
df_member_list = pd.Series(member_list['member'])

df_dish_list = df_dish_list()
df_member_list = df_member_list()

dish_list = df_dish_list.index
ln_list = len(dish_list)
today = datetime.today()
today_dish_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
today_dish_list = pd.read_csv(today_dish_list_csv)
today_dish_list['Дата'] = pd.to_datetime(today_dish_list['Дата']).dt.date
today_dish_list_fin = today_dish_list[today_dish_list['Дата'] == pd.Timestamp.today().date()]
table = pd.pivot_table(today_dish_list_fin, values='Количество', index='Блюдо', aggfunc=sum)
edoki = today_dish_list_fin['Едок'].unique()
# Функция приложения
def show_predict_page():
    st.title('🍜🥓Форма заказа еды🥓🍜')
    #d = st.date_input("Сегодня:", today)
    st.write('Текущая дата:', pd.Timestamp.today().date())
    if len(table) != 0:
        with st.expander("Заказы на сегодня"):
            #st.write('Все заказы на сегодня:')
            #st.dataframe(data=today_dish_list_fin, width=None, height=None)
            st.write('Список блюд со всех заказов:')
            st.table(data=table)
            #st.write('Список активных едоков:')
            #st.table(data=edoki)
        if len(edoki) != 0:
            st.write('Активные едоки сегодня:')
            for i in edoki:
                with st.expander(i):
                    edok_list = today_dish_list_fin[today_dish_list_fin['Едок'] == i].drop(labels=['Дата', 'Едок'], axis=1)
                    st.table(data=edok_list)
    else:
        st.info('На сегодня еще никто ничего не заказал')
    st.header('Кто вы:')
    member = st.radio('Выберите едока', df_member_list, index=0, horizontal=True)
    st.header('Что будете кушать?')
    order_list = []
    for i in range(0, ln_list):
        dish_list_radio = st.radio(df_dish_list.index[i], [int(0), int(1), int(2)], index=0, horizontal=True)
        dish_item = [df_dish_list.index[i], dish_list_radio]
        order_list.append(dish_item)
    order_list = pd.DataFrame(order_list, columns=['Блюдо', 'Количество'])
    order_list_not_zero = order_list[order_list['Количество'] > 0]
    order_list_full = order_list_not_zero
    order_list_full['Едок'] = member
    order_list_full['Дата'] = str(today)
    order_list_full['Количество'] = order_list_full['Количество'].astype('str')
    
    # Блок отображения делаемого заказа
    if len(order_list_not_zero) !=0:
        st.header('Ваш заказ:')
        st.dataframe(data=order_list_not_zero, width=None, height=None)
        # Кнопка заказа еды
        #st.dataframe(data=order_list_full, width=None, height=None)
        if st.button('Отправить запрос на еду'):
            order = []
            for row in order_list_full.index:
                stroka = [order_list_full.loc[row][3], order_list_full.loc[row][2], order_list_full.loc[row][0], order_list_full.loc[row][1]]
                order.append(stroka)
            resp = service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body={'values': order}).execute()
            st.success('ВАШ ЗАКАЗ ПРИНЯТ!')
            
            
   
    
# Вызываем приложение

show_predict_page()
