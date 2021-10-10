from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint,uniform
import joblib
import pandas as pd
import pickle
import os

import sqlite3
from app_flask import DB_FILEPATH
from app_flask import MODEL_FILEPATH
from app_flask import MODEL_FILENAME

columns_list=['RTMS_ID','ACC_YEAR','BJDONG10_CD','BJDONG_NM','BLDG_AREA','BLDG_MUSE_CD','BLDG_MUSE_NM','BLDG_NM','BUILD_YEAR','DEAL_YMD','FLR_INFO','OBJ_AMT','SGG_CD','SGG_NM','TOT_AREA']
#모델 학습에 사용할 특성 리스트
select_columns=['BJDONG10_CD','BLDG_AREA','BLDG_MUSE_CD','BUILD_YEAR','SGG_CD','TOT_AREA','OBJ_AMT']


if not os.path.isfile(MODEL_FILEPATH):
    #데이터 베이스 연결
    conn=sqlite3.connect(DB_FILEPATH) 
    cur=conn.cursor()

    #데이터베이스 정보를 판다스 프래임으로 변환
    data=cur.execute("SELECT * FROM actual_price").fetchall()
    df=pd.DataFrame(data,columns=columns_list)

    #중복 혹은 불필요한 특성 제거
    df_clean=df[select_columns]

    X_data=df_clean.drop('OBJ_AMT',axis=1)
    y_data=df_clean['OBJ_AMT']

    #훈련모델 설정 및 하이퍼 파라미터 조정
    model = RandomForestRegressor(random_state=2,oob_score=True,n_jobs=-1,)

    dists={
        'max_depth' : [5,10,15,20,None],
        'max_features':uniform(0,1),
        'n_estimators':randint(100,300),
        'min_samples_leaf':[5,8,10,15,20],
        'min_samples_split':[15,20,30,40,50]
    }

    clf=RandomizedSearchCV(
        model,
        dists,
        n_iter=50,
        cv=5,
        scoring='r2',
        verbose=True
    )

    clf.fit(X_data,y_data)

    joblib.dump(clf.best_estimator_,MODEL_FILENAME)