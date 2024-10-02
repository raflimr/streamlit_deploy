import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
from geodatasets import get_path


 
st.title('Dashboard E-Commerce Public Dataset')
orders_category = pd.read_csv('../data/orders_category_filtered.csv')
orders_category['order_purchase_timestamp'] = pd.to_datetime(orders_category['order_purchase_timestamp'])
orders_category.info()

orders_payment = pd.read_csv('../data/orders_payment.csv')
orders_payment['order_purchase_timestamp'] = pd.to_datetime(orders_payment['order_purchase_timestamp'])
orders_payment.info()

rfm_analysis = pd.read_csv('../data/rfm_analysis.csv')
rfm_analysis.info()

geospatial_analysis = pd.read_csv('../data/geospatial_analysis.csv')

 
with st.sidebar:
    st.title("Submission Belajar Analisis Data Dengan Python")
    st.image("https://dicoding-web-img.sgp1.digitaloceanspaces.com/original/jobs/dos:company_logo_dicoding_indonesia_050423140704.jpg")
    
    st.subheader("Name: Rafli Muhamad Ridhwan")

with st.container():
     # Group data by year and quarter
    df_grouped = orders_category.groupby([
        orders_category['order_purchase_timestamp'].dt.year,
        orders_category['order_purchase_timestamp'].dt.quarter
    ])['order_id'].count().unstack()

    # Buat clustered bar chart dengan gap
    fig, ax = plt.subplots(figsize=(10, 6))
    df_grouped.plot(kind='bar', ax=ax, width=0.8)
    plt.title('Perbandingan Jumlah Pesanan pada Tahun 2017 dan 2018 pada Setiap Kuartal')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Pesanan')
    plt.xticks(rotation=0)
    plt.legend(title='Kuartal')
    plt.ylim(0, 25000)

    # Tambahkan label di atas setiap bar
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Tambahkan jarak antar bar
    plt.subplots_adjust(wspace=0.2)

    # Tampilkan grafik di Streamlit
    st.pyplot(fig)
   
    with st.expander("See explanation"):
        st.write("Dapat dilihat pada grafik perbandingan jumlah pesanan pada tahun 2017 dan 2018 pada setiap kuartal, bahwa jumlah pesananan pada tahun berikutnya tepatnya di 2018 mengalami peningkatan dibandingkan tahun sebelumnya")
 
    # Filter data untuk tahun 2018 dan hapus tipe pembayaran 'not_defined'
    df_payment_2018 = orders_payment[
        (orders_payment['order_purchase_timestamp'].dt.year == 2018) &
        (orders_payment['payment_type'] != 'not_defined')
    ]

    # Group by payment_type dan hitung jumlah pesanan
    df_payment_type_grouped = df_payment_2018.groupby('payment_type')['order_id'].count()

    # Urutkan dari terendah ke tertinggi
    df_payment_type_grouped = df_payment_type_grouped.sort_values()

    # Buat grafik horizontal bar chart dengan color gradient
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(df_payment_type_grouped)))  # Warna dengan colormap
    df_payment_type_grouped.plot(kind='barh', ax=ax, color=colors)

    plt.title('Metode Pembayaran Terpopuler Tahun 2018')
    plt.xlabel('Jumlah Pemakaian')
    plt.ylabel('Metode Pembayaran')
    plt.xlim(0, 45000)

    # Tambahkan label nilai di setiap bar
    for i, v in enumerate(df_payment_type_grouped):
        ax.text(v, i, str(v), va='center')

    st.pyplot(fig)
    with st.expander("See explanation"):
        st.write("Dapat dilihat pada grafik metode pembayaran terpopuler pada tahun 2018 bahwa credit card menjadi pemakaian tertinggi dalam metode pembayaran  kemudian dilanjut oleh boleto dan diikuti oleh voucher serta diakhiri oleh debit_card")
    
    st.subheader("RFM Analysis")
    # Membuat subplot dengan 1 baris dan 3 kolom
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Warna untuk bar chart
    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

    # Bar chart pertama: Recency
    sns.barplot(y="recency", x="customer_id_rename", 
                data=rfm_analysis.sort_values(by="recency", ascending=True).head(5), 
                palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=15)

    # Bar chart kedua: Frequency
    sns.barplot(y="frequency", x="customer_id_rename", 
                data=rfm_analysis.sort_values(by="frequency", ascending=False).head(5), 
                palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Bar chart ketiga: Monetary
    sns.barplot(y="monetary", x="customer_id_rename", 
                data=rfm_analysis.sort_values(by="monetary", ascending=False).head(5), 
                palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Menambahkan judul untuk seluruh plot
    plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)
    with st.expander("See explanation"):
        st.write("Salah satu teknik analisis lanjutan yang melakukan pengelompokkan user atau pelanggan berdasarkan tiga faktor utama yaitu Recency, Frequency, dan Monetary atau sering disingkat RFM analysis. Dapat dilihat bahwa berdasarkan faktor recency didapatkan ID15596 merupakan pelanggan yang aktif dalam menggunakan e-commerce, untuk faktor frequency setara , sedangkan faktor monetary didapatkan oleh id8547")
    
    st.subheader("Geospatial Analysis")
    gdf = gpd.GeoDataFrame(
    geospatial_analysis, geometry=gpd.points_from_xy(geospatial_analysis.geolocation_lng, geospatial_analysis.geolocation_lat), crs="EPSG:4326"
    )

    # Baca peta dunia dari GeoPandas datasets
    shapefile_path = "../data/naturalearth_land/ne_110m_land.shp"
    world = gpd.read_file(shapefile_path)

    # Membatasi peta hanya untuk Brazil (koordinat untuk clip)
    ax = world.cx[-74:-34, -33:5].plot(color="white", edgecolor="black")

    # Plot GeoDataFrame (titik data)
    gdf.plot(ax=ax, color="red")

    # Menampilkan visualisasi di Streamlit
    st.pyplot(plt)
