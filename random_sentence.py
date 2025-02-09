import streamlit as st
import time
import re

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

# 將單字加粗並加底線
def highlight_word(sentence, word):
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub(lambda match: f"<b><u>{match.group(0)}</u></b>", sentence)

# 顯示每個單字的 Expander 區塊
def display_word_info(row, show_chinese):
    highlighted_sentence = highlight_word(row['sentence'], row['words'])
    with st.expander(f"#### **{row['words']}**"):
        st.write(f"**句子：** {highlighted_sentence}", unsafe_allow_html=True)
        if show_chinese:
            st.write(f"**單字意思：** {row['words_ch']}")
            st.write(f"**句子翻譯：** {row['sentence_ch']}")
        st.write(f"——第{row['book']}集《{get_book_title(row['book'])}》第{row['chapter']}章：{row['title']}")


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

# 主要句子頁面
def random_sentence(df):
    st.title("📖 哈利波特單字")
    st.write("- 選擇想學的書籍，決定是否顯示中文翻譯，再點擊 **「開始」**\n"
             "- 隨機學到 5 個單字及其對應句子，幫助你熟悉原文語境。\n")

    books_selected, show_chinese = book_and_translation_selection()

    # 開始按鈕
    if not books_selected:
        st.warning("請選擇至少一本書籍才能開始練習！")
    start_disabled = not bool(books_selected)
    start_button = st.button("⏳ 開始", disabled=start_disabled)

    if start_button:
        with st.spinner("查詢中..."):
            time.sleep(0.5)
        st.markdown(
            "<div style='background-color:#d4edda; color:#155724; padding:10px; border-radius:5px;'>"
            "✅ <b>完成（請點開單字看例句）：</b></div>",
            unsafe_allow_html=True
        )

        # **篩選數據**
        filtered_df = df[df["book"].isin(books_selected)].sample(n=10, replace=True)

        # **顯示結果**
        for _, row in filtered_df.iterrows():
            display_word_info(row, show_chinese)
