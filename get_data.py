import streamlit as st

def get_data(db, user_name, b_or_c):
    _ = db.collection(b_or_c).where('user_name', '==', user_name).get()
    for d in _:
        bId = d.id
        
    query = db.collection('QuestionnaireResult').where('bId', '==', bId).where('isProcessedByAI', '==', True)
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