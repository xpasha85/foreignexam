import streamlit as st
from random import choice, shuffle
import json
import texts

#  ---------- Настройка внешнего вида меню и заголовков --------------
st.set_page_config(page_title='Экзамен для иностранных граждан', page_icon='✍')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# загружаем все задания из файлов
def load_tasks():
    for i in range(20):
        try:
            with open(f'tasks{i + 1}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                tasks_ls = data['tasks']
                task_name = data['name']
                task = choice(tasks_ls)
                st.session_state[task_name] = task
                # ---- Перемешать ответы -----
                opt = st.session_state[task_name]['options']
                shuffle(opt)
                st.session_state[task_name]['options'] = opt
                st.session_state[task_name]['disabled_task'] = False
        except FileNotFoundError as ex:
            pass


def disable_task():
    pass


def task5():
    expander = st.expander('Задание №5')
    with expander:
        tsk = st.session_state['task5']
        id = tsk['id']
        adv = tsk["adv"]
        hint = tsk["answer_hint"]
        hint_rus = tsk["hint_rus"]
        hint_eng = tsk["hint_eng"]
        hint_idn = tsk["hint_idn"]
        st.session_state['right_ans_5'] = tsk["answer"]
        with st.container(border=True, key='adv5'):
            adv = tsk["adv"]
            st.write(adv)
        st.text_input(label='111', label_visibility='hidden', key="inp_user_ans_5", disabled=st.session_state['task5']['disabled_task'])
        if st.checkbox('Показать подсказки', key='chb5'):
            st.markdown(f":green[{hint}]")
            st.markdown(f":green[{hint_rus}]")
            st.markdown(f":green[{hint_idn}]")
        if st.button('Ответить', icon='✅', disabled=st.session_state['task5']['disabled_task'],
                     on_click=disable_task, key='btn5'):
            if 'inp_user_ans_5' not in st.session_state or st.session_state['inp_user_ans_5'] is None or \
                    st.session_state['inp_user_ans_5'] == "":
                st.warning(texts.ERROR_NO_CHECK_ANSWER)
            else:
                k = str.lower(st.session_state["inp_user_ans_5"])
                st.session_state["user_ans_5"] = k
                st.session_state['task5']['disabled_task'] = True
                st.rerun()


# ------ Показать вопросы на экране --------------
def show_def_tasks(number: int, adv_enable: bool = False):
    expander = st.expander(f'Задание №{number}')
    with expander:
        tsk = st.session_state[f'task{number}']
        id = tsk['id']
        name_rus = tsk["name_rus"]
        name_eng = tsk["name_eng"]
        name_idn = tsk["name_idn"]
        hint = tsk["answer_hint"]
        hint_rus = tsk["hint_rus"]
        hint_eng = tsk["hint_eng"]
        hint_idn = tsk["hint_idn"]
        options = tsk["options"]
        st.session_state[f'right_ans_{number}'] = tsk["answer"]
        if adv_enable:
            with st.container(border=True, key=f'adv{number}'):
                adv = tsk["adv"]
                st.write(adv)
        col1, col2 = st.columns([0.4, 0.6])
        with col1:

            st.radio(name_rus, options, index=None, key=f"user_ans_{number}",
                     disabled=st.session_state[f'task{number}']['disabled_task'])
        with col2:
            if st.checkbox('Показать подсказки', key=f'chb{number}'):
                st.markdown(f":green[{hint}]")
                st.markdown(f":green[{hint_rus}]")
                st.markdown(f":green[{hint_idn}]")
        if st.button('Ответить', icon='✅', disabled=st.session_state[f'task{number}']['disabled_task'],
                     on_click=disable_task, key=f'btn{number}'):
            if f'user_ans_{number}' not in st.session_state or st.session_state[f'user_ans_{number}'] is None:
                st.warning(texts.ERROR_NO_CHECK_ANSWER)
            else:
                st.session_state[f'task{number}']['disabled_task'] = True
                st.rerun()


#  -------- Инициируем первую загрузку страницы -----------
if "first_load" not in st.session_state:
    load_tasks()
    st.session_state.first_load = True


# --------- Обновление вопросов в билетах -------------
def refresh_exam():
    st.session_state.clear()


# ---------- Начало программы -----------------
# st.write(st.session_state)
col1, col2 = st.columns(2)
with col1:
    st.subheader('Экзамен для иностранных граждан', divider=True)
with col2:
    st.button(label='Генерировать тест', icon='🔁', on_click=refresh_exam)

st.subheader('Аудирование')
st.text('Listening skills | Keterampilan mendengarkan')
show_def_tasks(1)
show_def_tasks(2)
st.subheader('Чтение')
st.text('Reading skills | Keterampilan membaca')
show_def_tasks(3, True)
show_def_tasks(4, True)
st.subheader('Письмо')
st.text('Writing skills | Keterampilan menulis')
task5()

# ---------- Задание 1 ----------------
# task1 = st.expander('Задание №1')
# with task1:
#     # st.text('Они говорят')
#     tmp_task = st.session_state['task1']
#     task1_id = tmp_task["id"]
#     task1_name_rus = tmp_task["name_rus"]
#     task1_name_eng = tmp_task["name_eng"]
#     task1_name_idn = tmp_task["name_idn"]
#     answer_hint = tmp_task["answer_hint"]
#     task1_hint_rus = tmp_task["hint_rus"]
#     task1_hint_eng = tmp_task["hint_eng"]
#     task1_hint_idn = tmp_task["hint_idn"]
#     task1_options = tmp_task["options"]
#     st.session_state['right_ans_1'] = tmp_task["answer"]
#     col1, col2 = st.columns([0.3, 0.7])
#     with col1:
#         st.radio(task1_name_rus, task1_options, index=None, key="user_ans_1",
#                  disabled=st.session_state['task1']['disabled_task'])
#     with col2:
#         if st.checkbox('Показать подсказки'):
#             st.markdown(f":green[{answer_hint}]")
#             st.markdown(f":green[{task1_hint_rus}]")
#             st.markdown(f":green[{task1_hint_idn}]")
#     if st.button('Ответить', icon='✅', disabled=st.session_state['task1']['disabled_task'], on_click=disable_task):
#         if 'user_ans_1' not in st.session_state or st.session_state['user_ans_1'] is None:
#             st.warning(texts.ERROR_NO_CHECK_ANSWER)
#         else:
#             st.session_state['task1']['disabled_task'] = True
#             st.rerun()
