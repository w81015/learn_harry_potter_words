import streamlit as st
import time
import re

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


def random_sentence(df):
    st.title("📖 哈利波特單字")
    
    st.write("- 選擇想學的書籍，決定是否顯示中文翻譯，再點擊 **「開始」**\n"
    "- 隨機學到 5 個單字及其對應句子，幫助你熟悉原文語境。\n\n")

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

    # 是否顯示中文
    show_chinese = st.checkbox("### **🔍 顯示中文翻譯**", value=False)

    st.divider()  # 增加分隔線

    # 開始按鈕
    start_button = st.button("⏳ 開始")

    if start_button:
        with st.spinner("查詢中..."):
            time.sleep(0.5)  # 模擬等待 1 秒
        st.success("✅ 完成（請點開單字看例句）：")


    # 3. 交互式顯示（使用Expander）
    if start_button:
        if not books_selected:
            st.warning("請至少選擇一集！")
        else:
            # **篩選數據**
            filtered_df = df[df["book"].isin(books_selected)].sample(n=10, replace=True)

            # **根據設定顯示數據**
            # st.write("### 顯示結果")
            for idx, row in filtered_df.iterrows():
                sentence_with_bold_and_underline = row['sentence']  # 把英文句子中的目標單字加粗並加底線（配對大小寫）
                word_to_replace = row['words']
                # 使用正則表達式不區分大小寫進行匹配
                pattern = re.compile(re.escape(word_to_replace), re.IGNORECASE)
                # 使用 re.sub 替換找到的匹配字，並保持原始字母大小寫
                sentence_with_bold_and_underline = pattern.sub(
                    lambda match: f"<b><u>{match.group(0)}</u></b>", 
                    sentence_with_bold_and_underline
                )

                with st.expander(f"#### **{row['words']}**"):
                    st.write(f"**句子：** {sentence_with_bold_and_underline}", unsafe_allow_html=True)
                    if show_chinese:
                        st.write(f"**單字意思：** {row['words_ch']}")
                        st.write(f"**句子翻譯：** {row['sentence_ch']}")
                    st.write(f"——第{row['book']}集《{get_book_title(row['book'])}》第{row['chapter']}章：{row['title']}")

