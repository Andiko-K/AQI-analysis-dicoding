import pandas as pd
import dashboar_func as f
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Statistik Polusi Udara pada Stasiun Pengamatan Tiongkok')
pollution_df = pd.read_csv('./dashboard/pollution_data.csv')
pollution_df['date'] = pd.to_datetime(pollution_df['date'])

#Filter date_input untuk komponen sidebar 
min_date = pollution_df['date'].min()
max_date = pollution_df['date'].max()

with st.sidebar:
    
    st.write('# Laporan Kualitas Udara')

    start_date, end_date = st.date_input(
        label = 'Rentang Tanggal',
        min_value=min_date, max_value=max_date,
        value = [min_date,max_date]
    )

##Filter all_df sesuai date_input
main_df = pollution_df[(pollution_df['date'] >= str(start_date)) &
                 (pollution_df['date'] <= str(end_date))]

#Tingkat Polutan
st.write('# Pertumbuhan Tingkat Polutan')
city = st.selectbox(
    label = 'Lokasi Stasiun Pengamatan',
    options = (pollution_df['station'].unique().tolist()))

date_rule = st.radio(
    label = 'Rentang Pengamatan',
    options = ('hari', 'bulan'),
    horizontal = True
)

date_dict = {'hari': 'd', 'bulan': 'm'}
city_val, date_val = city, date_rule
pol1, pol2, pol3, pol4, pol5, pol6 = st.tabs(["PM2.5", "PM10", "SO2", 'NO2', 'CO', 'O3'])
 
with pol1:
    fig_pol_1, ax_pol_1 = f.graph(main_df, date_dict[date_val], 'PM2.5', city_val)
    st.pyplot(fig_pol_1)
 
with pol2:
    fig_pol_2, ax_pol_2 = f.graph(main_df, date_dict[date_val], 'PM10', city_val, 'orange')
    st.pyplot(fig_pol_2)
 
with pol3:
    fig_pol_3, ax_pol_3 = f.graph(main_df, date_dict[date_val], 'SO2', city_val, 'orangered')
    st.pyplot(fig_pol_3)

with pol4:
    fig_pol_4, ax_pol_4 = f.graph(main_df, date_dict[date_val], 'NO2', city_val, 'salmon')
    st.pyplot(fig_pol_4)

with pol5:
    fig_pol_5, ax_pol_5 = f.graph(main_df, date_dict[date_val], 'CO', city_val, 'black')
    st.pyplot(fig_pol_5)

with pol6:
    fig_pol_6, ax_pol_6 = f.graph(main_df, date_dict[date_val], 'O3', city_val, 'crimson')
    st.pyplot(fig_pol_6)


# Polutan berdasarkan Wilayah
st.write('# Kadar Polutan Pada Tiap Wilayah')
reg1, reg2, reg3, reg4, reg5, reg6 = st.tabs(["PM2.5", "PM10", "SO2", 'NO2', 'CO', 'O3'])

with reg1:
    fig_reg_1, ax_reg_1 = f.bar(main_df, 'PM2.5')
    st.pyplot(fig_reg_1)

with reg2:
    fig_reg_2, ax_reg_2 = f.bar(main_df, 'PM10')
    st.pyplot(fig_reg_2)

with reg3:
    fig_reg_3, ax_reg_3 = f.bar(main_df, 'SO2')
    st.pyplot(fig_reg_3)

with reg4:
    fig_reg_4, ax_reg_4 = f.bar(main_df, 'NO2')
    st.pyplot(fig_reg_4)

with reg5:
    fig_reg_5, ax_reg_5 = f.bar(main_df, 'CO')
    st.pyplot(fig_reg_5)

with reg6:
    fig_reg_6, ax_reg_6 = f.bar(main_df, 'O3')
    st.pyplot(fig_reg_6)

#Persentase Konsentrasi Polutan dan AQI
st.write('# Indeks Kualitas Udara')
col1,col2 = st.columns([2,1])

with col1:
    st.write('##### Nilai AQI Tiap Polutan')
    fig_bar_1, ax_bar_1 = f.aqi_bar(main_df)
    st.pyplot(fig_bar_1)

with col2:
    st.write('##### Konsentrasi Polutan (%)')
    fig_pie_1, ax_pie_1 = f.pie_graph(main_df)
    st.pyplot(fig_pie_1)

st.caption('Andiko Putra, 2024')

