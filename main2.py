import pandas as pd
from heatmaps import heatmaps
import streamlit as st

def get_data(user_name, db):
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


def login_service(user_name, db):
    st.write('店舗画面')
    st.write('user name : ' + user_name)
    option = st.selectbox('サービスを選択してください',('-', 'ヒートマップ・円グラフ', '時系列可視化', '抽選設定'))
    if option == 'ヒートマップ・円グラフ':
        print('aaaaaa')
        file = get_data(user_name, db)
        heatmaps(file)

