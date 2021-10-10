from flask import Blueprint, render_template
from app_flask import DB_FILEPATH
import sqlite3

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
def index():
    conn=sqlite3.connect(DB_FILEPATH) 
    cur=conn.cursor()
    #최신 거래정보 10개 출력
    info=cur.execute("""SELECT DEAL_YMD, BJDONG_NM ,SGG_NM ,BLDG_MUSE_NM ,BLDG_AREA ,TOT_AREA ,OBJ_AMT 
                        FROM actual_price ap 
                        order by DEAL_YMD DESC
                        limit 10""").fetchall()
    info_deal=[]
    for row in range(len(info)):
        info_deal.append(format(info[row][6],','))

    return render_template('index.html',info=info,info_deal=info_deal),200

@main_bp.route('/dashboard')
def semi_index():
    conn=sqlite3.connect(DB_FILEPATH) 
    cur=conn.cursor()
    #월 정보 출력
    info=cur.execute("""SELECT DEAL_YMD, BJDONG_NM ,SGG_NM ,BLDG_MUSE_NM ,BLDG_AREA ,TOT_AREA ,OBJ_AMT 
                        FROM actual_price ap 
                        order by DEAL_YMD DESC
                        limit 15""").fetchall()
    info_deal=[]
    for row in range(len(info)):
        info_deal.append(format(info[row][6],','))
    #월간 실거래량 출력
    labels_list=cur.execute("""SELECT DEAL_YMD/100 as DEAL_YM,count() as count
                            from actual_price ap
                            group by DEAL_YMD/100
                            order by DEAL_YM """).fetchall()
    conn.close()

    return render_template('dashboard/index.html',info=info,labels_list=labels_list[-12:],info_deal=info_deal),200

@main_bp.route('/reports')
def report_index():
    conn=sqlite3.connect(DB_FILEPATH) 
    cur=conn.cursor()
    #월 정보 출력
    labels_list=cur.execute("""SELECT DEAL_YMD/100 as DEAL_YM
                                from actual_price ap
                                group by DEAL_YM
                                order by DEAL_YM """).fetchall()
    #월간 건물주용도에 따른 실거래량 출력 후 dict형으로 변경
    data_list={}
    for name in ['단독주택','아파트','연립주택','오피스텔']:
        data=cur.execute(f"""SELECT DEAL_YMD/100 as DEAL_YM,count(BLDG_MUSE_NM) as count
                            from actual_price ap
                            WHERE BLDG_MUSE_NM='{name}'
                            group by DEAL_YM
                            order by DEAL_YM""").fetchall()
        data2={}
        for row in data:
            data2[row[0]]=row[1]

        data_list[name]=data2

    #월간 건물주용도에 따른 3.3㎡당 평균 매매가 출력 후 dict형으로 변경
    data2_list={}
    for name in ['단독주택','아파트','연립주택','오피스텔']:
        data=cur.execute(f"""SELECT DEAL_YMD/100 as DEAL_YM,round(AVG(AVG_ATM*3.3)) as AVG_ATM2
                            FROM (SELECT *,round(OBJ_AMT/BLDG_AREA) as AVG_ATM  FROM actual_price) as ap
                            WHERE BLDG_MUSE_NM='{name}'
                            group by DEAL_YM
                            order by DEAL_YM""").fetchall()
        data2={}
        for row in data:
            data2[row[0]]=row[1]

        data2_list[name]=data2

    #월 정보의 리스트형 변환
    labels=[]
    for row in labels_list[-12:]:
        labels.append(row[0])

    conn.close()
    return render_template('reports/index.html',labels_list=labels_list[-12:],labels=labels,data_1001=data_list['단독주택'],data_2001=data_list['아파트'],data_2002=data_list['연립주택'],data_14202=data_list['오피스텔'],data2_1001=data2_list['단독주택'],data2_2001=data2_list['아파트'],data2_2002=data2_list['연립주택'],data2_14202=data2_list['오피스텔'])

@main_bp.route('/metabase')
def metabase_index():
    return render_template('metabase/index.html')