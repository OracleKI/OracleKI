import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL situs web yang akan di-scrape
url = 'https://contoh.com/situs-web-anda'

# Mengambil data HTML dari situs web
response = requests.get(url)
html = response.text

# Membuat objek BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Inisialisasi list untuk menyimpan data
data_barang = []

# Mencari elemen-elemen HTML yang berisi informasi barang
barang_items = soup.find_all('div', class_='barang-item')  # Ganti dengan kelas yang sesuai di situs web Anda

for item in barang_items:
    nama_barang = item.find('h2', class_='nama-barang').text  # Ganti dengan kelas yang sesuai
    deskripsi_barang = item.find('p', class_='deskripsi-barang').text  # Ganti dengan kelas yang sesuai
    harga_barang = item.find('span', class_='harga-barang').text  # Ganti dengan kelas yang sesuai
    penjualan_barang = item.find('span', class_='penjualan-barang').text  # Ganti dengan kelas yang sesuai
    gambar_barang = item.find('img')['src']  # Ganti dengan atribut yang sesuai

    data_barang.append({
        'Nama Barang': nama_barang,
        'Deskripsi Barang': deskripsi_barang,
        'Harga Barang': harga_barang,
        'Penjualan Barang': penjualan_barang,
        'Gambar Barang': gambar_barang
    })

# Membuat DataFrame dari data
df = pd.DataFrame(data_barang)

# Menyimpan data ke dalam file Excel
df.to_excel('data_barang.xlsx', index=False, engine='openpyxl')
