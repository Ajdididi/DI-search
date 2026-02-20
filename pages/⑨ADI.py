import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 認証と操作関数
def get_gsheet_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    service_account_info = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                    dict(service_account_info), 
                    scope
                    )
    client = gspread.authorize(credentials)

    return client

def append_to_sheet(adi, staff_id):
    client = get_gsheet_client()
    sheet = client.open('ADI既読チェック').sheet1  # スプレッドシート名と一致させる
    sheet.append_row([adi, str(staff_id)])

def read_sheet():
    client = get_gsheet_client()

    sheet = client.open('ADI既読チェック').sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)


# メンテナンス箇所（staff, backnumber）
staff = [270312, 317098, 331813, 353019, 373966, 382841,
        396389, 402281, 428973, 462187, 462217, 466654, 466689, 468096, 494569, 501085, 
        504513, 513954, 529079, 539619, 539724, 559334, 559423, 559431, 559466, 570249, 
        571334, 587222, 587249, 587257, 587273, 601489, 601519, 601535, 606626, 
        624535, 627712, 640298, 640301, 640328, 640336, 640344, 647543, 653608, 653624, 
        653632, 653659, 665746, 665754, 665762, 665789, 665797, 665819, 703125, 703150, 
        703168, 703176, 704121, 704172, 717380, 717398, 717401, 717410, 717428, 728934,
        728942, 728977, 728985, 728993, 743712, 743739, 743747, 743755, 743763, 747785,
        760633, 760641, 760650, 774278, 774286
        ]
backnumber = ['ADI2026.1・2月号', 'ADI2025.12月号', 'ADI2025.11月号', 'ADI2025.10月号', 'ADI2025.09月号', 'ADI2025.07月号', 'ADI2025.06月号', 'ADI2025.05月号', 
              #'ADItest', 
              #'ADI2025.03月号', 'ADI2025.01-02月号', '2024.12月号', '2024.11月号', '2024.10月号', '2024.08-09月号',
              ]

st.title('ADI')
st.write('---')
st.write('✓[2025年度](https://drive.google.com/drive/folders/1iFa_Ar05RP-c6JDYhPLcw50Gjeffqzue?usp=sharing)')
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
        append_to_sheet(adi, staff_id)
        st.success('登録しました')

# 未読確認
st.write('---')
check = st.checkbox('未読確認')
if check:
    df = read_sheet()


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
            st.write(f'■{adi}未読者：残り{len(midoku)}名')
            st.write(f'{midoku}')
    st.write('---')
