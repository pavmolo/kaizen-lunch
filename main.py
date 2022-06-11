import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from datetime import datetime
from datetime import date
from notion.client import NotionClient
import requests, json
client = NotionClient(token_v2="3b7c4e7acf1f99610e191d44b024dd9ba201e470a96860d2e1607fba7370497a5c0500cb3c49319ae8cc28607d72021bf6a388018475e9011fa9e891c6b3e57c10ee832634524a77068a6a4b2d89")
page = client.get_block("https://www.notion.so/kaizeninstitute/4b77f19c3cbb4d8ea289eefd438da180?v=973c72e0c791442e937f86ca5a5c2f44")


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

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
    order_list_full['Дата'] = today
    col2.dataframe(data=order_list_full, width=None, height=None)
    col2.markdown(f'The old title is" {page.title}'
# Вызываем приложение
show_predict_page()
