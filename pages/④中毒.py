import streamlit as st
import sqlite3
db = sqlite3.connect('chudoku.db')
cur = db.cursor()
st.write('★★★テストページ★★★')
st.title('中毒情報')
st.write('★★★テストページ★★★')
kensaku = st.text_input('医薬品名（商品名、一般名もしくは分類名）を入力してください。※半角・全角は区別されます')
btn = st.button('検索')
if btn:
    kensaku = '%'+kensaku+'%'
    cur.execute("SELECT * FROM T_chudoku WHERE category LIKE ? OR general LIKE ? OR major_product LIKE ?", 
            [kensaku, kensaku, kensaku]
            )
    data = cur.fetchall()
    cur.close()
    db.close()

    if len(data) == 0:
        st.write('該当データはありません。')
        st.write('----------------------')
    else:
        st.write(f'該当データ数：{len(data)} 件')
        st.write('----------------------')

        for i in range(0, len(data)):
            st.write(f'[分類]：{data[i][1]}')
            st.write(f'[一般名]：{data[i][2]} ({data[i][3]}など)')
            st.write(f'[中毒量・致死量]：  \n'
                    + f'{data[i][4]}')
            st.write(f'[中毒症状]：  \n'
                    + f'{data[i][5]}')
            st.write(f'[体内動態]：  \n'
                    + f'{data[i][6]}')
            st.write(f'[処置]：  \n'
                    + f'{data[i][7]}  \n'                
                    )
            st.write('----------------------')