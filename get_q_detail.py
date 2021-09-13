import streamlit as st
import pandas as pd

pd.get_option("display.max_columns")
def get_q_detail(file):

    logout_button = st.sidebar.button('log out')
    if logout_button:
        st.session_state['login'] = 0

    if 'file_review' not in st.session_state:
        st.session_state['file_review'] = file[file['Ambience#Decoration']!='-']

    
    st.table(st.session_state['file_review'][['年齢', '性別', '属性', 'レビュー']])