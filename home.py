import streamlit as st

def home_page():
    # Streamlit UI
    st.title("🧙‍♂️讀哈利波特學英文🧙‍♂️")

    # **說明文字**
    st.write(
    "歡迎來到哈利波特的魔法學習空間！🪄\n\n"
    "在這裡，你可以挑戰自己學習更多英文詞彙，透過兩種學習模式提升你的語言能力！\n\n"
    "### 📖 隨機學習單字和句子\n"
    "- 選擇想學的書籍，決定是否顯示中文翻譯，然後點擊 「開始」，\n"
    "- 隨機學到 5 個單字及其對應句子，幫助你熟悉原文語境。\n\n"
    "### ✍️ 句子填空測驗\n"
    "- 挑戰自己對於句子內容的理解，透過四選一的填空題檢驗對單字的理解。\n"
    "- 隨機生成5個題目，作答完成後將提供詳解。\n\n"
    "準備好成為一個魔法英文高手了嗎？\n"
    "點選下方（或側邊欄）的頁面到各個功能！"
    )

    col1, col2= st.columns(2)
    with col1:
        # 連結到 "學習單字和句子" 頁面
        if st.button("前往學習單字和句子", key="to_random_sentence", use_container_width=True):
            st.session_state.page = "學習單字和句子"
            st.rerun()  # 重新執行以刷新頁面

    with col2:
        # 連結到 "句子填空測驗" 頁面
        if st.button("前往句子填空測驗", key="to_quiz", use_container_width=True):
            st.session_state.page = "句子填空測驗"
            st.rerun()

    st.markdown("---")