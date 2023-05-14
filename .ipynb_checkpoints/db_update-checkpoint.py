#新旧Excelファイルからそれぞれdbを作成（上書き）する
import pandas as pd
import sqlite3
#Excelファイル読込みと加工（旧データファイル）
df = pd.read_excel('★個人情報削除【2021.12月まで】問い合わせ件数管理.xlsx', header=0)
df.drop(df.columns[[1, 2, 3, 4, 5, 8]], axis=1, inplace=True)
df.set_axis(['date', 'category', 'drug', 'question', 'answer'], axis=1, inplace=True)
df.set_index('date', inplace=True)
df.fillna('―', inplace=True)
#Excelファイル読込みと加工（新データファイル）
df_n = pd.read_excel('【2022.1月から】問い合わせ記録_2021改訂版.xlsx', 
                    sheet_name='問い合わせ記録', header=1)
df_n.drop(df_n.columns[[1, 2, 3, 4, 5, 11, 12]], axis=1, inplace=True)
df_n.set_axis(['date', 'category', 'drug', 'question', 'answer', 'reference'], 
            axis=1, inplace=True)
df_n.set_index('date', inplace=True)
df_n.fillna('―', inplace=True)
#db作成（既存のdbへの上書き）
db = sqlite3.connect('toiawase.db')
cur = db.cursor()
#2021年までのデータテーブル作成
sql = """
    CREATE TABLE IF NOT EXISTS T_old(
        "date" NUMERIC, 
        "category" STRING, 
        "drug" STRING, 
        "question" STRING, 
        "answer" STRING
        );
"""
cur.execute(sql)
#2022年以降のデータテーブル作成
sql = """
    CREATE TABLE IF NOT EXISTS T_new(
        "date" NUMERIC, 
        "category" STRING, 
        "drug" STRING, 
        "question" STRING, 
        "answer" STRING,
        "reference" STRING
        );
"""
cur.execute(sql)
db.commit()
#テーブル（旧データファイル）データの上書き
df.to_sql('T_old', db, if_exists='replace')
cur.execute("SELECT * FROM T_old")
data = cur.fetchall()
#テーブル（新データファイル）データの上書き
df_n.to_sql('T_new', db, if_exists='replace')
cur.execute("SELECT * FROM T_new")
data_n = cur.fetchall()

cur.close()
db.close()