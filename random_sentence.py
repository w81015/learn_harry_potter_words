import streamlit as st
import pandas as pd
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
    st.subheader("📚 選擇書籍 (可複選)")

    books = []
    # 全選功能
    select_all = st.checkbox("全選", value=False)

    # 使用 st.columns 來讓 checkbox 橫向顯示
    col1, col2, col3 = st.columns(3)
    # 第一行 (第1集到第3集)
    with col1:
        if st.checkbox(f"第1集：神秘的魔法石  Philosopher's Stone", value=select_all):
            books.append(1)
    with col2:
        if st.checkbox(f"第2集：消失的密室  Chamber of Secrets", value=select_all):
            books.append(2)
    with col3:
        if st.checkbox(f"第3集：阿茲卡班的逃犯  Prisoner of Azkaban", value=select_all):
            books.append(3)

    # 第二行 (第4集到第6集)
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.checkbox(f"第4集：火盃的考驗  Goblet of Fire", value=select_all):
            books.append(4)
    with col5:
        if st.checkbox(f"第5集：鳳凰會的密令  Order of the Phoenix", value=select_all):
            books.append(5)
    with col6:
        if st.checkbox(f"第6集：混血王子的背叛 Half-Blood Prince", value=select_all):
            books.append(6)

    # 第三行 (第7集)
    col7 = st.columns(3)
    with col7[0]:
        if st.checkbox(f"第7集：死神的聖物  Deathly Hallows", value=select_all):
            books.append(7)

    st.markdown("<br>", unsafe_allow_html=True)  # 增加換行


    # **是否顯示中文**
    st.subheader("🔍 是否需要中文翻譯")
    show_chinese = st.checkbox("顯示單字和句子的中文翻譯", value=False)

    st.divider()  # 增加分隔線


    # **開始按鈕**
    start_button = st.button("⏳ 開始")

    if start_button:
        with st.spinner("查詢中..."):
            time.sleep(0.5)  # 模擬等待 1 秒
        st.success("✅ 完成（請點開單字看例句）：")


    # 3. 交互式顯示（使用Expander）
    if start_button:
        if not books:
            st.warning("請至少選擇一集！")
        else:
            # **篩選數據**
            filtered_df = df[df["book"].isin(books)].sample(n=10, replace=True)

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
            # # 把英文句子中的目標單字加粗並加底線（舊的版本，沒有配對大小寫）
            # for idx, row in filtered_df.iterrows():
            #     sentence_with_bold_and_underline = row['sentence']
            #     if row['words'] in sentence_with_bold_and_underline:
            #         sentence_with_bold_and_underline = sentence_with_bold_and_underline.replace(
            #             row['words'], f"<b><u>{row['words']}</u></b>")  

                with st.expander(f"#### **{row['words']}**"):
                    st.write(f"**句子：** {sentence_with_bold_and_underline}", unsafe_allow_html=True)  # 使用 unsafe_allow_html 來顯示 HTML 標籤
                    if show_chinese:
                        st.write(f"**單字意思：** {row['words_ch']}")
                        st.write(f"**句子翻譯：** {row['sentence_ch']}")
                    st.write(f"——第{row['book']}集《{get_book_title(row['book'])}》第{row['chapter']}章：{row['title']}")


# # 以表格顯示
# if start_button:
#     if not books:
#         st.warning("請至少選擇一集書籍！")
#     else:
#         # **篩選數據**
#         filtered_df = df[df["book"].isin(books)].sample(n=5, replace=True)

#         # **根據設定顯示數據**
#         if show_chinese:
#             display_df = filtered_df[["book", "chapter", "words", "sentence", "words_ch", "sentence_ch"]]
#         else:
#             display_df = filtered_df[["book", "chapter", "words", "sentence"]]

#         # **分頁顯示數據**
#         st.write("### 顯示結果")
#         st.table(display_df)


## 2. 以卡片形式顯示
# if start_button:
#     if not books:
#         st.warning("請至少選擇一集書籍！")
#     else:
#         # **篩選數據**
#         filtered_df = df[df["book"].isin(books)].sample(n=5, replace=True)

#         # **根據設定顯示數據**
#         st.write("### 顯示結果")
#         for idx, row in filtered_df.iterrows():
#             st.markdown(f"#### 第{row['book']}集 第{row['chapter']}章")
#             st.markdown(f"**單字:** {row['words']}")
#             st.markdown(f"**英文句子:** {row['sentence']}")
#             if show_chinese:
#                 st.markdown(f"**單字中文:** {row['words_ch']}")
#                 st.markdown(f"**句子中文:** {row['sentence_ch']}")
#             st.markdown("---")

