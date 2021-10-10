from flask import Blueprint, render_template
from app_flask import DB_FILEPATH
import sqlite3

import joblib
from app_flask.data.make_model import select_columns

api_bp=Blueprint('api',__name__)

@api_bp.route('/api')
def index():
    #확인용 코드
    conn=sqlite3.connect(DB_FILEPATH) 
    cur=conn.cursor()
    info=cur.execute("""SELECT DEAL_YMD, BJDONG_NM ,SGG_NM ,BLDG_MUSE_NM ,BLDG_AREA ,TOT_AREA ,OBJ_AMT 
                        FROM actual_price ap 
                        order by DEAL_YMD DESC
                        limit 15""").fetchall()
    labels_list_dumy=[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],[11,11],[12,12]]

    return render_template('api/index.html',info=info,labels_list=labels_list_dumy[-12:]),200

@api_bp.route('/api/<BJDONG10_CD>/<BLDG_AREA>/<BLDG_MUSE_CD>/<BUILD_YEAR>/<SGG_CD>/<TOT_AREA>')
def api_get(BJDONG10_CD,BLDG_AREA,BLDG_MUSE_CD,BUILD_YEAR,SGG_CD,TOT_AREA):
    
    X_data=[[BJDONG10_CD,BLDG_AREA,BLDG_MUSE_CD,BUILD_YEAR,SGG_CD,TOT_AREA]]
    forest_model=joblib.load('forest_model.pkl')
    
    y_pred=forest_model.predict(X_data)
    return_object={'predicted_value' : int(y_pred), 'Precision' : 1}
    return return_object,200

