import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta
import numpy as np

def make_date_column(start, end):

    # 日付条件の設定
    strdt = dt.strptime(start, '%Y-%m-%d')  # 開始日
    enddt = dt.strptime(end, '%Y-%m-%d')  # 終了日

    # 日付差の日数を算出（リストに最終日も含めたいので、＋１しています）
    days_num = (enddt - strdt).days + 1 
    # シンプルにforとappendを使用した場合
    datelist = []
    for i in range(days_num):
        datelist.append(strdt + timedelta(days=i))

    date2=[]

    # 確認用
    for d in datelist:
        #     print(d.strftime("%Y-%m-%d"))
        date2.append(d.strftime("%Y-%m-%d"))
    date2=pd.DataFrame({'date':date2})
    
    return date2

def time_series(df1):
    
    st.write('各種時系列')
    dfa=df1[['time','星評価']].set_index('time')
    dfa=dfa.groupby('time').mean()
    dfb=df1[['time','属性']]
    dfb=dfb.groupby(['time','属性']).sum()
    start, end=dfb.index[0][0],dfb.index[-1][0]
    df_new=make_date_column(start,end).rename(columns={'date':'time'})

    for name in ['属性','性別']:
        dfb=df1[['time',name]]
        dfb['num']=1
        dfb=dfb.groupby(['time',name]).sum()
        columns =df1[name].unique().tolist()

        
        for belongs in columns:
            a=dfb.xs(belongs,level=name).rename(columns={'num':  belongs}).reset_index()
            df_new=pd.merge(df_new,a,on='time', how='outer')
        df_new=df_new.fillna(0).set_index('time').astype(int)
    name='年齢'
    dfs=df1[['time',name]].sort_values(name)
    dfs['num']=1
    labels = [ '{0} – {1}'.format(i, i + 10) for i in range(10, 90, 10) ]
    dfs[name]=pd.cut(dfs[name],np.arange(10, 100, 10),labels=labels)
    dfs=dfs.groupby(['time',name]).sum()

    start, end=dfb.index[0][0],dfb.index[-1][0]
    df_old=make_date_column(start,end).rename(columns={'date':'time'})
    for belongs in labels:
        a=dfs.xs(belongs,level=name).rename(columns={'num':  belongs}).reset_index()
        df_old=pd.merge(df_old,a,on='time', how='outer')
    df_old=df_old.fillna(0).set_index('time').astype(int)
    df_all = pd.concat([dfa,df_new,df_old],axis=1) 

    names = st.multiselect('属性を選択してください',df_all.columns)
    fig = go.Figure()
    for name in names:
        fig.add_trace(go.Scatter(y=df_all[name],x=df_all.index, name=name))
    fig.update_layout(width=900, height=400)
    st.plotly_chart(fig, use_container_width=True)