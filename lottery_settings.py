import streamlit as st

def lottery_settings(db, user_name, b_or_c):
    
    logout_button = st.sidebar.button('log out')
    if logout_button:
        st.session_state['login'] = 0

    if 'branch_data' not in st.session_state:
        docs = db.collection('BranchInfo').where('user_name' ,'==', user_name)
        query = db.collection('BranchInfo')
        
        for d in docs.stream():
            branch_data = d.to_dict()
            bId = d.id
        st.session_state['branch_data'] = branch_data
        st.session_state['query'] = query
        st.session_state['bId'] = bId
    
    if 'save_button' not in st.session_state:
        st.session_state['save_button'] = False
    
    
    lottery_discount = st.number_input('抽選割引率(%)', value=int(st.session_state['branch_data']['lotteryDiscount']*100), min_value=0, max_value=100)
    lottery_probability = st.number_input('抽選確率(%)', value=int(st.session_state['branch_data']['lotteryProbability']*100), min_value=0, max_value=100)
    questionare_DiscountRate = st.number_input('アンケート割引率(%)', value=int(st.session_state['branch_data']['questionareDiscountRate']*100), min_value=0, max_value=100)

    save_button = st.button('保存')
    if save_button:
        st.session_state['branch_data']['lotteryDiscount'] = lottery_discount / 100
        st.session_state['branch_data']['lotteryProbability'] = lottery_probability / 100
        st.session_state['branch_data']['questionareDiscountRate'] = questionare_DiscountRate / 100

        st.session_state['query'].document(st.session_state['bId']).set(st.session_state['branch_data'])


