import selenium
from selenium.webdriver.common.by import By                             # by untuk mendapatkan elemen menggunakan pemilih              
from selenium import webdriver as wb                                    # wb untuk menjalankan driver
from selenium.webdriver.support import expected_conditions as EC        # EC untuk mengatasi kondisi pengecualian
from selenium.webdriver.support.ui import WebDriverWait as wait         # wait untuk mengatasi kondisi menunggu
import pandas as pd                                                     # pd untuk mengekspor data
from tqdm import tqdm                                                   # tqdm untuk visualisasi proses perulangan
from selenium.webdriver.common.keys import Keys                         # Kunci sebagai prosedur menggunakan keyboard
import datetime

# Inisialisasi Driver Chrome untuk menjalankan simulasi dan mendapatkan URL
driver = wb.Chrome()
driver.get('https://www.tokopedia.com/')

driver.implicitly_wait(5)

# Inisialisasi input untuk mendapatkan kata kunci dan halaman
keywords = input("Keywords: ")
pages = int(input("Pages: "))

# Inisialisasi pencarian untuk mencari berdasarkan kata kunci dan tekan tombol ENTER
search = driver.find_element(By.XPATH, '//*[@id="header-main-wrapper"]/div[2]/div[2]/div/div/div/div/input')
search.send_keys(keywords)
search.send_keys(Keys.ENTER)

driver.implicitly_wait(5)

# Inisialisasi product_data untuk menyimpan data produk sebagai sebuah array
product_data = []

# Definisikan scrolling untuk scroll halaman
def scrolling():
    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .01

# Definisikan reverse_scrolling untuk membalikkan scroll
def reverse_scrolling():
    body = driver.find_element(By.TAG_NAME, 'body')

    i = 0
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i += 1
        if i >= 25:
            break

# Definisikan extract_data untuk mengekstrak data menggunakan driver
def extract_data(driver):

    driver.implicitly_wait(20)
    driver.refresh()
    scrolling()

    # Mendapatkan item data menggunakan pemilih XPATH, tunggu selama 30 detik jika melebihi batas waktu akan memunculkan pengecualian
    data_item = wait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "css-12sieg3")]')))

    # Jika item data tidak mencapai 80, maka proses pengambilan data akan diulang
    if len(data_item) != 80:
        driver.refresh()
        driver.implicitly_wait(10)
        scrolling()

        data_item = wait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "css-12sieg3")]')))

    # loop untuk mengekstrak data atribut menggunakan pemilih XPATH
    for item in tqdm(data_item):

        element = wait(item, 10).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-y5gcsw"]')))

        name = element.find_element(By.XPATH, './/div[@class="prd_link-product-name css-3um8ox"]').text
        price = element.find_element(By.XPATH, './/div[@class="prd_link-product-price css-1ksb19c"]').text
        location = element.find_element(By.XPATH, './/span[@class="prd_link-shop-loc css-1kdc32b flip"]').text
        try:
            rating = element.find_element(By.XPATH, './/span[@class="prd_rating-average-text css-t70v7i"]').text
        except:
            rating = None

        try:
            sold = element.find_element(By.XPATH, './/span[@class="prd_label-integrity css-1duhs3e"]').text
        except:
            sold = None    

        details_link = element.find_element(By.XPATH, './/div[@class="css-1f2quy8"]/a').get_property('href')

        # impan data ke dalam dictionary.
        data = {
            'name': name,
            'price': price,
            'location': location,
            'rating': rating,
            'sold': sold,
            'details_link': details_link
        }

        # Tambahkan data ke product_data
        product_data.append(data)

stop = 1

# loop untuk proses scraping 
while stop <= pages:
    extract_data(driver)

    # "Dapatkan elemen tombol selanjutnya menggunakan pemilih CSS, tunggu hingga 60 detik, jika melebihi waktu tersebut, akan menghasilkan pengecualian
    try:
        next_page = wait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Laman berikutnya"]')))
    except:
        driver.refresh()
        scrolling()
        reverse_scrolling()
        scrolling()
        next_page = wait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Laman berikutnya"]')))
    
    # Klik tombol halaman berikutnya
    try:
        next_page.click()
    except:
        break

    stop += 1
    
df = pd.DataFrame(product_data)

now = datetime.datetime.today().strftime('%d-%m-%Y')

# Ekspor data ke dalam format CSV 
df.to_csv(f'sample_data_{now}.csv', index=False)
