import streamlit as st
import pandas as pd
import random

# 方法來根據書籍號碼取得書名（最後一行顯示）
def get_book_title(book_num):
    book_titles = {
        1: "神秘的魔法石",
        2: "消失的密室",
        3: "阿茲卡班的逃犯",
        4: "火盃的考驗",
        5: "鳳凰會的密令",
        6: "混血王子的背叛",
        7: "死神的聖物"
    }
    return book_titles.get(book_num, "未知書籍")

def generate_question(df):
    row = df.sample(1).iloc[0]
    target_word = row['words']
    sentence = row['sentence'].replace(target_word, "___")
    
    options = df[df['words'] != target_word].sample(3)['words'].tolist()
    options.append(target_word)
    random.shuffle(options)

    sentence_ch = row['sentence_ch']
    words_ch = row['words_ch']
    chapter = row['chapter']
    title = row['title']
    
    return sentence, options, target_word, sentence_ch, words_ch, row['book'], chapter, title, 


def book_and_translation_selection(df):
    st.subheader("📚 選擇書籍 (可複選)")

    # 設定可選書籍
    books_available = {
        1: "第1集：神秘的魔法石  Philosopher's Stone",
        2: "第2集：消失的密室  Chamber of Secrets",
        3: "第3集：阿茲卡班的逃犯  Prisoner of Azkaban",
        4: "第4集：火盃的考驗  Goblet of Fire",
        5: "第5集：鳳凰會的密令  Order of the Phoenix",
        6: "第6集：混血王子的背叛  Half-Blood Prince",
        7: "第7集：死神的聖物  Deathly Hallows"
    }

    # "全選" 功能
    select_all = st.checkbox("全選", value=False)

    books_selected = []
    cols = st.columns(3)  # 讓選項分成三欄顯示
    for i, (book_num, book_name) in enumerate(books_available.items()):
        with cols[i % 3]:  # 分成 3 欄
            if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
                books_selected.append(book_num)

    # 顯示是否有選擇書籍
    if not books_selected:
        st.warning("請選擇至少一本書籍才能開始練習！")

    # **是否顯示中文**
    show_chinese = st.checkbox("### **🔍 顯示句子的中文翻譯**", value=False)

    return books_selected, show_chinese


def quiz_page(df):
    st.title("📖 哈利波特填空練習")

    books_selected, show_chinese = book_and_translation_selection(df)
    
    if not books_selected:
        return

    st.markdown("<br>", unsafe_allow_html=True)

    # 初始化 session state
    required_states = ['questions', 'answers', 'score', 'reset_questions', 
                      'start_button_clicked', 'books_selected', 'show_chinese']
    for state in required_states:
        if state not in st.session_state:
            st.session_state[state] = None if state == 'questions' else False if 'clicked' in state else [] if 'books' in state else 0

    # 创建独立容器放置按钮避免布局闪动
    button_container = st.container()

    with button_container:
        if st.button("開始練習", key="start"):
            # 强制重新生成题目
            st.session_state.books_selected = books_selected
            st.session_state.show_chinese = show_chinese
            st.session_state.start_button_clicked = True
            st.session_state.reset_questions = True  # 新增这行强制重置

    if st.session_state.start_button_clicked:
        # 动态生成题目（每次点击开始都会更新）
        if st.session_state.reset_questions:
            filtered_df = df[df['book'].isin(st.session_state.books_selected)]
            st.session_state.questions = [generate_question(filtered_df) for _ in range(5)]
            st.session_state.answers = [None] * 5
            st.session_state.score = 0
            st.session_state.reset_questions = False

        # 显示问题区
        for i, (question, options, correct_answer, sentence_ch, words_ch, book_num, chapter, title) in enumerate(st.session_state.questions):
            with st.expander(f"#### 問題 {i + 1}", expanded=True):
                st.write(f"{question}")  
                answer = st.radio(
                    f"選項：",
                    options,
                    key=f"q{i}_v2",  # 修改key避免缓存问题
                    index=None  # 强制用户必须选择
                )
                st.session_state.answers[i] = answer
                if st.session_state.show_chinese:
                    st.caption(f"💡 翻譯提示：{sentence_ch}")
                    st.write(f"`出自第{book_num}集《{get_book_title(book_num)}》第{chapter}章：{title}`")


        # 提交答案区
        if st.button("📩 交卷"):
            # 检查是否有未作答题目
            if None in st.session_state.answers:
                st.error("還有題目沒完成喔！")
            else:
                # 计算得分并记录错题
                wrong_questions = []
                for i, (_, _, correct, _, _, _, _, _) in enumerate(st.session_state.questions):
                    if st.session_state.answers[i] != correct:
                        wrong_questions.append(i+1)
                
                st.session_state.score = 5 - len(wrong_questions)
                st.success(f"🎯 得分：{st.session_state.score}/5")
                
                # 显示详细解析
                with st.expander("🔍 答案", expanded=True):
                    for i, (q, opts, correct, s_ch, w_ch, bk, _, _) in enumerate(st.session_state.questions):
                        user_ans = st.session_state.answers[i]
                        status = "✅ 答對" if user_ans == correct else "❌ 答錯"
                        color = "green" if user_ans == correct else "red"
                        
                        st.write(f"### 第 {i+1} 題 {status}")
                        st.markdown(f"**題目**： {q.replace('___', f'**`{correct}`**')}")
                        st.write(f"**翻譯**： {s_ch.replace(w_ch, f'`{w_ch}`')}")
                        st.write(f"**您的回答**：", f'<span style="color:{color}; font-weight:bold">{user_ans}</span>', unsafe_allow_html=True)
                        st.write(f"**正確答案**： {correct}")
                        st.write(f"**單字解釋**： {w_ch}")
                        
                        
                        # # 显示选项分布
                        st.markdown("**其他選項：**", unsafe_allow_html=True)
                        options_html = ""
                        for opt in opts:
                            if opt != correct:
                                translated_word = df[df['words'] == opt]['words_ch'].iloc[0]
                                options_html += f"<span style='margin-right: 10px;'> - {opt} (<span style='font-style:bold;'>{translated_word}</span>)</span>"
                        st.markdown(options_html, unsafe_allow_html=True)
                        st.markdown("---")
                        # st.markdown("**其他選項：**")
                        # for opt in opts:
                        #     if opt != correct:
                        #         # 从 DataFrame 中获取选项的中文翻译
                        #         translated_word = df[df['words'] == opt]['words_ch'].iloc[0]
                        #         st.markdown(f"- {opt}  {translated_word}")
                        # st.markdown("---")

        # 重置按钮
        if st.button("🔄 再測一次"):
            st.session_state.start_button_clicked = False
            st.session_state.reset_questions = True
            st.rerun()



# import streamlit as st
# import pandas as pd
# import random


# def generate_question(df):
#     row = df.sample(1).iloc[0]
#     target_word = row['words']
#     sentence = row['sentence'].replace(target_word, "___")
    
#     options = df[df['words'] != target_word].sample(3)['words'].tolist()
#     options.append(target_word)
#     random.shuffle(options)

#     sentence_ch = row['sentence_ch']
#     words_ch = row['words_ch']
    
#     return sentence, options, target_word, sentence_ch, words_ch, row['book']


# def book_and_translation_selection(df):
#     st.subheader("📚 選擇書籍 (可複選)")

#     # 設定可選書籍
#     books_available = {
#         1: "第1集：神秘的魔法石  Philosopher's Stone",
#         2: "第2集：消失的密室  Chamber of Secrets",
#         3: "第3集：阿茲卡班的逃犯  Prisoner of Azkaban",
#         4: "第4集：火盃的考驗  Goblet of Fire",
#         5: "第5集：鳳凰會的密令  Order of the Phoenix",
#         6: "第6集：混血王子的背叛  Half-Blood Prince",
#         7: "第7集：死神的聖物  Deathly Hallows"
#     }

#     # "全選" 功能
#     select_all = st.checkbox("全選", value=False)

#     books_selected = []
#     cols = st.columns(3)  # 讓選項分成三欄顯示
#     for i, (book_num, book_name) in enumerate(books_available.items()):
#         with cols[i % 3]:  # 分成 3 欄
#             if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
#                 books_selected.append(book_num)

#     # 顯示是否有選擇書籍
#     if not books_selected:
#         st.warning("請選擇至少一本書籍才能開始練習！")

#     # **是否顯示中文**
#     show_chinese = st.checkbox("### **🔍 顯示句子的中文翻譯**", value=False)

#     return books_selected, show_chinese


# def quiz_page(df):
#     st.title("📖 哈利波特填空練習")

#     books_selected, show_chinese = book_and_translation_selection(df)
    
#     if not books_selected:
#         return

#     st.markdown("<br>", unsafe_allow_html=True)  # 增加換行

#     # Initialize session state variables if they don't exist
#     if 'questions' not in st.session_state:
#         st.session_state.questions = None
#     if 'answers' not in st.session_state:
#         st.session_state.answers = None
#     if 'score' not in st.session_state:
#         st.session_state.score = 0
#     if 'reset_questions' not in st.session_state:
#         st.session_state.reset_questions = False
#     if 'start_button_clicked' not in st.session_state:
#         st.session_state.start_button_clicked = False
#     if 'books_selected' not in st.session_state:
#         st.session_state.books_selected = books_selected
#     if 'show_chinese' not in st.session_state:
#       st.session_state.show_chinese = show_chinese

#     # 按下 Start 按鈕後才顯示問題
#     if st.button("開始練習", key="start"):
#         # 透過 session_state 保存選擇的書籍和中文選項
#         st.session_state.books_selected = books_selected
#         st.session_state.show_chinese = show_chinese
#         st.session_state.start_button_clicked = True

#         # 篩選資料
#         filtered_df = df[df['book'].isin(st.session_state.books_selected)]

#         if st.session_state.questions is None or st.session_state.reset_questions:
#             st.session_state.questions = [generate_question(filtered_df) for _ in range(5)]
#             st.session_state.answers = [None] * 5
#             st.session_state.score = 0
#             st.session_state.reset_questions = False  # 重設為 False
    
#     if st.session_state.start_button_clicked:
#         for i, (question, options, correct_answer, sentence_ch, words_ch, book_num) in enumerate(st.session_state.questions):
#             with st.expander(f"#### **問題 {i + 1}** (第{book_num}集)", expanded=True):
#                 st.write(question)
#                 answer = st.radio(f"選擇填入的單字 (問題 {i + 1}):", options, key=f"q{i}")
#                 st.session_state.answers[i] = answer
#                 if st.session_state.show_chinese:
#                     st.write(f"**句子翻譯：** {sentence_ch}")

#         if st.button("提交所有答案"):
#             st.session_state.score = sum(
#                 1 for i, (_, _, correct_answer, _, _, _) in enumerate(st.session_state.questions)
#                 if st.session_state.answers[i] == correct_answer
#             )
#             st.success(f"✅ 你的總分是: {st.session_state.score} / 5")

#             # 顯示每題的正確答案和翻譯
#             st.subheader("正確答案與翻譯")
#             for i, (question, _, correct_answer, sentence_ch, words_ch, book_num) in enumerate(st.session_state.questions):
#                 st.write(f"**問題 {i + 1}**")
#                 st.write(f"正確答案：{correct_answer}")
#                 st.write(f"單字翻譯：{words_ch}")
#                 st.write(f"題目：{question}")

#         st.markdown("<br>", unsafe_allow_html=True)  # 增加換行

#         # 增加一個按鈕來重置問題
#         if st.button("再試一次"):
#             st.session_state.reset_questions = True
#             st.session_state.start_button_clicked = False # reset this state
#             st.rerun()



# # 第1版
# import streamlit as st
# import pandas as pd
# import random
# import time


# def generate_question(df):
#     row = df.sample(1).iloc[0]
#     target_word = row['words']
#     sentence = row['sentence'].replace(target_word, "___")
    
#     options = df[df['words'] != target_word].sample(3)['words'].tolist()
#     options.append(target_word)
#     random.shuffle(options)

#     sentence_ch = row['sentence_ch']
#     words_ch = row['words_ch']
    
#     return sentence, options, target_word, sentence_ch, words_ch, row['book']


# def quiz_page(df):
#     st.title("📖 哈利波特填空練習")
    
#     st.subheader("📚 選擇書籍 (可複選)")
    
#     # 設定可選書籍
#     books_available = {
#         1: "第1集：神秘的魔法石  Philosopher's Stone",
#         2: "第2集：消失的密室  Chamber of Secrets",
#         3: "第3集：阿茲卡班的逃犯  Prisoner of Azkaban",
#         4: "第4集：火盃的考驗  Goblet of Fire",
#         5: "第5集：鳳凰會的密令  Order of the Phoenix",
#         6: "第6集：混血王子的背叛  Half-Blood Prince",
#         7: "第7集：死神的聖物  Deathly Hallows"
#     }

#     # "全選" 功能
#     select_all = st.checkbox("全選", value=False)

#     books_selected = []
#     cols = st.columns(3)  # 讓選項分成三欄顯示
#     for i, (book_num, book_name) in enumerate(books_available.items()):
#         with cols[i % 3]:  # 分成 3 欄
#             if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
#                 books_selected.append(book_num)
    
#     if not books_selected:
#         st.warning("請選擇至少一本書籍才能開始練習！")
#         return

#     st.markdown("<br>", unsafe_allow_html=True)  # 增加換行


#     # **是否顯示中文**
#     show_chinese = st.checkbox("### **🔍 顯示句子的中文翻譯**", value=False)



#     filtered_df = df[df['book'].isin(books_selected)]

#     if 'questions' not in st.session_state or st.session_state.get('reset_questions', False):
#         st.session_state.questions = [generate_question(filtered_df) for _ in range(5)]
#         st.session_state.answers = [None] * 5
#         st.session_state.score = 0
#         st.session_state.reset_questions = False  # 重設為 False
    
#     for i, (question, options, correct_answer, sentence_ch, words_ch, book_num) in enumerate(st.session_state.questions):
#         with st.expander(f"#### **問題 {i + 1}** (第{book_num}集)", expanded=True):
#             st.write(question)
#             answer = st.radio(f"選擇填入的單字 (問題 {i + 1}):", options, key=f"q{i}")
#             st.session_state.answers[i] = answer
#             if show_chinese:
#                 st.write(f"**句子翻譯：** {sentence_ch}")
    
#     if st.button("提交所有答案"):
#         st.session_state.score = sum(
#             1 for i, (_, _, correct_answer, _, _, _) in enumerate(st.session_state.questions)
#             if st.session_state.answers[i] == correct_answer
#         )
#         st.success(f"✅ 你的總分是: {st.session_state.score} / 5")

#         # 顯示每題的正確答案和翻譯
#         st.subheader("正確答案與翻譯")
#         for i, (question, _, correct_answer, sentence_ch, words_ch, book_num) in enumerate(st.session_state.questions):
#             st.write(f"**問題 {i + 1}**")
#             st.write(f"正確答案：{correct_answer}")
#             st.write(f"句子翻譯：{words_ch}")

#     st.markdown("<br>", unsafe_allow_html=True)  # 增加換行

#     # 增加一個按鈕來重置問題
#     if st.button("再試一次"):
#         st.session_state.reset_questions = True
#         st.rerun()


