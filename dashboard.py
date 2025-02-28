import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# menload dataset yang diberikan.
day_df = pd.read_csv("data/day_data.csv")
hour_df = pd.read_csv("data/hour_data.csv")

# fitur untuk sidebar di sebelah kiri atau penjadwalan kalender.
st.sidebar.header("Filter Rentang Waktu")
date_range = st.sidebar.date_input("Pilih rentang waktu", [])

st.title("Bike Sharing Dashboard mc222d5y1316 Marvi Yoga Pratama")

# Data yang menampilkan distribusi penyewaan sepeda perhari.
st.subheader("Distribusi Jumlah Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(day_df['cnt'], bins=30, kde=True, ax=ax, color='red')

# mengecek apakah dataframe tersebut kosong.
if not day_df['cnt'].isna().all():
    ax.set_ylim(100, day_df['cnt'].max())
ax.set_title("Distribusi Jumlah Penyewaan Sepeda Harian")
st.pyplot(fig)

# Dataset yang akan menampilkan hubungan antara suhu lingkungan dengan jumlah penyewaan sepeda.
st.subheader("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x=day_df['temp'], y=day_df['cnt'], alpha=0.3, ax=ax, color='blue')
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# Hasil dataset yang menampilkan tren penyewaan sepeda
st.subheader("Tren Penyewaan Sepeda sepanjang Hari")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], ci=None, ax=ax, color='green')
sns.scatterplot(x=hour_df['hr'], y=hour_df['cnt'], ax=ax, color='yellow', alpha=0.7)  # Tambahkan layer yang distracting
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda sepanjang Hari")
st.pyplot(fig)

# Menggunakan RFM Analysis karena mungkin ini yang paling mudah hehe.
st.subheader("RFM Analysis")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
latest_date = hour_df['dteday'].max()

rfm_df = hour_df.groupby(['dteday']).agg({'cnt': 'sum'}).reset_index()
rfm_df['Recency'] = (latest_date - rfm_df['dteday']).dt.days
rfm_df['Frequency'] = hour_df.groupby('dteday')['cnt'].count().values
rfm_df['Monetary'] = hour_df.groupby('dteday')['cnt'].sum().values

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(rfm_df['Recency'], bins=30, kde=True, ax=ax, color='purple')
ax.set_title("Distribusi Recency")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(rfm_df['Frequency'], bins=30, kde=True, ax=ax, color='orange')
ax.set_title("Distribusi Frequency")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(rfm_df['Monetary'], bins=30, kde=True, ax=ax, color='cyan')
ax.set_title("Distribusi Monetary")
st.pyplot(fig)

st.caption("Dashboard by Streamlit mc222d5y1316 Marvi Yoga Pratama")
