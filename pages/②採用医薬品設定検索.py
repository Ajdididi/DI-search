import streamlit as st
import sqlite3
db = sqlite3.connect('druginfo.db')
cur = db.cursor()
st.title('医薬品設定情報')
kensaku = st.text_input('医薬品名（商品名もしくは一般名）を入力してください。※半角・全角は区別されます')
btn = st.button('検索')
if btn:
    if kensaku == '':
        st.write('何か入力してください！')
    else:
        kensaku = '%'+kensaku+'%'
        cur.execute("SELECT * FROM info WHERE drug LIKE ? OR general LIKE ?", 
                    [kensaku, kensaku])
        kekka = cur.fetchall()
        cur.close()
        db.close()

        if len(kekka) == 0:
            st.write('該当データはありません。')
            st.write('----------------------')
        else:
            st.write(f'該当データ数：{len(kekka)} 件')
            st.write('----------------------')

            for i in range(len(kekka)):
                # 採用の有無
                if kekka[i][1] == 1:
                    saiyo = '採用あり'
                elif kekka[i][1] == 2:
                    saiyo = '院内製剤'
                elif kekka[i][1] == 3:
                    saiyo = '緊急購入'
                else:
                    saiyo = '採用なし'
                
                # 採用形式
                if not kekka[i][7] is None:
                        youji = '要時'
                else:
                    youji = ''

                # 科限定
                if not kekka[i][8] is None:
                    limit = f'制限：{kekka[i][8]}'
                else:
                    limit = ''
                
                # 貯法
                if not kekka[i][6] is None:
                        store = '冷'
                else:
                    store = ''
                
                # 区分
                if not kekka[i][4] is None:
                        category = kekka[i][4]
                else:
                    category = ''
                
                # 自動車運転
                if not kekka[i][13] is None:
                    car = kekka[i][13]
                else:
                    car = '該当しない'
                
                # 薬情
                if not kekka[i][22] is None:
                    yakko1 = kekka[i][22]
                    side_effect = kekka[i][23]
                else:
                    yakko1 = '設定なし'

                st.write(f'【{kekka[i][0]}】&nbsp;&nbsp;{store}&nbsp;&nbsp;{youji}&nbsp;&nbsp;{limit}&nbsp;&nbsp;{category}&nbsp;&nbsp;{saiyo}  \n'
                    + f'■基本情報  \n'
                    + f'[一般名]&nbsp;&nbsp;{kekka[i][2]}  \n'
                    + f'[メーカー]&nbsp;&nbsp;{kekka[i][3]}  \n'
                    + f'[薬価]&nbsp;&nbsp;{kekka[i][5]} 円  \n'
                    + f'[YJcode]&nbsp;&nbsp;{kekka[i][12]}  \n'
                    )
                if not kekka[i][17] is None:   #粉砕設定が空欄かどうかで分岐
                    st.write('■調剤設定  \n'
                        + f'[一包化]&nbsp;&nbsp;{kekka[i][16]}  \n'
                        + f'[粉砕]&nbsp;&nbsp;{kekka[i][17]}  \n'
                        + f'[簡易懸濁]&nbsp;&nbsp;{kekka[i][18]}  \n'
                        + f'[注意事項]&nbsp;&nbsp;{kekka[i][19]}  \n'
                        )
                if not kekka[i][15] is None:   #日数制限設定の理由があるかどうかで分岐
                    st.write('■処方日数制限（法令上の制限は除く）  \n'
                        + f'[上限]&nbsp;&nbsp;{kekka[i][14]} 日  \n'
                        + f'[理由]&nbsp;&nbsp;{kekka[i][15]}  \n'
                        )
                st.write('■情報提供')
                st.write(f'[運転等]&nbsp;&nbsp;{car}')
                if not kekka[i][22] is None:
                    st.write(f'[薬効]&nbsp;&nbsp;  \n'
                             + f'{kekka[i][22]}  \n'
                             + f'[注意・副作用]&nbsp;&nbsp;  \n'
                             + f'{kekka[i][23]}')
                else:
                    st.write('[薬情] 設定なし')
                if not kekka[i][24] is None:
                    st.write(f'[薬効（診療科限定）]&nbsp;&nbsp;  \n'
                             + f'{kekka[i][24]}')
                
                if not kekka[i][20] is None:  #比重設定が空欄かどうかで分岐
                    st.write('■AddDis  \n'
                            + f'[比重]&nbsp;&nbsp;{kekka[i][20]}  \n'
                            + f'[粉の重量]&nbsp;&nbsp;{kekka[i][21]}'
                            )
                st.write('------------------------------  \n')