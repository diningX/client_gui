import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
from heatmaps import heatmaps
from get_data import get_data
from time_series import time_series
from lottery_settings import lottery_settings
from get_q_detail import get_q_detail
import os
import json



if not firebase_admin._apps:

    
    # 初期済みでない場合は初期化処理を行う
    keys = {
    "type": os.environ.get('type'),
    "project_id": os.environ.get('project_id'),
    "private_key_id": os.environ.get('private_key_id'),
    "private_key": os.environ.get('private_key'),
    "client_email": os.environ.get('client_email'),
    "client_id": os.environ.get('client_id'),
    "auth_uri": os.environ.get('auth_uri'),
    "token_uri": os.environ.get('token_uri'),
    "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
    "client_x509_cert_url": os.environ.get('client_x509_cert_url')
    }
    
    keys = {
        "type" : "service_account",
        "project_id" : "table-customer-app-development",
        "private_key_id" : "412c7471a564bb5f9ba84312edd0f4b440989d34",
        "private_key" : "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCeu4Pp+zmTYBFn\nSOZGD6K8Te4oxALeaoPGGeE3Li9XysQqpEtH70OgTfO+YvKciGE0TVLQzPH2X4xq\np3uZ8DV/YQonh0H6uVRyLlGxKTK1uQaVo/x8cTJILwdcI7VC6ps/pvXPYa+nLE4V\nlwAC4eWjYSk2KHzfecQomDjvzktkuQGEl+tpOcVXyEkzOQEjpLPhgg+P6SoaFHqw\nwtkxO5PaWQjjRx99eX/d9b7jjDpII3hwd+OMi7cgj17ictiYYAjhXykfFyHuardP\n7QYX1mmkQUxw80NB7JNSPgZWAz48Y4MSoFmPtJKZHYOykFfyt+3ZS92WQ4q2pe99\nRSesT/V1AgMBAAECggEAAubpEP3g/hhGCS40g426oG2zpSF8RJu26rLDbX0AgZQ5\nROb5t112TjfOn9RIR44DakTgTDqgUSxLBrzReNgtlOAYeEOJScUEow0aEj6aE5Id\nPt7KJBj1CIvPkHgt/VoJBOoPrr8Zn9lNWNNeEoTAbDMVC/fuhy6/OYIa8bYYURrn\nYgL1b0ME0ZQTq0BEKliOvVs3jujKCOiHcy2A3gdgKg0SgIMDtMr+kifDy4I8Bnbx\nmD721ykUT4Rlswm6AZ6QyzZXM+X4jQMg1LUx7VGdYqd2OKqYrev7VO5SX/niWQaW\noJd0e33ZObqqZSymH/kd2SGmkkOdEhpuulqHPlmIIQKBgQDdHMLm3aAgOf83Jvfl\nXwSecZT2LAJptTKkMGJ8j9ggGuTil35iF+m6otodszJ53zhNa7plnMSSHFCbT1Ot\nbPmO2zzk4eL9zc49+K7rvrpHl3U3j1Vycgnbem0mAf1rTdbNhgZzrNWD93gwZngw\n/QS+woW3FcNEiTrIkP7DRNWbRQKBgQC3xxZERo/6PS4dRCPj+pkV/WDQbx2RNEvq\nJksOtX3nmkwvEuA7P3OhzXbfe8Qlmz377+5v6k+kzNPH7tVN2daPS4JKBy6PrE5z\nUncfC69WKT8g2r9AMjS1lSgpg6YteLrc0vwF8lOZB96hfssiltrI6BbxEdJIlpL2\n5SthDB18cQKBgQDWF2Mf5reEfKOA41pj3Py77X4uXa54a9n84Fx7/0tkyqWUQNs+\nX6kP7V8EIt5c4qXBUO3KNWCfmIrz1ntPEJUSnXT4qT8AQKXRm1jDKolziFMW2NID\nXiftOz0z7/lQTK4PkhXtKwwSGytksdLunA5cJj0SaSAI3FbunHYQ3DV3gQKBgHyJ\nWip8Urb13JkSguvL9w9yu7ejhLrQYJ1Uw8o87QwUgInp1a/wqLA95s89NMdzMwbW\nKZMHil8YOm+jBkMSWpaSScFWqpPL5QG7IWQVbAUMQG5ILhAXtaZTZHr1bpgj1yUr\niIOTGll6fsCbhpZy+eHpfRpxxDlSaFcNJ19FcXnRAoGBAJWbzR5CrKOyhCecp1eD\nR+NQXMwOyPp7SNoumqTQs5iTuuIqRopO6Ey4N4296WVYDfQr4nTvDncwhsG1wb5d\nu3Lj5GG4G3xNSmfaJ0rs90E77uRDFpK9b7xZoxQuD2HNNQ5Bp/bHpj83JuXD6ByS\nYJ7wQvueTKwXNEuoIvML/W7A\n-----END PRIVATE KEY-----\n",
        "client_email" : "firebase-adminsdk-w8skc@table-customer-app-development.iam.gserviceaccount.com",
        "client_id" : "109308147140205209586",
        "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
        "token_uri" : "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url" : "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url" : "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-w8skc%40table-customer-app-development.iam.gserviceaccount.com"
    }
    #print(type(keys))

    #json_open = open('keys.json', 'w')
    #json.dump(keys, json_open, indent=2)
    #json_open.close()
    #json_open = open('keys.json', 'r')
    #json_file = json.load(json_open)
    #print('=========================')
    #print(json_file)
    #print('=========================')

    cred = credentials.Certificate(keys)
    firebase_admin.initialize_app(cred)

st.session_state['db'] = firestore.client()

if 'login' not in st.session_state:
    st.session_state['login'] = 0
if st.session_state['login'] == 0:
    info_pass_list = {'店長' : 'BranchInfo', 'オーナー' : 'ClientInfo'}
    branch_or_client = st.radio('選択', ['店長', 'オーナー'])
    query = st.session_state['db'].collection(info_pass_list[branch_or_client])
    docs = query.get()
    login_pass_list = {}
    for d in docs:
        doc = d.to_dict()
        login_pass_list[doc['user_name']] = doc['password']
    #st.write(login_pass_list)
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
        option = st.selectbox('サービスを選択してください',('-', 'ヒートマップ・円グラフ', '時系列可視化', 'レビュー個別表示', '各種設定'))
        if option == 'ヒートマップ・円グラフ':

            if 'file' not in st.session_state:
                file = get_data(st.session_state['db'], st.session_state['user_name'], st.session_state['b_or_c'])
                st.session_state['file'] = file
            heatmaps(st.session_state['file'])
        
        if option == '時系列可視化':
            if 'file' not in st.session_state:
                file = get_data(st.session_state['db'], st.session_state['user_name'], st.session_state['b_or_c'])
                st.session_state['file'] = file
            time_series(st.session_state['file'])
        
        if option == 'レビュー個別表示':
            if 'file' not in st.session_state:
                file = get_data(st.session_state['db'], st.session_state['user_name'], st.session_state['b_or_c'])
                st.session_state['file'] = file
            get_q_detail(st.session_state['file'])

        if option == '各種設定':
            lottery_settings(st.session_state['db'], st.session_state['user_name'], st.session_state['b_or_c'])



    
    else:
        st.write('実装中')
        logout = st.button('logout')


        if logout:
            st.session_state['login'] = 0

            





            

