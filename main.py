import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
from heatmaps import heatmaps
from main2 import login_service
from login import login

def get_data(user_name):
    query = db.collection('QuestionnaireResult').where('user_name', '==', user_name)
    docs = query.get()

    data = []
    for doc in docs:
        datum = {}
        review_data = doc.to_dict()
        user_data = db.collection('UserInfo').document(review_data['uId'])
        user_data = user_data.get().to_dict()
        datum['レビュー'] = review_data['response']['detail']
        datum['星評価'] = review_data['response']['star']
        datum['居住地'] = user_data["prefecture"]+user_data["municipality"]
        datum['属性'] = user_data["affiliation"]
        birthdata = user_data['birthday'].split('/')
        datum['年齢'] = age(int(birthdata[0]), int(birthdata[1]), int(birthdata[2]))
        datum['性別'] = user_data['gender']
        datum['time'] = review_data['time'].split('T')[0]

        for a in aspects:
            datum[a] = review_data[a]
        data.append(datum)
    return pd.DataFrame(data=data)


if not firebase_admin._apps:

    # 初期済みでない場合は初期化処理を行う
    cred = credentials.Certificate('table-customer-app-development-firebase-adminsdk-w8skc-5ef3db5472.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

login_or_not = login(db)
if login_or_not:
    st.write('login 成功')

            





            

