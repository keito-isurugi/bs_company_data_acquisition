import csv
import requests
import time
from bs4 import BeautifulSoup
from soupsieve import select
import itertools


# emidasにアクセス
res = requests.get('https://www.nc-net.or.jp/search/search/?w=%E6%B5%B7%E5%A4%96&x=0&y=0&sxf=&sxt=&syf=&syt=&szf=&szt=&en=&es=&eq=&e=&pno=1')
soup = BeautifulSoup(res.content, 'lxml')

time.sleep(3)

# ベースとなるURL
base_url = "https://www.nc-net.or.jp/"

# 空の配列作成
comp_a = []

# 企業個別リンク取得
comp_a.append(soup.select(".ttl-h3-03 a[href]"))


# ページhref取得
for i in range(70):
  pages = soup.select('.nav-page-skip-01 li a[href]')
  next_page = pages[-1].get("href")
  res = requests.get(base_url + next_page)
  soup = BeautifulSoup(res.content, 'lxml', from_encoding='utf-8')
  comp_a.append(soup.select(".ttl-h3-03 a[href]"))

# # 空の配列作成
comp_hrefs = []
comp_urls = []
csv_datas = [['No', '企業名', '主要三品目①', '主要三品目②', '主要三品目③', '企業HP']]

# # 取得した企業の個別リンク分処理を繰り返す(二次元配列→一次元化)
for comp_href in list(itertools.chain.from_iterable(comp_a)):
# #   # 配列にhref追加
  comp_hrefs.append(comp_href.get("href"))

for comp_href in comp_hrefs:
# #   # 企業個別URL生成
  comp_urls.append(base_url + comp_href)

i = 1


for comp_url in comp_urls:
  comp_url1 = requests.get(comp_url)
  soup = BeautifulSoup(comp_url1.content, 'lxml', from_encoding='utf-8')
  # 企業名、業種、採用情報URL取得
  comp_na = soup.select(".tbl-data-01 td")[0].text if soup.select(".tbl-data-01 td") else ""
  target = '('
  idx = comp_na.find(target)
  comp_name = comp_na[:idx].strip().replace('　', '')
  # print(comp_name)
  # print("------------------------")
  if soup.select(".list-dot-01 li"):
    main_item = soup.select(".list-dot-01 li") 
    if len(main_item) > 0: 
      main_item1 = main_item[0].text 
      if len(main_item) > 1:
        main_item2 = main_item[1].text 
        if len(main_item) > 2: 
          main_item3 = main_item[2].text 
        else:
          ""
      else:
        ""
    else:
      ""
  else:
    ""



  comp_a = soup.select_one(".ttl-h1-02 a") if soup.select_one(".ttl-h1-02 a") else "" 
  comp_href = comp_a["href"] if soup.select_one(".ttl-h1-02 a") else ""
  csv_datas.append([i, comp_name, main_item1, main_item2, main_item3, comp_url])
  # print(comp_name)
  i += 1



# # # csvファイルを新規作成、取得した企業名等のデータを書き込む
f = open("emidas_data.csv", "w")
csvf = csv.writer(f)
for csv_data in csv_datas:
  csvf.writerow(csv_data)
f.close



