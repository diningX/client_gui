import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st

cred = credentials.Certificate('/content/drive/MyDrive/database/table-customer-app-development-firebase-adminsdk-w8skc-5ef3db5472.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

user_name = st.text_input('user_name')
password = st.text_input('password', type="password")

query_b = db.collection('BranchInfo')
docs_b = query_b.get()
login_list
for doc in docs_b:



query_c = db.collection('ClientInfo')
docs_c = 
