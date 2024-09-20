import streamlit as st
import sqlite3
import pandas as pd

# メンテナンス箇所（staff, backnumber）
staff = [205788, 240192, 270312, 301833, 317098, 330264, 353019, 364444, 373966, 382841,
        396389, 402281, 428973, 462187, 462217, 466654, 466689, 468096, 494569, 501085, 
        504513, 513954, 529079, 539619, 539724, 559334, 559423, 559431, 559466, 570249, 
        571334, 587222, 587249, 587257, 587273, 601489, 601519, 601527, 601535, 606626, 
        624535, 627712, 640298, 640301, 640328, 640336, 640344, 647543, 653608, 653624, 
        653632, 653659, 665746, 665754, 665762, 665789, 665797, 665819, 703125, 703150, 
        703168, 703176, 704121, 704172, 717380, 717398, 717401, 717410, 717428, 728934,
        728942, 728977, 728985, 728993, 743712, 743739, 743747, 743755, 743763, 747785,
        760633, 760641, 760650
        ]
backnumber = ['2024.08-09月号']

st.title('ADI')
st.write('---')
st.write('✓[2024年度](https://drive.google.com/drive/folders/1xPIKiFwlnCPvb-Jp8tvmU-1baTgIM6ka?usp=sharing)')
st.write('✓[2023年度](https://drive.google.com/drive/folders/1LiWky3OD6VmAsYeiGiKY5YIqmoakwBw0?usp=sharing)')
st.write('---')
st.write('✓[採用・中止薬一覧](https://drive.google.com/drive/folders/1rjZ3mokmV5k1jAMdvd5eJGBkYMPfGqRS?usp=sharing)'
         +'（どの薬品がいつ採用・中止になったのか確認できます）')
st.write('---')
submitter = st.checkbox('既読の報告')
if submitter:
    with st.form(key='form1'):
        adi = st.selectbox('確認したADIを選択してください', backnumber)
        staff_id = st.number_input('職員IDを入力してください', step=1)
        btn = st.form_submit_button(label='送信')
    if btn:
        db = sqlite3.connect('kidoku_check.db')
        cur = db.cursor()
        cur.execute("INSERT INTO kidoku (ADI, ID) VALUES (?, ?)", (adi, staff_id))
        db.commit()
        cur.close()
        db.close()
        st.write('登録しました')

st.write('---')
check = st.checkbox('未読確認')
if check:
    db = sqlite3.connect('kidoku_check.db')
    # SQLクエリを使用しデータを取得
    query = "SELECT * FROM kidoku"
    df = pd.read_sql_query(query, db)
    db.close()

    for adi in backnumber:
        dfq = df.query(f"ADI == '{adi}'")
        kidoku = dfq['ID'].unique().tolist()
        midoku = sorted(list(set(staff) - set(kidoku)))
        if len(midoku) == 0:
            st.write('---')
            st.write(f'■{adi}')
            st.write('Complete !')
        else:
            st.write('---')
            st.write(f'■{adi}未読者')
            st.write(f'{midoku}')
    st.write('---')

