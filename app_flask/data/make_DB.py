import requests
import sqlite3
import json
import os
from app_flask import DB_FILEPATH

LIST_COUNT=200000 #초기 DB에 저장할 자료 수



def create_table(cur,conn):
  #서울특별시 부동산 실거래가 정보 DB 생성
  cur.execute("""CREATE TABLE IF NOT EXISTS actual_price( RTMS_ID INT FRIMARY KEY NOT NULL,
                                                  ACC_YEAR INT, 
                                                  BJDONG10_CD INT,
                                                  BJDONG_NM VARCHAR,
                                                  BLDG_AREA FLOAT,
                                                  BLDG_MUSE_CD INT,
                                                  BLDG_MUSE_NM VARCHAR,
                                                  BLDG_NM VARCHAR,
                                                  BUILD_YEAR INT,
                                                  DEAL_YMD INT,
                                                  FLR_INFO INT,
                                                  OBJ_AMT INT,
                                                  SGG_CD INT,
                                                  SGG_NM VARCHAR,
                                                  TOT_AREA FLOAT)
                                                  """)
  conn.commit()

#데이터 EDA 함수
def data_sol(row):
  if row['FLR_INFO'] == '':
    row['FLR_INFO']=1
  if row['BLDG_NM'] == '':
    row['BLDG_NM']='unkwon'
  if row['BUILD_YEAR'] == '':
    row['BUILD_YEAR']=0000
  if row['TOT_AREA'] == '':
    row['TOT_AREA']=0.0
    
  row['RTMS_ID'] = int(row['RTMS_ID'].replace('-',''))
  return row


#데이터를 저장할 데이터 베이스 생성
conn=sqlite3.connect(DB_FILEPATH) 
cur=conn.cursor()
#테이블 생성 함수 호출
create_table(cur,conn)

#데이터 베이스 내 기본키의 리스트를 호출하여 저장
DB_RTMS_ID=[]
for row in cur.execute("SELECT RTMS_ID FROM actual_price").fetchall():
    if row is None:
        break
    DB_RTMS_ID.append(row[0])

count=0

while count<=LIST_COUNT :
    #API를 통한 데이터 받아오기
    API_URL=f'http://openapi.seoul.go.kr:8088/6961534552696f7037316247686e44/json/landActualPriceInfo/{count+1}/{count+1000}/'
    count+=1000
    data=requests.get(API_URL)
    
    #JSON 데이터를 파싱하여 가공
    parsed_data=json.loads(data.text)
    list_data=parsed_data.get('landActualPriceInfo').get('row')
    total_count=parsed_data.get('landActualPriceInfo').get('list_total_count')

    #기본키 중복여부를 확인한 후, 데이터베이스에 입력
    for row in list_data:
        row=data_sol(row)
        if row['RTMS_ID'] in DB_RTMS_ID:
          conn.commit()
          count=cur.execute("SELECT COUNT() FROM actual_price").fetchone()[0]
          break
        
        cur.execute(f"""INSERT INTO actual_price VALUES({row['RTMS_ID']},{row['ACC_YEAR']},{row['BJDONG10_CD']},"{row['BJDONG_NM']}",{row['BLDG_AREA']},{row['BLDG_MUSE_CD']},"{row['BLDG_MUSE_NM']}","{row['BLDG_NM']}",{row['BUILD_YEAR']},{row['DEAL_YMD']},{row['FLR_INFO']},{row['OBJ_AMT']},{row['SGG_CD']},"{row['SGG_NM']}",{row['TOT_AREA']})""")
    conn.commit()
    print("DB update list count: ",count)

if count>LIST_COUNT:
      cur.execute(f"DELETE FROM actual_price WHERE RTMS_ID in(SELECT RTMS_ID FROM actual_price LIMIT 100000 OFFSET {LIST_COUNT})")
      conn.commit()
      print(f"이전데이터 삭제(현재 보유개수{LIST_COUNT})")

conn.close()