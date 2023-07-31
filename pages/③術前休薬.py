import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st
from PIL import Image

st.title('休薬関連 検索')
kensaku = st.text_input('検索ワード（1単語のみ）を入力してください。  ※半角・全角は区別されます')
btn = st.button('検索')

st.write('===== データベース使用上の注意 =====')
st.write('休薬関連情報は、基本的な対応事例を基に作成したデータベースです。  \n'
        +'患者ごとに対応が異なる場合があります。カルテ内容を十分に確認してください。  \n'
        +'※このページからは情報の修正はできません。修正が必要な場合は管理担当者へ連絡してください。' 
        )

if btn:
    kensaku = '%' + kensaku + '%'
    db = sqlite3.connect('kyuyaku.db')
    cur = db.cursor()    

    cur.execute("SELECT * FROM k_data WHERE category LIKE ? OR operation LIKE ? OR abbreviations LIKE ? OR risk1 LIKE ? OR risk2 LIKE ? OR anesthesia LIKE ? OR meal LIKE ? OR contrast LIKE ? OR others LIKE ?", 
                [kensaku, kensaku, kensaku, kensaku, kensaku, kensaku, kensaku, kensaku, kensaku]
                )
    data = cur.fetchall()
    cur.close()
    db.close()

    if len(data) == 0:
        st.write('-------------------------------------------------------------------')
        st.write('休薬関連情報：該当データなし')
        st.write('-------------------------------------------------------------------')
    else:
        st.write(f'休薬関連情報：{len(data)}')
        st.write('-------------------------------------------------------------------')
        for i in range(0, len(data)):
            #tdatetime = datetime.strptime(data[i][0], '%Y-%m-%d %H:%M:%S') 
            #tdate = tdatetime.date().strftime('%Y/%m/%d')
            st.write(f'【診療科】{data[i][1]}' )
            st.write(f'【術式】{data[i][2]}')
            st.write(f'【略語】{data[i][3]}')
            st.write(f'【出血リスク】{data[i][4]}')
            st.write(f'【出血リスク(内視鏡)】{data[i][5]}')
            st.write(f'【麻酔】{data[i][6]}')
            st.write(f'【欠食】{data[i][7]}')
            st.write(f'【造影剤】{data[i][8]}')
            st.write(f'【その他注意事項】{data[i][9]}')
            st.write('-------------------------------------------------------------------')
    st.write('')
    
image = Image.open('yakuzai.png')

st.image(image,use_column_width=True)