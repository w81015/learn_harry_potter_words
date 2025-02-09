import streamlit as st
import time
import random

# 取得書籍名稱
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

# 產生填空題
def generate_question(df):
    row = df.sample(1).iloc[0]
    target_word = row["words"]
    sentence = row["sentence"].replace(target_word, "___")
    
    options = df[df["words"] != target_word].sample(3)["words"].tolist() + [target_word]
    random.shuffle(options)

    return {
        "sentence": sentence,
        "options": options,
        "answer": target_word,
        "sentence_ch": row["sentence_ch"],
        "words_ch": row["words_ch"],
        "book_num": row["book"],
        "chapter": row["chapter"],
        "title": row["title"]
    }

# 書籍選擇介面
def book_and_translation_selection():
    st.subheader("📚 選擇書籍 (可複選)")

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

    # 書籍選擇 (三欄顯示)
    books_selected = []
    cols = st.columns(3)
    for i, (book_num, book_name) in enumerate(books_available.items()):
        with cols[i % 3]:
            if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
                books_selected.append(book_num)

    show_chinese = st.checkbox("🔍 顯示句子的中文翻譯", value=False)

    return books_selected, show_chinese

# 初始化 session_state
def initialize_session_state():
    default_values = {
        "questions": None,
        "answers": [None] * 5,
        "score": 0,
        "reset_questions": False,
        "start_button_clicked": False,
        "books_selected": [],
        "show_chinese": False
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

# 顯示問題並處理回答
def display_questions():
    for i, q in enumerate(st.session_state.questions):
        with st.expander(f"#### 問題 {i + 1}", expanded=True):
            st.write(q["sentence"])
            st.session_state.answers[i] = st.radio(
                "選項：", q["options"], key=f"q{i}_v2", index=None
            )

            if st.session_state.show_chinese:
                st.caption(f"💡 翻譯提示：{q['sentence_ch']}")
                st.write(f"`出自第{q['book_num']}集《{get_book_title(q['book_num'])}》第{q['chapter']}章：{q['title']}`")

# 計算分數並顯示詳解
def evaluate_answers(df):
    if None in st.session_state.answers:
        st.error("還有題目沒完成喔！")
        return
    
    wrong_questions = [
        i + 1 for i, q in enumerate(st.session_state.questions) if st.session_state.answers[i] != q["answer"]
    ]
    st.session_state.score = 5 - len(wrong_questions)

    st.success(f"🎯 得分：{st.session_state.score}/5")

    with st.expander("🔍 答案", expanded=True):
        for i, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.answers[i]
            correct = user_ans == q["answer"]
            status = "✅ 答對" if correct else "❌ 答錯"
            color = "green" if correct else "red"

            st.write(f"### 第 {i+1} 題 {status}")

            st.write(f"**您的回答**：", f'<span style="color:{color}; font-weight:bold">{user_ans}</span>', unsafe_allow_html=True)
            st.write(f"**正確答案**： {q['answer']} ({q['words_ch']})")

            # st.markdown(f"**題目**： {q['sentence'].replace('___', f'**`{q['answer']}`**')}")
            answer_formatted = f"**`{q['answer']}`**"
            sentence_display = q['sentence'].replace('___', answer_formatted)
            st.markdown(f"**題目**： {sentence_display}")

            # st.write(f"**翻譯**： {q['sentence_ch'].replace(q['words_ch'], f'`{q['words_ch']}`')}")
            words_ch_formatted = f"`{q['words_ch']}`"
            sentence_ch_display = q['sentence_ch'].replace(q['words_ch'], words_ch_formatted)
            st.write(f"**翻譯**： {sentence_ch_display}")

            # 其他選項
            st.markdown("**其他選項：**", unsafe_allow_html=True)
            options_html = ""
            for opt in q["options"]:
                if opt != q["answer"]:
                    translated_word = df[df["words"] == opt]["words_ch"].iloc[0]
                    options_html += f"<span style='margin-right: 10px;'> - {opt} (<span style='font-style:bold;'>{translated_word}</span>)</span>"
            st.markdown(options_html, unsafe_allow_html=True)
            st.markdown("---")

# 主要測驗頁面
def quiz_page(df):
    st.title("📖 哈利波特填空練習")

    st.write(
        "- 選擇想學的書籍，決定是否顯示中文翻譯，再點擊 **「開始」**\n"
        "- 隨機生成 5 題四選一的單字填空題，作答完成後將提供詳解。\n"
    )

    books_selected, show_chinese = book_and_translation_selection()

    initialize_session_state()

    # 開始按鈕
    if not books_selected:
        st.warning("請選擇至少一本書籍才能開始練習！")
    start_disabled = not bool(books_selected)
    start_button = st.button("⏳ 開始測驗", disabled=start_disabled)

    if start_button:
        with st.spinner("查詢中..."):
            time.sleep(0.5)
        st.info("✅ 完成（請開始作答）：")   
        st.session_state.books_selected = books_selected
        st.session_state.show_chinese = show_chinese
        st.session_state.start_button_clicked = True
        st.session_state.reset_questions = True  

    if st.session_state.start_button_clicked:
        if st.session_state.reset_questions:
            filtered_df = df[df["book"].isin(st.session_state.books_selected)]
            st.session_state.questions = [generate_question(filtered_df) for _ in range(5)]
            st.session_state.answers = [None] * 5
            st.session_state.score = 0
            st.session_state.reset_questions = False

        display_questions()

        if st.button("📩 交卷"):
            evaluate_answers(df)

        if st.button("🔄 再測一次"):
            st.session_state.start_button_clicked = False
            st.session_state.reset_questions = True
            st.rerun()