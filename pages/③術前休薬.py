import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st
from PIL import Image

st.title('休薬関連 検索★★テストページ★★')

st.write('===== データベース使用上の注意 =====')
st.write('休薬関連情報は、休薬規約を基に作成したデータベースです。  \n'
        +'一部、参考情報として過去の対応事例を参考に出血リスクを表示しています。  \n'
        +'患者ごとに対応が異なる場合があります。カルテ内容を十分に確認してください。  \n'
        +'※このページからは情報の修正はできません。修正が必要な場合は管理担当者へ連絡してください。' 
        )
st.write('検索条件を選択してください。')

sentaku=st.radio("検索条件",["術式","薬剤名"], 
                 index=0, 
                 horizontal=True
                 )
kensaku1 = st.text_input('検索用語（1単語のみ）を入力してください。  ※半角・全角は区別されます')
btn1 = st.button('検索')

if sentaku == '術式':
    if btn1:
        kensaku1 = '%' + kensaku1 + '%'
        db = sqlite3.connect('kyuyaku.db')
        cur = db.cursor()    

        cur.execute("SELECT * FROM k_data WHERE category LIKE ? OR operation LIKE ? OR abbreviations LIKE ? OR risk1 LIKE ? OR risk2 LIKE ? OR anesthesia LIKE ? OR meal LIKE ? OR contrast LIKE ? OR others LIKE ?", 
                    [kensaku1, kensaku1, kensaku1, kensaku1, kensaku1, kensaku1, kensaku1, kensaku1, kensaku1]
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
            for i in range(len(data)):
                st.write(f'【診療科】{data[i][1]}')
                st.write(f'【術式】{data[i][2]}')
                st.write(f'【略語】{data[i][3]}')
                if data[i][4] == '―':
                    st.write(f'【出血リスク(内視鏡)】{data[i][5]}')
                else:
                    st.write(f'【出血リスク】{data[i][4]}')
                st.write(f'【麻酔】{data[i][6]}')
                st.write(f'【欠食】{data[i][7]}')
                st.write(f'【造影剤】{data[i][8]}')
                st.write(f'【その他注意事項】{data[i][9]}')
                st.write('-------------------------------------------------------------------')
        st.write('')
        
elif sentaku == '薬剤名':
    if btn1:
        kensaku1 = '%' + kensaku1 + '%'
        db = sqlite3.connect('yakuzai.db')
        cur = db.cursor()    

        cur.execute("SELECT * FROM y_data WHERE category LIKE ? OR name LIKE ? OR generic LIKE ? OR adupt2 LIKE ?",
                    [kensaku1, kensaku1, kensaku1, kensaku1]
                    )
        data1 = cur.fetchall()
        cur.close()
        db.close()
        
        if len(data1) == 0:
            st.write('-------------------------------------------------------------------')
            st.write('休薬関連情報：該当データなし')
            st.write('-------------------------------------------------------------------')
        else:
            st.write(f'休薬関連情報：{len(data1)}')
            st.write('＊例外あり。詳細は休薬規約を参照して下さい。  \n※留意点あり。詳細は休薬規約を参照して下さい。')
            st.write('-------------------------------------------------------------------')
            for i in range(len(data1)):
                st.write(f'【分類】{data1[i][1]}' )
                st.write(f'【採用】{data1[i][2]}')
                st.write(f'【商品名】{data1[i][3]}')
                st.write(f'【一般名】{data1[i][4]}')
                st.write(f'【当院採用薬】{data1[i][5]}')
                st.write(f'【手術および抜歯を含む侵襲的医療行為出血リスク（高）】  \n{data1[i][6]}')
                st.write(f'【手術および抜歯を含む侵襲的医療行為出血リスク（中）】  \n{data1[i][7]}')
                st.write(f'【手術および抜歯を含む侵襲的医療行為出血リスク（低）】  \n{data1[i][8]}')
                st.write(f'【脊髄くも膜下麻酔、硬膜外麻酔、深部神経ブロック】  \n{data1[i][9]}')
                st.write(f'【消化器内視鏡検査および治療出血リスク（高）】  \n{data1[i][10]}')
                st.write(f'【消化器内視鏡検査および治療出血リスク（低）】  \n{data1[i][11]}')
                st.write(f'【ヨード造影剤を用いた検査】  \n{data1[i][12]}')
                st.write(f'【その他】  \n{data1[i][13]}')
                st.write('-------------------------------------------------------------------')
        st.write('')
          
elif sentaku == '':
    if btn1:
        st.write('※検索条件「術式」または「薬剤名」を一つ選択してください。※')