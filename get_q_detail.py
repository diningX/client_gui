import streamlit as st

def get_q_detail(file):
    file_review = file[file['Ambience#Decoration']!='-']
    