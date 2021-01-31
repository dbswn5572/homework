import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.geniedb


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

charts = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for chart in charts:
    rank = chart.select_one('td.number').text[0:2].strip()
    info = chart.select_one('td.info > a.title').text.strip()
    artist = chart.select_one('td.info > a.artist').text.strip()
    # print(rank, info, artist)
    doc = {
        'rank': rank,
        'title': info,
        'artist': artist
    }
    db.charts.insert_one(doc)

#commit again