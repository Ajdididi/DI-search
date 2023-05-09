import streamlit as st
import sqlite3
db = sqlite3.connect('druginfo.db')
cur = db.cursor()
st.title('医薬品設定情報')
kensaku = st.text_input('医薬品名（商品名もしくは一般名）を入力してください。※半角・全角は区別されます')
btn = st.button('検索')
if btn:
    kensaku = '%'+kensaku+'%'
    cur.execute("SELECT * FROM T_druginfo WHERE drug LIKE ? OR general LIKE ?", 
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

        for i in range(0, len(kekka)):
            if kekka[i][1] == 1:
                saiyo = '採用あり'
            elif kekka[i][1] == 2:
                saiyo = '院内製剤'
            else:
                saiyo = '採用なし'
            
            if not kekka[i][11] is None:
                youji = '要時購入'
            else:
                youji = '通常採用'
            
            if not kekka[i][12] is None:
                if not kekka[i][13] is None:
                    if not kekka[i][14] is None:
                        limit = f'{kekka[i][12]}・{kekka[i][13]}・{kekka[i][14]}'
                    else:
                        limit = f'{kekka[i][12]}・{kekka[i][13]}'
                else:
                    limit = f'{kekka[i][12]}'
            else:
                limit = 'なし'
            
            if not kekka[i][9] is None:
                store = '冷'
            else:
                store = '室温'
            
            if not kekka[i][6] is None:
                class_ = kekka[i][6]
            else:
                class_ = '―'

            st.write(f'{kekka[i][0]}  ＜{saiyo}＞' )
            st.write('----基本情報----  \n'
                    + f'[一般名]：{kekka[i][4]}  \n'
                    + f'[販売会社等]：{kekka[i][5]}  \n'
                    + f'[薬効分類名]：{kekka[i][8]}  \n'
                    + f'[薬価]：{kekka[i][7]} 円  \n'
                    + f'[貯法]：{store}  \n'
                    + f'[採用形式]：{youji}  \n'
                    + f'[診療科限定]：{limit}  \n'                
                    )
            #調剤設定
            if not kekka[i][42] is None:  #粉砕設定が空欄かどうかで分岐
                st.write('----調剤設定----  \n'
                        + f'[一包化]：{kekka[i][41]}  \n'
                        + f'[粉砕]：{kekka[i][42]}  \n' 
                        + f'[簡易懸濁]：{kekka[i][43]}  \n' 
                        + f'[注意事項]：{kekka[i][44]}  \n'
                        )
            else:
                st.write('----調剤設定----  \n'
                        + '該当しない')
            #最大量設定
            if not kekka[i][16] is None:
                st.write('----最大量設定----  \n'
                        + f'[1日最大量]：{kekka[i][16]} {kekka[i][15]}／[1回最大量]：{kekka[i][17]} {kekka[i][15]}  \n'
                        + f'[1日小児量]：{kekka[i][18]} {kekka[i][15]}／[1回小児量]：{kekka[i][19]} {kekka[i][15]}  \n' 
                        + f'[設定理由]：{kekka[i][20]}  \n'
                        + f'[備考]：{kekka[i][21]}  \n'
                        )
            else:
                st.write('----最大量設定----  \n'
                        + '該当しない')
            #自動車運転等の注意喚起
            if not kekka[i][27] is None:
                st.write('----自動車運転等の注意喚起----  \n'
                        + f'[注意分類]：{kekka[i][27]}／[注意番号]：{kekka[i][28]}  \n'
                        + f'[電カルマスタ登録(1・3)]：{kekka[i][29]}  \n'
                        + f'[部門マスタ登録(1・2・3)]：{kekka[i][30]}  \n' 
                        )
            else:
                st.write('----自動車運転等の注意喚起----  \n'
                        + '該当しない')
            #投与日数制限
            if not kekka[i][31] is None:
                st.write('----投与日数制限----  \n'
                        + f'[電カル設定（日）]：{kekka[i][31]}  \n'
                        + f'[部門設定（日）]：{kekka[i][32]}  \n'
                        + f'[休薬チェック表]：{kekka[i][33]}  \n'
                        + f'[設定理由]：{kekka[i][34]}  \n'
                        )
            elif not kekka[i][35] is None:
                st.write('----投与日数制限----  \n'
                        + f'[電カル設定（日）]：{kekka[i][35]}  \n'
                        + f'[部門設定（日）]：{kekka[i][36]}  \n'
                        + f'[設定理由]：{kekka[i][37]}  \n'
                        )
            else:
                st.write('----投与日数制限----  \n'
                        + '該当しない')
            #冷所医薬品の室温での安定性
            if not kekka[i][47] is None:
                st.write('----冷所医薬品の室温での安定性----  \n'
                        + f'[曝光]：{kekka[i][47]}  \n'
                        + f'[遮光]：{kekka[i][48]}  \n'
                        )
            elif not kekka[i][49] is None:
                st.write('----冷所医薬品の室温での安定性----  \n'
                        + f'[曝光]：{kekka[i][49]}  \n'
                        + f'[遮光]：{kekka[i][50]}  \n'
                        )
            else:
                st.write('----冷所医薬品の室温での安定性----  \n'
                        + '該当しない')
            #薬情
            if not kekka[i][51] is None:
                st.write('----薬情----  \n'
                        + f'[薬効]  \n'
                        + f'{kekka[i][51]}  \n'
                        + f'[注意・副作用]  \n'
                        + f'{kekka[i][52]}  \n'
                        )
                if not kekka[i][53] is None:
                    st.write(f'[薬効（診療科限定）]  \n'
                            + f'{kekka[i][53]}')
            else:
                st.write('----薬情----  \n'
                        + '設定なし')
            st.write('----------------------')

