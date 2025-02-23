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


# Глобальная переменная принимает значения idn, tha, (в дальнейшем chn)
# для выбора языка подсказок.


LANGUAGE = "tha"



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


# --------- Тестовый парсер строки с подсказкой ---------------
def parse_hint(text: str, lng="tha", prev_lng='idn'):
    ls1 = text.split('|')

    rus = ls1[0]
    th = ls1[1].split(f'({lng})')
    en = ls1[1].split('(eng)')[0]
    if len(en) > 0:
        while en[0] == ' ':
            en = en[1:]

    ls2 = th[0].split(f'({prev_lng})')
    it = ls2[-1]
    print('+', it, '+')
    if len(it) > 0:
        while it[0] in ([' ', ',', ')']) and len(it) > 1:
            it = it[1:]

    print(ls1, th, en, ls2, it, sep='\n')
    new_st = rus + ' | ' + en + ' (eng), ' + it + ' (' + lng + ')|'
    return new_st


def task5():
    expander = st.expander('Задание №5')
    with expander:
        tsk = st.session_state['task5']
        id = tsk['id']
        adv = tsk["adv"]
        hint = parse_hint(tsk["answer_hint"])
        hint_rus = tsk["hint_rus"]
        hint_eng = tsk["hint_eng"]
        hint_lng = tsk.get(f"hint_{LANGUAGE}")
        st.session_state['right_ans_5'] = tsk["answer"]
        # st.session_state["user_ans_5"] = None
        with st.container(border=True, key='adv5'):
            adv = tsk["adv"]
            st.write(adv)
        st.text_input(label='111', label_visibility='hidden', key="inp_user_ans_5",
                      disabled=st.session_state['task5']['disabled_task'])
        if st.checkbox('Показать подсказки', key='chb5'):
            st.markdown(f":green[{hint}]")
            st.markdown(f":green[{hint_rus}]")
            st.markdown(f":green[{hint_lng}]")
        if st.button('Ответить', icon='✅', disabled=st.session_state['task5']['disabled_task'],
                     on_click=disable_task, key='btn5'):
            if 'inp_user_ans_5' not in st.session_state or st.session_state['inp_user_ans_5'] is None or \
                    st.session_state['inp_user_ans_5'] == "":

                st.warning(texts.ERROR_NO_CHECK_ANSWER[LANGUAGE])
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
        hint = parse_hint(tsk["answer_hint"])
        hint_rus = tsk["hint_rus"]
        hint_eng = tsk["hint_eng"]
        hint_lng = tsk.get(f"hint_{LANGUAGE}")
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
                st.markdown(f":green[{hint_lng}]")
        if st.button('Ответить', icon='✅', disabled=st.session_state[f'task{number}']['disabled_task'],
                     on_click=disable_task, key=f'btn{number}'):
            if f'user_ans_{number}' not in st.session_state or st.session_state[f'user_ans_{number}'] is None:
                st.warning(texts.ERROR_NO_CHECK_ANSWER[LANGUAGE])
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


# ------- Проверка есть ли неотвеченные вопросы --------
def check_unchecked_tasks():
    fl = True
    for i in range(1, 21):
        if st.session_state[f'user_ans_{i}'] is None:
            fl = False
            break
        if not fl:
            fl = False
            break
    return fl


# -------- Считаем верные ответы --------------
def calc_exam():
    num_right_uns = 0
    ls = []
    if check_unchecked_tasks():

        for i in range(1, 21):
            u_uns = st.session_state[f'user_ans_{i}']
            r_uns = st.session_state[f'right_ans_{i}']
            if u_uns == r_uns:
                num_right_uns += 1
            else:
                ls.append([i, u_uns, r_uns])
            # st.write(f'Ответ юзера - "{u_uns}", правильный ответ - "{r_uns}", {num_right_uns}')
    else:
        num_right_uns = 0
        st.warning(texts.ERROR_NOT_ALL_CHECKED)
    return num_right_uns, ls


# ---------- Начало программы -----------------
# st.write(st.session_state)
col1, col2 = st.columns(2)
with col1:
    st.subheader('Экзамен для иностранных граждан', divider=True)
with col2:
    st.button(label='Генерировать тест', icon='🔁', on_click=refresh_exam)

st.subheader('Аудирование')
st.text('Listening skills')  # | Keterampilan mendengarkan')
show_def_tasks(1)
show_def_tasks(2)
st.subheader('Чтение')
st.text('Reading skills')  # | Keterampilan membaca')
show_def_tasks(3, True)
show_def_tasks(4, True)
st.subheader('Письмо')
st.text('Writing skills')  # | Keterampilan menulis')
task5()
st.subheader('Лексика и грамматика')
st.text('Vocabulary and grammar')  # | Kosakata dan tata bahasa')
show_def_tasks(6)
show_def_tasks(7)
show_def_tasks(8)
show_def_tasks(9, True)
st.subheader('ИСТОРИЯ РОССИИ')
st.text('THE HISTORY OF RUSSIA')  # | SEJARAH RUSIA')
show_def_tasks(10)
show_def_tasks(11)
show_def_tasks(12)
show_def_tasks(13)
st.session_state['right_ans_14'] = '14'
st.session_state['user_ans_14'] = '14'
st.subheader('ОСНОВЫ ЗАКОНОДАТЕЛЬСТВА РОССИЙСКОЙ ФЕДЕРАЦИИ')
st.text('FUNDAMENTALS OF THE LEGISLATION OF THE RUSSIAN FEDERATION')  # | DASAR-DASAR UNDANG-UNDANG FEDERASI RUSIA')
show_def_tasks(15, True)
show_def_tasks(16, True)
show_def_tasks(17, True)
show_def_tasks(18, True)
show_def_tasks(19, True)
show_def_tasks(20, True)
if st.button('Проверить', key='check_btn', icon='📝'):
    res, ls = calc_exam()
    color = 'green'
    if res <= 10:
        color = 'red'
    elif res <= 16:
        color = 'orange'

    if res != 0:
        st.subheader(f":{color}[Ошибок: {20 - res}]")
        if len(ls) > 0:
            for item in ls:
                st.markdown(f'№{item[0]}. Ваш ответ - {item[1]}.Правильный ответ - {item[2]}')
