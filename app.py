import streamlit as st
import home, random_sentence, quiz, listening
from read_csv import load_data


# 1️⃣ 嘗試載入 GA_ID，避免 KeyError
GA_ID = st.secrets["general"].get("GA_ID", None)

# 確保 GA_ID 存在
# 讀取 HTML 檔案
with open('ga_script.html', 'r') as file:
    GA_SCRIPT = file.read()
        
# 替換 GA_ID 位置
GA_SCRIPT = GA_SCRIPT.replace("{{GA_ID}}", GA_ID)

# 使用 st.components.v1.html 來確保 JavaScript 正確載入
st.components.v1.html(GA_SCRIPT, height=0)

# 2️⃣ 快取 CSV 資料
@st.cache_data
def load_and_cache_data(filepath):
    return load_data(filepath)

df = load_and_cache_data('result.csv')

if df is None:
    st.error("資料讀取失敗！請檢查 CSV 檔案")
else:
    st.sidebar.title("目錄")

    if "page" not in st.session_state:
        st.session_state.page = "功能介紹"

    def switch_page(page_name):
        st.session_state.clear()  # 清除所有 session_state 變數
        st.session_state.page = page_name

    # 頁面按鈕
    if st.sidebar.button("功能介紹", use_container_width=True):
        switch_page("功能介紹")

    if st.sidebar.button("學習單字和句子", use_container_width=True):
        switch_page("學習單字和句子")

    if st.sidebar.button("句子填空測驗", use_container_width=True):
        switch_page("句子填空測驗")

    if st.sidebar.button("聽力填空測驗", use_container_width=True):
        switch_page("聽力填空測驗")

    # 顯示對應的頁面內容
    if st.session_state.page == "功能介紹":
        home.home_page() # 在home.py的def home_page()
    elif st.session_state.page == "學習單字和句子":
        random_sentence.random_sentence(df)
    elif st.session_state.page == "句子填空測驗":
        quiz.quiz_page(df)
    elif st.session_state.page == "聽力填空測驗":
        listening.listening_page(df)