import streamlit as st
import time
from gtts import gTTS
import io

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

    return {
        "sentence": sentence,
        "sentence_with_answer": row["sentence"],
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

    # 書籍選擇 (兩欄顯示，分為1-4集與5-7集)
    books_selected = []
    cols = st.columns(2)

    # 第一欄 (顯示1-4集)
    with cols[0]:
        for i, (book_num, book_name) in enumerate(books_available.items()):
            if book_num <= 4:
                if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
                    books_selected.append(book_num)

    # 第二欄 (顯示5-7集)
    with cols[1]:
        for i, (book_num, book_name) in enumerate(books_available.items()):
            if book_num >= 5:
                if st.checkbox(book_name, value=select_all, key=f"book_{book_num}"):
                    books_selected.append(book_num)

    show_chinese = st.checkbox("🔍 顯示句子的中文翻譯", value=False)
    
    return books_selected, show_chinese

# 初始化 session_state
def initialize_session_state():
    default_values = {"question": None, "user_answer": "", "score": 0, "start_button_clicked": False, "books_selected": [], "show_chinese": False}
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

# 顯示問題並播放語音
def display_questions():
    qq = st.session_state.question
    st.write(qq["sentence"])

    # 產生語音並存到記憶體
    tts = gTTS(text=qq["sentence_with_answer"], lang="en")
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)  # 重置指標以便播放

    # 顯示音訊播放器
    st.audio(audio_bytes, format="audio/mp3")

    # 顯示輸入框讓使用者回答
    st.session_state.user_answer = st.text_input(f"請填空：", key=f"user_input")

    if st.session_state.show_chinese:
        st.caption(f"💡 翻譯提示：{qq['sentence_ch']}")
        st.write(f"`出自第{qq['book_num']}集《{get_book_title(qq['book_num'])}》第{qq['chapter']}章：{qq['title']}`")

# 計算分數並顯示詳解
def evaluate_answers():
    if not st.session_state.user_answer:
        st.error("請填寫答案後再提交！")
        return
    
    qq = st.session_state.question
    correct = st.session_state.user_answer.strip().lower() == qq["answer"].strip().lower()
    st.session_state.score = 1 if correct else 0
    
    status = "✅ 答對" if correct else "❌ 答錯"
    color = "green" if correct else "red"
    
    st.markdown(f"### {status}")

    # st.markdown(f"**題目**： {q['sentence'].replace('___', f'**`{q['answer']}`**')}")
    answer_formatted = f"**`{qq['answer']}`**"
    sentence_display = qq['sentence'].replace('___', answer_formatted)
    st.markdown(f"**題目**： {sentence_display}")

    st.write(f"**翻譯**： {qq['sentence_ch']}")
    st.write(f"**您的回答**：", f'<span style="color:{color}; font-weight:bold">{st.session_state.user_answer}</span>', unsafe_allow_html=True)
    st.write(f"**正確答案**： {qq['answer']}")
    st.write(f"**單字解釋**： {qq['words_ch']}")
    
# 主要測驗頁面
def listening_page(df):
    st.title("📖 哈利波特聽力練習")
    st.write("- 選擇想學的書籍，決定是否顯示中文翻譯，再點擊 **「開始」**\n- 隨機生成 1 題聽力填空練習，作答完成後將提供答案。")
    
    books_selected, show_chinese = book_and_translation_selection()
    initialize_session_state()
    
    if not books_selected:
        st.warning("請選擇至少一本書籍才能開始練習！")
    start_disabled = not bool(books_selected)
    start_button = st.button("⏳ 開始測驗", disabled=start_disabled)
    
    if start_button:
        with st.spinner("查詢中..."):
            time.sleep(1)
        st.info("✅ 完成（請開始作答）：")
        st.session_state.books_selected = books_selected
        st.session_state.show_chinese = show_chinese
        st.session_state.start_button_clicked = True
        st.session_state.question = generate_question(df[df["book"].isin(books_selected)])
        st.session_state.user_answer = ""
    
    if st.session_state.start_button_clicked:
        display_questions()
        if st.button("📩 交卷"):
            evaluate_answers()
        if st.button("🔄 再測一次"):
            st.session_state.start_button_clicked = False
            st.rerun()
