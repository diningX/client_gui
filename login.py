import streamlit as st
def login(db):
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
            return False
        else:
            correct_password = login_pass_list[user_name]
            if correct_password != password:
                st.write('pass wordが違います。')
                return False
            else:
                return True