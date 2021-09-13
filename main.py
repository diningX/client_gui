import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
from heatmaps import heatmaps
from get_data import get_data
from time_series import time_series
from lottery_settings import lottery_settings


if not firebase_admin._apps:

    # 初期済みでない場合は初期化処理を行う
    cred = credentials.Certificate('table-customer-app-development-firebase-adminsdk-w8skc-5ef3db5472.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

if 'login' not in st.session_state:
    st.session_state['login'] = 0
if st.session_state['login'] == 0:
    info_pass_list = {'店長' : 'BranchInfo', '経営者' : 'ClientInfo'}
    branch_or_client = st.radio('選択', ['店長', '経営者'])
    query = db.collection(info_pass_list[branch_or_client])
    docs = query.get()
    login_pass_list = {}
    for d in docs:
        doc = d.to_dict()
        login_pass_list[doc['user_name']] = doc['password']
    st.write(login_pass_list)
    user_name = st.text_input('user name')
    password = st.text_input('password', type="password")
    login_button = st.button('login')
    if login_button:
        if user_name not in login_pass_list.keys():
            st.write('user nameが存在しません')
        else:
            correct_password = login_pass_list[user_name]
            if correct_password != password:
                st.write('pass wordが違います。')
            else:
                if len(st.session_state) != 0:
                    for k in st.session_state.keys():
                        st.session_state.pop(k)
                st.session_state['login'] = 1
                st.session_state['user_name'] = user_name
                st.session_state['b_or_c'] = info_pass_list[branch_or_client]

if st.session_state['login'] == 1:
    if st.session_state['b_or_c'] == 'BranchInfo':
        option = st.selectbox('サービスを選択してください',('-', 'ヒートマップ・円グラフ', '時系列可視化', 'アンケート個別表示', '抽選設定'))
        if option == 'ヒートマップ・円グラフ':
            st.session_state['logout_sidebar'] = 0
            user_name = st.session_state['user_name']
            b_or_c = st.session_state['b_or_c']
            if 'file' not in st.session_state:
                file = get_data(db, user_name, b_or_c)
                st.session_state['file'] = file
            heatmaps(st.session_state['file'])
        
        if option == '時系列可視化':
            if 'file' not in st.session_state:
                file = get_data(db, user_name, b_or_c)
                st.session_state['file'] = file
            time_series(st.session_state['file'])

        if option == '抽選設定':
            user_name = st.session_state['user_name']
            b_or_c = st.session_state['b_or_c']
            lottery_settings(db, user_name, b_or_c)



    
    else:
        st.write('実装中')
        logout = st.button('logout')


        if logout:
            st.session_state['login'] = 0

            





            

