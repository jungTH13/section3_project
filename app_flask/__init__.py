from flask import Flask
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time


DB_FILENAME = 'DB_API.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
MODEL_FILENAME = 'forest_model.pkl'
MODEL_FILEPATH = os.path.join(os.getcwd(), MODEL_FILENAME)
START_FUNC=1


def create_app():
    app=Flask(__name__)

    from app_flask.views.main import main_bp
    from app_flask.views.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app


#데이터베이스 및 예측모델 생성
def update():
    print("update sol activate")
    exec(open(os.path.join(os.getcwd(), 'app_flask/data/make_DB.py'),'rt',encoding='UTF8').read())
    exec(open(os.path.join(os.getcwd(), 'app_flask/data/make_model.py'),'rt',encoding='UTF8').read())
    print("update sol done")

#서울특별시 부동산 실거래가 정보 DB 속성 설명 dict
columns_name={'RTMS_ID': '실거래가아이디',
              'ACC_YEAR': '신고년도',
              'BJDONG10_CD': '법정동코드',
              'BJDONG_NM': '법정동명',
              'BLDG_AREA': '건물면적',
              'BLDG_MUSE_CD': '건물주용도코드',
              'BLDG_MUSE_NM': '건물주용도',
              'BLDG_NM': '건물명',
              'BUILD_YEAR': '건축년도',
              'DEAL_YMD': '계약일자',
              'FLR_INFO': '층정보',
              'OBJ_AMT': '물건금액',
              'SGG_CD': '시군구코드',
              'SGG_NM': '자치구명',
              'TOT_AREA': '대지권면적'}

#DB 자동 업데이트를 위한 스케쥴러 호출(매일 9시경 DB업데이트 실시)
scheduler= BackgroundScheduler()
job= scheduler.add_job(update, 'cron', day_of_week='mon-sun', hour=0, minute=55)
scheduler.start()

update()

if __name__=='__main__':
    app.run(debug=True)