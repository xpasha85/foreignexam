import streamlit as st
from random import choice, shuffle
import json


def load_1_task():
    with open('tasks1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks_ls = data['tasks']
    task = choice(tasks_ls)
    st.session_state['task1'] = task







st.set_page_config(page_title='Экзамен для иностранных граждан', page_icon='✍')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

if "first_load" not in st.session_state:
    load_1_task()
    st.session_state.first_load = True


def rf():
    # st.session_state.first_load = True
    st.session_state.clear()

st.write(st.session_state)
col1, col2 = st.columns(2)
with col1:
    st.subheader('Экзамен для иностранных граждан', divider=True)
with col2:
    st.button(label='Генерировать тест', icon='🔁', on_click=rf)


task1 = st.expander('Задание №1')
with task1:
    # st.text('Они говорят')
    tmp_task = st.session_state['task1']
    task1_id = tmp_task["id"]
    task1_name_rus = tmp_task["name_rus"]
    task1_name_eng = tmp_task["name_eng"]
    task1_name_idn = tmp_task["name_idn"]
    task1_right_answer = tmp_task["right_answer"]
    task1_hint_rus = tmp_task["hint_rus"]
    task1_hint_eng = tmp_task["hint_eng"]
    task1_hint_idn = tmp_task["hint_idn"]
    task1_answers = tmp_task["answers"]
    ls = []
    for item in task1_answers:
        if item['is_true']:
            st.session_state['right_ans_1'] = item["name_answ_rus"]
            st.session_state.update()
        ls.append(item["name_answ_rus"])
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        genre = st.radio(task1_name_rus, ls, index=None, key="user_ans_1")
    with col2:
        if st.checkbox('Показать подсказки'):
            st.markdown(f":green[{task1_right_answer}]")
            st.markdown(f":green[{task1_hint_rus}]")
            st.markdown(f":green[{task1_hint_idn}]")









