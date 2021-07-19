import csv
import requests
import time
from bs4 import BeautifulSoup
from soupsieve import select
import itertools


# リクナビ製造業、半導体URLにアクセス
res = requests.get('https://job.rikunabi.com/2022/search/company/result/?fw=&ms=0&b=8&b=9&b=10&b=7&b=32&b=31&b=33&b=14&b=15&b=11&b=13&b=16&b=21&b=20&b=12&b=18&b=19&b=17&b=22&b=3&b=4&b=6&b=5&b=30&b=29&b=27&b=28&b=23&b=25&b=26&b=24&b=2&b=1&b=34&kk=0&k=48&aot=&apr=&cwr=&cmr=&rry=3&rr=&ggr=1&gr=&awy=&wer=&wmr=&tt=34')
soup = BeautifulSoup(res.text, 'lxml')

time.sleep(3)

# ベースとなるURL
base_url = "https://job.rikunabi.com/"

# 空の配列作成
comp_a = []

# 企業個別リンク取得
comp_a.append(soup.select(".ts-h-search-cassetteTitle a[href]"))

# ページhref取得
while soup.select(".ts-h-search-pipePagerItem")[6].select_one("a"):
  page_a = soup.select(".ts-h-search-pipePagerItem")[6].select_one("a")
  page_href = page_a.get("href")
  page_url = base_url + page_href
  res = requests.get(page_url)
  soup = BeautifulSoup(res.text, 'lxml')
  comp_a.append(soup.select(".ts-h-search-cassetteTitle a[href]"))
  if soup.select(".ts-h-search-pipePagerItem")[6].select_one("a") == None:
    break


# # 空の配列作成
comp_hrefs = []
comp_urls = []
csv_datas = [['No', '企業名', '業種(大分類)', '業種(小分類)', '採用情報URL']]

# # 取得した企業の個別リンク分処理を繰り返す(二次元配列→一次元化)
for comp_href in list(itertools.chain.from_iterable(comp_a)):
#   # 配列にhref追加
  comp_hrefs.append(comp_href.get("href"))

for comp_href in comp_hrefs:
#   # 企業個別URL生成
  comp_urls.append(base_url + comp_href)

i = 1

for comp_url in comp_urls:
  comp_url1 = requests.get(comp_url)
  soup = BeautifulSoup(comp_url1.text, 'lxml')
  # 企業名、業種、採用情報URL取得
  comp_name = soup.select_one(".ts-h-company-mainTitle a").text
  comp_type_l = soup.select_one(".ts-h-company-dataTable-main").text 
  comp_type_m = soup.select_one(".ts-h-company-dataTable-sub").text if soup.select_one(".ts-h-company-dataTable-sub") else ""
  # comp_type_m = 1
  comp_offer_url = (base_url + comp_href + 'employ/')
  csv_datas.append([i, comp_name, comp_type_l, comp_type_m, comp_offer_url])
  print(comp_name)
  print("--------------------------------------")
  i += 1



# # csvファイルを新規作成、取得した企業名等のデータを書き込む
f = open("rikunabi_data.csv", "w")
csvf = csv.writer(f)
for csv_data in csv_datas:
  csvf.writerow(csv_data)
f.close



