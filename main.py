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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1qZS-Y7NxD15B3rPTGpYIsZfF67ySaBjAEsUEsDIwTdo'
SAMPLE_RANGE_NAME = 'base'

service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()




gsheetid = '1ubyAIc1JOWLRXz-vvTmfhbi1-AZALWKkQo8hJkfvVrc'
list_1 = 'menu'
list_2 = 'team'

df_dish_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
member_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)
df_dish_list = pd.read_csv(df_dish_list_csv)
member_list = pd.read_csv(member_list_csv)
df_dish_list.set_index('dish_name', inplace=True)
df_dish_list = pd.Series(df_dish_list['dish_id'])
df_member_list = pd.Series(member_list['member'])

dish_list = df_dish_list.index
ln_list = len(dish_list)
today = datetime.today()
# Функция приложения
def show_predict_page():
    d = st.date_input("Сегодня:", today)
    st.write('Текущая дата:', d)
    member = st.radio('Выберите едока', df_member_list, index=0, horizontal=True)
    col1, col2 = st.columns(2)
    order_list = []
    for i in range(0, ln_list):
        dish_list_radio = col1.radio(df_dish_list.index[i], [int(0), int(1), int(2)], index=0, horizontal=True)
        dish_item = [df_dish_list.index[i], dish_list_radio]
        order_list.append(dish_item)
    order_list = pd.DataFrame(order_list, columns=['Блюдо', 'Количество'])
    order_list_not_zero = order_list[order_list['Количество'] > 0]
    col2.dataframe(data=order_list_not_zero, width=None, height=None)
    order_list_full = order_list_not_zero
    order_list_full['Едок'] = member
    order_list_full['Дата'] = str(today)
    order_list_full['Количество'] = order_list_full['Количество'].astype('str')
    col2.dataframe(data=order_list_full, width=None, height=None)
    if col2.button('Отправить запрос на еду'):
      body = []
      for row in order_list_full.index:
        stroka = [order_list_full.loc[row][3], order_list_full.loc[row][2], order_list_full.loc[row][0], order_list_full.loc[row][1]]
        body.append(stroka)
      resp = service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body={'values': body}).execute()
      col2.write('Запрос принят')
      today_dish_list_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
      today_dish_list = pd.read_csv(today_dish_list_csv)
      today_dish_list['Дата'] = pd.to_datetime(today_dish_list['Дата']).dt.date
      today_dish_list_fin = today_dish_list[today_dish_list['Дата'] == pd.Timestamp.today().date()]
      col2.dataframe(data=today_dish_list_fin, width=None, height=None)
# Вызываем приложение

show_predict_page()
