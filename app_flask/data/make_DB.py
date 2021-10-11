import requests
import sqlite3
import json
import os
from app_flask import DB_FILEPATH

LIST_COUNT=200000 #초기 DB에 저장할 자료 수

TRIGER=False #중복 확인시 루프 타출을 위한 트리거

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

#데이터 베이스 내 가장 최근 거래일자를 호출하여 저장
try:
  DB_RTMS_ID=cur.execute("SELECT DEAL_YMD from actual_price ap order by DEAL_YMD DESC limit 1").fetchone()[0]
except:
  DB_RTMS_ID=0

count=0

while count<LIST_COUNT :
    #API를 통한 데이터 받아오기
    API_URL=f'http://openapi.seoul.go.kr:8088/6961534552696f7037316247686e44/json/landActualPriceInfo/{count+1}/{count+1000}/'
    count+=1000
    data=requests.get(API_URL)
    
    #JSON 데이터를 파싱하여 가공
    parsed_data=json.loads(data.text)
    list_data=parsed_data.get('landActualPriceInfo').get('row')
    total_count=parsed_data.get('landActualPriceInfo').get('list_total_count')

    #거래일자를 확인하여 중복여부 확인 후, 데이터베이스에 입력
    for row in list_data:
        row=data_sol(row)
        print(f'{count}번 데이터 확인중 ',row['DEAL_YMD'],' == ',DB_RTMS_ID)
        if int(row['DEAL_YMD']) <= DB_RTMS_ID:
          conn.commit()
          count=cur.execute("SELECT COUNT() FROM actual_price").fetchone()[0]
          TRIGER=True
          break
        else:
          cur.execute(f"""INSERT INTO actual_price VALUES({row['RTMS_ID']},{row['ACC_YEAR']},{row['BJDONG10_CD']},"{row['BJDONG_NM']}",{row['BLDG_AREA']},{row['BLDG_MUSE_CD']},"{row['BLDG_MUSE_NM']}","{row['BLDG_NM']}",{row['BUILD_YEAR']},{row['DEAL_YMD']},{row['FLR_INFO']},{row['OBJ_AMT']},{row['SGG_CD']},"{row['SGG_NM']}",{row['TOT_AREA']})""")
    conn.commit()
    print("DB update list count: ",count)
    if TRIGER:
      break

#데이터양이 최대 개수를 넘을 경우 오래된 데이터의 제거 실시
if count>LIST_COUNT:
      cur.execute(f"DELETE FROM actual_price WHERE DEAL_YMD <= (SELECT DEAL_YMD FROM actual_price order by DEAL_YMD DESC LIMIT 1 OFFSET {LIST_COUNT})")
      conn.commit()
      count=cur.execute("SELECT COUNT() FROM actual_price").fetchone()[0]
      print(f"이전데이터 삭제(현재 보유개수{count}/최대 보유개수{LIST_COUNT})")

conn.close()