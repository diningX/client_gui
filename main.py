import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
from heatmaps import heatmaps

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

login = False
if not firebase_admin._apps:
    # 初期済みでない場合は初期化処理を行う
    cred = credentials.Certificate('table-customer-app-development-firebase-adminsdk-w8skc-5ef3db5472.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

if not login:
    branch_or_client = st.radio('選択', ['店長', '経営者'])
    user_name = st.text_input('user name')
    password = st.text_input('password', type="password")

info_list = {'店長' : 'BranchInfo', '経営者' : 'ClientInfo'}

query = db.collection(info_list[branch_or_client])
docs = query.get()
login_list = {}
for d in docs:
    doc = d.to_dict()
    login_list[doc['user_name']] = doc['password']

st.write(login_list)

if not login:
    login_button = st.button('login')
    if login_button:
        if user_name not in login_list.keys():
            st.write('user nameが存在しません')
        else:
            correct_password = login_list[user_name]
            if correct_password != password:
                st.write('pass wordが違います。')
            else:
                st.write('login完了')
                login = True

if login:
    
    st.Title('店舗画面')
    st.write(user_name)
    option = st.selectbox('サービスを選択してください',('-', 'ヒートマップ・円グラフ', '時系列可視化', '抽選設定'))
    if option == 'ヒートマップ':
        file = get_data(user_name)
        heatmaps(file)

        





        

