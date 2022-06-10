import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
#from PIL import Image

gsheetid = '1S7gJojFKedjSvSRM9npIDAzN_6mkSZhgEdGpNbxXnK0'
list_1 = 'sector_margin'
list_2 = 'growth_rate'
list_3 = 'deltas_breakdown'
list_4 = 'answer_score'

df_sector_margin_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_growth_rate_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)
deltas_breakdown_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_3)
answer_score_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_4)


df_sector_margin = pd.read_csv(df_sector_margin_csv)
df_growth_rate = pd.read_csv(df_growth_rate_csv)
df_deltas_breakdown = pd.read_csv(deltas_breakdown_csv)
df_answer_score = pd.read_csv(answer_score_csv)


df_growth_rate.set_index('growth_state', inplace=True)
df_sector_margin.set_index('sector', inplace=True)
df_deltas_breakdown.set_index('answer', inplace=True)
df_answer_score.set_index('answer_id', inplace=True)

df_sector_margin = pd.Series(df_sector_margin['margin'])
df_growth_rate = pd.Series(df_growth_rate['growth_rate'])
df_deltas_breakdown = pd.Series(df_deltas_breakdown['question_score'])

gro_state_list = df_growth_rate.index
industry_list = df_sector_margin.index
answers_list = df_answer_score['answer']

# Функция прибыли
def lost_profit(ind, mar, rev, marg, gro):
    growth_rate = df_growth_rate[mar]
    margin_ind_rate = df_sector_margin[ind]
    potencial_profit = rev * (margin_ind_rate)
    act_profit = (marg / 100) * rev
    profit_delta_qdc = max(potencial_profit - act_profit, 0.05 * act_profit)
    profit_delta_growth = max(((growth_rate - (gro / 100)) * rev * margin_ind_rate), 0.005 * rev)
    profit_delta_total = profit_delta_qdc + profit_delta_growth
    return [profit_delta_total, profit_delta_qdc, profit_delta_growth]

operation_breakdown_elems = 11
groth_breakdown_elems = 6

def break_down(a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11):
    table = df_answer_score[['answer', 'answer_score']].set_index('answer')
    table = pd.Series(table['answer_score'])
    arg_list = pd.Series([table[a_1], table[a_2], table[a_3], table[a_4], table[a_5], table[a_6], 
                          table[a_7], table[a_8], table[a_9], table[a_10], table[a_11]], index=df_deltas_breakdown.head(operation_breakdown_elems).index)
    prom_list = arg_list * df_deltas_breakdown.head(operation_breakdown_elems)
    sum_prom = prom_list.sum()
    return pd.Series(prom_list / sum_prom)

def break_down_g(a_12, a_13, a_14, a_15, a_16, a_17):
    table = df_answer_score[['answer', 'answer_score']].set_index('answer')
    table = pd.Series(table['answer_score'])
    arg_list = pd.Series([table[a_12], table[a_13], table[a_14], table[a_15], table[a_16], table[a_17]], index=df_deltas_breakdown.tail(groth_breakdown_elems).index)
    prom_list = arg_list * df_deltas_breakdown.tail(groth_breakdown_elems)
    sum_prom = prom_list.sum()
    return pd.Series(prom_list / sum_prom)
    
    
# Функция приложения
def show_predict_page():
    #image = Image.open('https://www.kaizen.com/images/kaizen_logo.png')
    #st.image(image, caption='Kaizen Institute')
    st.markdown('''<a href="http://ru.kaizen.com/"><img src='https://www.kaizen.com/images/kaizen_logo.png' style="width: 50%; margin-left: 25%; margin-right: 25%; text-align: center;"></a><p>''', unsafe_allow_html=True)
    st.title("Определи свой потенциал")
    val_list = ['Рубль', 'Доллар США']
    val_0 = st.radio("Выберите валюту:", val_list, index=0)
    if val_0 == 'Рубль':
        val = 'млн₽'
    else:
        val = 'млн$'
    st.subheader('Нам необходима информация, чтобы спрогнозировать ваши показатели прибыли')

    industry = st.radio("Ваша отрасль:", industry_list)
    market_state = st.radio("Охарактеризуйте состояние сектора, в котором вы работаете:", gro_state_list)
    revenue = st.number_input(f"Какова ваша выручка, {val} в год:", value=0)
    margin = st.slider("Какова ваша маржа операционной прибыли, % к выручке:", -20, 80, 0, 2)
    growth = st.slider("Каков ваш среднегодовой рост выручки в % за последние 3 года", -20, 100, 0, 5)
    lost = lost_profit(industry, market_state, revenue, margin, growth)
    lost = pd.Series(lost).round(0)
    st.title("Результат")
    col1, col2, col3 = st.columns(3)
    proc_lost_rev = - (lost[0] / revenue * 100)
    proc_lost_1 = - (lost[1] / revenue * 100)
    proc_lost_2 = - (lost[2] / revenue * 100)
    
    col1.metric("ОБЩАЯ упущенная прибыль", f'{lost[0]:.0f} {val}', f'{proc_lost_rev:.0f}% выручки')
    col2.metric("Потери прибыли в ОПЕРАЦИЯХ", f'{lost[1]:.0f} {val}', f'{proc_lost_1:.0f}% выручки')
    col3.metric("Потери прибыли в РОСТЕ", f'{lost[2]:.0f} {val}', f'{proc_lost_2:.0f}% выручки')
    # st.markdown(f'Предварительная оценка разницы в прибыли при сравнении с компаниями, реализующими Kaizen: <b>{lost[0]:.0f}</b> {val} <p> в том числе: <p>Операционная Дельта (прибыль упущенная в операционной деятельности): <b>{lost[1]:.0f}</b> {val} <p> Дельта Роста (прибыль упущенная из-за отсутствия роста): <b>{lost[2]:.0f}</b> {val}', unsafe_allow_html=True)
    
    if revenue != 0:
        fig = go.Figure(go.Waterfall(name="20", orientation="v", measure=["absolute", "relative", "relative"],
                                     x=["Общая дельта", "Операционная дельта", "Дельта роста"],
                                     text=lost, y=[lost[0], -lost[1], -lost[2]],
                                     textposition="auto",
                                     connector={"line": {"color": "rgb(63, 63, 63)"}}))
        fig.update_layout(title = f"Потери прибыли, {val} в год")
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
        st.title("Оцените следующие аспекты вашей компании")
        st.subheader("Операционные аспекты:")
        anw_0 = st.radio(df_deltas_breakdown.index[0], answers_list, index=0)
        anw_1 = st.radio(df_deltas_breakdown.index[1], answers_list, index=0)
        anw_2 = st.radio(df_deltas_breakdown.index[2], answers_list, index=0)
        anw_3 = st.radio(df_deltas_breakdown.index[3], answers_list, index=0)
        anw_4 = st.radio(df_deltas_breakdown.index[4], answers_list, index=0)
        anw_5 = st.radio(df_deltas_breakdown.index[5], answers_list, index=0)
        anw_6 = st.radio(df_deltas_breakdown.index[6], answers_list, index=0)
        anw_7 = st.radio(df_deltas_breakdown.index[7], answers_list, index=0)
        anw_8 = st.radio(df_deltas_breakdown.index[8], answers_list, index=0)
        anw_9 = st.radio(df_deltas_breakdown.index[9], answers_list, index=0)
        anw_10 = st.radio(df_deltas_breakdown.index[10], answers_list, index=0)
        st.subheader("Аспекты роста:")
        anw_11 = st.radio(df_deltas_breakdown.index[11], answers_list, index=0)
        anw_12 = st.radio(df_deltas_breakdown.index[12], answers_list, index=0)
        anw_13 = st.radio(df_deltas_breakdown.index[13], answers_list, index=0)
        anw_14 = st.radio(df_deltas_breakdown.index[14], answers_list, index=0)
        anw_15 = st.radio(df_deltas_breakdown.index[15], answers_list, index=0)
        anw_16 = st.radio(df_deltas_breakdown.index[16], answers_list, index=0)    

        lost_oper_full = break_down(anw_0, anw_1, anw_2, anw_3, anw_4, anw_5, anw_6, anw_7, anw_8, anw_9, anw_10) * lost[1]
        lost_growth_full = break_down_g(anw_11, anw_12, anw_13, anw_14, anw_15, anw_16) * lost[2]
        lost_oper = lost_oper_full[lost_oper_full > 0]
        lost_growth = lost_growth_full[lost_growth_full > 0]
        
        lost_oper_fin = pd.DataFrame(lost_oper)
        lost_oper_fin['o_g'] = np.repeat('Операции', len(lost_oper_fin))
        lost_oper_fin['Ответ'] = lost_oper_fin.index
        lost_oper_fin.columns = ['Оценка', 'Направление', 'Аспект']

        lost_growth_fin = pd.DataFrame(lost_growth)
        lost_growth_fin['o_g'] = np.repeat('Рост', len(lost_growth_fin))
        lost_growth_fin['Ответ'] = lost_growth_fin.index
        lost_growth_fin.columns = ['Оценка', 'Направление', 'Аспект']

        lost_total = lost_oper_fin.append(lost_growth_fin)
        lost_total = lost_total.sort_values("Оценка", ascending=False)        
        if len(lost_oper) != 0:
            fig_1 = px.bar(lost_total, y='Оценка', x='Аспект', text='Оценка', color='Направление')
            fig_1.update_traces(texttemplate='%{text:.2s}', textposition='auto')
            fig_1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title = "Разбивка упущенной прибыли", yaxis_title=f"{val} упущенной прибыли", xaxis_title="Факторы Kaizen", showlegend=False)
            fig_1.update_xaxes(categoryorder='total descending')
            st.plotly_chart(fig_1, use_container_width=True, sharing="streamlit")
            st.dataframe(lost_total.drop('Аспект', axis='columns').sort_values("Оценка", ascending=False))

#        if len(lost_oper) != 0:
#            fig_2 = px.bar(lost_oper, y=0, x=lost_oper.index)
#            fig_2.update_layout(title = "Разбивка операционной дельты", yaxis_title=f"{val} упущенной прибыли", xaxis_title="Операционные факторы Kaizen")
#            st.plotly_chart(fig_2, use_container_width=True, sharing="streamlit")
#
#        if len(lost_growth) != 0:
#            fig_3 = px.bar(lost_growth, y=0, x=lost_growth.index)
#            fig_3.update_layout(title = "Разбивка дельты роста", yaxis_title=f"{val} упущенной прибыли", xaxis_title="Факторы Роста Kaizen")
#            st.plotly_chart(fig_3, use_container_width=True, sharing="streamlit")
#        if len(lost_oper.append(lost_growth)) != 0:
#            lost_oper_fin = pd.DataFrame(lost_oper)
#            lost_oper_fin['o_g'] = np.repeat('Операции', len(lost_oper_fin))
#            lost_oper_fin['Ответ'] = lost_oper_fin.index
#            lost_oper_fin.columns = ['Оценка', 'Направление', 'Аспект']
#
#            lost_growth_fin = pd.DataFrame(lost_growth)
#            lost_growth_fin['o_g'] = np.repeat('Рост', len(lost_growth_fin))
#            lost_growth_fin['Ответ'] = lost_growth_fin.index
#            lost_growth_fin.columns = ['Оценка', 'Направление', 'Аспект']
#            
#            lost_total = lost_oper_fin.append(lost_growth_fin)
#            fig_4 = px.sunburst(lost_total, path=['Направление', 'Аспект'], values='Оценка', maxdepth=2)
#            fig_4.update_layout(title = "Разбивка общей дельты")
#            st.plotly_chart(fig_4, use_container_width=True, sharing="streamlit")

# Вызываем приложение
show_predict_page()
