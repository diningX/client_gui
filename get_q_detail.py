import streamlit as st
import pandas as pd
from freq_words_extract import get_freq_words_, no_a, no_n, no_v
from janome.tokenizer import Tokenizer

review_columns = ['年齢', '性別', '所属', 'レビュー', 'janome']
def get_hinshi(text):
    t = Tokenizer()
    keys = []
    for token in t.tokenize(text):
        if token.part_of_speech.startswith('動詞'):
            if token.base_form not in no_v:
                keys.append(token.base_form)
        if token.part_of_speech.startswith('名詞'):
            if token.base_form not in no_n:
                keys.append(token.base_form)
        if token.part_of_speech.startswith('形容詞'):
            if token.base_form not in no_a:    
                keys.append(token.base_form)
    return ' '.join(keys)

def make_word_df(file, words):
    data = []
    for i in range(len(file)):
        review_text = file.iloc[i, 3]
        #print(file.iloc[i, :])
        m = 0
        for word in words:
            if word in file.iloc[i, 4]:
                m += 1
            if m == len(words):
                datum = {}
                for c in range(5):
                    datum[review_columns[c]] = file.iloc[i, c]
                data.append(datum)
    return pd.DataFrame(data=data)

def make_gender_df(file, gender):
    data = []
    for i in range(len(file)):
        g = file.iloc[i, 1]
        if g in gender:
            datum = {}
            for j in range(5):
                datum[review_columns[j]] = file.iloc[i, j]
            data.append(datum)
    if len(data) == 0:
        return pd.DataFrame(data = data, columns=review_columns)
    else:
        return pd.DataFrame(data = data)

    return file[file['性別'] in gender]
def make_affiliation_df(file, affiliation):
    data = []
    for i in range(len(file)):
        g = file.iloc[i, 2]
        if g in affiliation:
            datum = {}
            for j in range(5):
                datum[review_columns[j]] = file.iloc[i, j]
            data.append(datum)
    if len(data) == 0:
        return pd.DataFrame(data = data, columns=review_columns)
    else:
        return pd.DataFrame(data = data)
def make_age_df(file, age_list):
    data = []
    age_list = [int(i.replace('代', '')) for i in age_list]
    for i in range(len(file)):
        g = file.iloc[i, 0]
        g = 10*int(g/10)
        if g in age_list:
            datum = {}
            for j in range(5):
                datum[review_columns[j]] = file.iloc[i, j]
            data.append(datum)
    if len(data) == 0:
        return pd.DataFrame(data = data, columns=review_columns)
    else:
        return pd.DataFrame(data = data)

def filter_df(file, gender, affiliation, age_list):
    file = make_gender_df(file, gender)
    file = make_affiliation_df(file, affiliation)
    file = make_age_df(file, age_list)
    return file


pd.get_option("display.max_columns")
def get_q_detail(file):

    if 'file_review' not in st.session_state:
        file_review = file[file['Ambience#Decoration']!='-']
        st.session_state['file_review'] = file_review[['年齢', '性別', '所属', 'レビュー']]
        keys = []
        for i in st.session_state['file_review']['レビュー']:
            keys.append(get_hinshi(i))
        CONTENT = ' '.join(keys)
        st.session_state['file_review']['janome'] = keys
        
        st.session_state['CONTENT'] = CONTENT


    if 'CONTENT' not in st.session_state:
        keys = []
        for i in st.session_state['file_review']['レビュー']:
            keys.append(get_hinshi(i))
        CONTENT = ' '.join(keys)
        st.session_state['file_review']['janome'] = keys
        
        st.session_state['CONTENT'] = CONTENT


    logout_button = st.sidebar.button('log out')
    if logout_button:
        st.session_state['login'] = 0

    

    show_all = st.sidebar.radio('全てのレビューを表示', options=['する', 'しない'])
    if show_all == 'する':
        show_df = st.session_state['file_review'][['年齢', '性別', '所属', 'レビュー']]
        show_df['index'] = [i+1 for i in range(len(show_df))]
        show_df = show_df.set_index('index')
        st.table(show_df)
    else:

        default_gender = st.session_state['file_review']['性別'].unique()
        default_affiliation = st.session_state['file_review']['所属'].unique()
        default_age = [str(i*10)+'代' for i in range(15)]

        gender = st.sidebar.multiselect('性別による絞り込み', options=default_gender, default=default_gender)
        affiliation = st.sidebar.multiselect('所属による絞り込み', options=default_affiliation, default=default_affiliation)
        age_list = st.sidebar.multiselect('年代による絞り込み', options=default_age, default=default_age)
        show_df = filter_df(st.session_state['file_review'], gender, affiliation, age_list)

        word_select = st.sidebar.checkbox('頻出単語による絞り込みを行う')
        if word_select:
            num = st.sidebar.number_input('頻出単語の表示する件数（多い順）', min_value=0, step=1)
            options = get_freq_words_(st.session_state['CONTENT'], num)
            selected_words = st.sidebar.multiselect('頻出単語による絞り込み', options=options)
            selected_words = [i.split('(')[0] for i in selected_words]
            show_df = make_word_df(show_df, selected_words)
        if len(show_df) == 0:
            show_df = pd.DataFrame(data=[], columns=review_columns)
        show_df = show_df.rename(columns={'属性': '所属'})
        show_df['index'] = [i+1 for i in range(len(show_df))]
        show_df = show_df.set_index('index')
        st.table(show_df[['年齢', '性別', '所属', 'レビュー']])
        st.sidebar.write('レビュー表示件数：' + str(len(show_df)), ' 件')
    #st.table(st.session_state['file_review'][['年齢', '性別', '所属', 'レビュー']])