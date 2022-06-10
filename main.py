import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from datetime import datetime
#from PIL import Image

gsheetid = '1ubyAIc1JOWLRXz-vvTmfhbi1-AZALWKkQo8hJkfvVrc'
list_1 = 'sector_margin'
list_2 = 'growth_rate'
list_3 = 'deltas_breakdown'
list_4 = 'answer_score'

df_sector_margin_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_sector_margin = pd.read_csv(df_sector_margin_csv)
df_sector_margin.set_index('dish_name', inplace=True)
df_sector_margin = pd.Series(df_sector_margin['dish_id'])

industry_list = df_sector_margin.index

    
# Функция приложения
def show_predict_page():
    d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
    st.write('Your birthday is:', d)

# Вызываем приложение
show_predict_page()
