#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from asyncore import write
from operator import index
from turtle import right
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='أداء مبيعات منافذ',
                   page_icon=":Bar_Chart:",
                   layout="wide")
st.header('أداء مبيعات منافذ لعام 2021')
st.markdown(' تم إنشاء الصفحة لغرض المقابلة الشخصية والأرقام المعروضه غير حقيقيه وسيتم حذف الصفحة قريبَا')
st.markdown("##")
image= Image.open('banner.jfif')
st.image(image,caption='جميع الحقوق محفوظه لنجم | منافذ')
### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:E',
                   header=3)

df.dropna(inplace=True)


# --- STREAMLIT SELECTION
Company = df['أسم الشركة'].unique().tolist()
Port = df['المنفذ'].unique().tolist()
Sales_Quarter = df['الربع'].unique().tolist()

Quarter_selection = st.multiselect("يرجى إختيار الربع السنوي بالأسفل (ملاحظة: للمزيد من الخيارات يرجى الضغط على السهم الموجود بأعلى الخانة اليسرى)",
                                    Sales_Quarter,
                                    default=Sales_Quarter)

company_selection = st.sidebar.multiselect(':أسم الشركة',
                                    Company,
                                    default=Company)

Port_selection = st.sidebar.multiselect(':المنفذ',
                                    Port,
                                    default=Port)

# --- FILTER DATAFRAME BASED ON SELECTION


# --- GROUP DATAFRAME AFTER SELECTION
mask = (df['أسم الشركة'].isin(company_selection)) & (df['الربع'].isin(Quarter_selection)) & (df['المنفذ'].isin(Port_selection))
df_grouped = df[mask].groupby(by=['أسم الشركة']).sum()[['المبيعات']]
df_grouped = df_grouped.rename(columns={'أسم الشركة': 'الشركة'})
df_grouped = df_grouped.reset_index()
##### Raw Data 
df_quarter = df[mask].groupby(by=['الربع']).sum()[['المبيعات']]
df_quarter = df_quarter.rename(columns={'المبيعات': ''})


total_sales = int(df[mask].sum()[['المبيعات']])
st.markdown("__________________________________")

st.write('بحسب إختياراتك فإن')
st.write('**مجموع مبيعات منافع هي**',f"**: {total_sales:,}** ", '**ريال سعودي**')


st.markdown("__________________________________")
st.markdown("##")
######################## مبيعات بالربع خطي
st.markdown(":المبيعات حسب كل ربع")
st.line_chart(df_quarter)
########################## تفاصيل
st.markdown("__________________________________")
st.markdown("##")
df_grouped2 = df[mask].groupby(by=['أسم الشركة','الربع','المنفذ']).sum()[['المبيعات']]
df_grouped2 = df_grouped2.rename(columns={'أسم الشركة': 'الشركة'})
df_grouped2 = df_grouped2.reset_index()
st.markdown(":تفاصيل المبيعات")
st.dataframe(df_grouped2)
# --- PLOT BAR CHART
st.markdown("__________________________________")
st.markdown("##")
st.markdown('مبيعات الشركات')
bar_chart = px.bar(df_grouped,
                   title='',
                   x='المبيعات',
                   y='أسم الشركة',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)


# --- PLOT PIE CHART
st.markdown("__________________________________")
st.markdown("##")
df_grouped3 = df[mask].groupby(by=['المنفذ']).sum()[['المبيعات']]
#df_grouped3 = df_grouped3.rename(columns={'أسم الشركة': 'الشركة'})
df_grouped3 = df_grouped3.reset_index()
st.markdown('مبيعات المنافذ')
pie_chart = px.pie(df_grouped3,
                   names='المنفذ',
                values='المبيعات')
st.plotly_chart(pie_chart)

st.markdown("__________________________________")
st.markdown("##")
st.markdown('تم تطوير هذه الصفحة من قبل طلال العيار')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            h1 {text-align: center;}
            p {text-align: center;}
            div {text-align: center;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)