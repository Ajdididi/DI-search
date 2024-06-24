import streamlit as st

st.title('新聞見出しチェック')
st.write('新聞各社の医療・健康のページから、見出し＋記事へのリンクを取得します。  \n'
         + '※有料記事は閲覧できません。'
         )

from bs4 import BeautifulSoup
import requests
import datetime
import pytz

today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
today = today.strftime('%Y/%m/%d %H:%M')

def mainichi():
    url = 'https://mainichi.jp/medical/'
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    headlines = soup.find_all(class_='articlelist-title')
    titles = []
    for i in range(0, len(headlines)):
        title = headlines[i].text
        titles.append(title)

    stem = 'https://mainichi.jp/'
    urls = []
    links = soup.find_all(class_='articlelist is-tophorizontal js-morelist')
    for i in range(0, len(links)):
        topics = links[i].find_all('a')
        for j in range(0, len(topics)):
            link = topics[j].attrs['href']
            urls.append(stem+link)

    mainichi = []
    for i in range(0, len(titles)):
        if len(titles) == len(urls):
            mainichi.append(f'・[{titles[i]}]({urls[i]})')
        else:
            mainichi.append(f'記事を取得できませんでした。{url}をご参照ください。')
    mainichi = set(mainichi)  #リストの重複を削除
    return mainichi

def yomiuri():
    url = 'https://www.yomiuri.co.jp/medical/'
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    yomiuri = []
    articles = soup.find_all(class_='p-list-item__inner')
    for i in range(len(articles)):
      article = articles[i].find('a')
      text = article.text
      href = article.attrs['href']
      yomiuri.append(f'・[{text}]({url+href})')
    yomiuri = set(yomiuri)  #リストの重複を削除
    return yomiuri

def asahi():
    url = 'https://www.asahi.com/apital/?iref=pc_gnavi'
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")
    art_list = soup.find_all('h4')
    stem = 'https://www.asahi.com/'
    asahi = []
    for i in range(len(art_list)):
        article = art_list[i].text.replace('\n', '')
        url = stem + art_list[i].find('a').attrs['href']
        asahi.append(f'・[{article}]({url})')
    asahi = set(asahi)  #リストの重複を削除
    return asahi

yomiuri_cb = st.checkbox('読売新聞')
if yomiuri_cb:
    st.write(f'{today}取得')
    yomiuri_data = yomiuri()
    for i in yomiuri_data:
        st.write(i)

asahi_cb = st.checkbox('朝日新聞')
if asahi_cb:
    st.write(f'{today}取得')
    asahi_data = asahi()
    for i in asahi_data:
        st.write(i)

mainichi_cb = st.checkbox('毎日新聞')
if mainichi_cb:
    st.write(f'{today}取得')
    mainichi_data = mainichi()
    for i in mainichi_data:
        st.write(f'{i}')