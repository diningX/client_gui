import streamlit as st
def login(login_list):
    info_list = {'店長' : 'BranchInfo', '経営者' : 'ClientInfo'}

    query = db.collection(info_list[branch_or_client])
    docs = query.get()
    login_pass_list = {}
    for d in docs:
        doc = d.to_dict()
        login_pass_list[doc['user_name']] = doc['password']
    branch_or_client = st.radio('選択', ['店長', '経営者'])
    user_name = st.text_input('user name')
    password = st.text_input('password', type="password")
    login_button = st.button('login')
    if login_button:
        if user_name not in login_list.keys():
            st.write('user nameが存在しません')
            return False
        else:
            correct_password = login_list[user_name]
            if correct_password != password:
                st.write('pass wordが違います。')
                return False
            else:
                return True