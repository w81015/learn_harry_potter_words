import streamlit as st
import home, random_sentence, quiz
from read_csv import load_data

# 使用裝飾器來快取資料
@st.cache_data
def load_and_cache_data(filepath):
    return load_data(filepath)

# 讀取 CSV 資料，並使用快取
df = load_and_cache_data('result.csv')  # 請使用你自己的資料路徑

# 檢查資料是否成功讀取
if df is None:
    st.error("資料讀取失敗！請檢查 CSV 檔案")
else:
    st.sidebar.title("目錄")
    # 預設頁面
    if "page" not in st.session_state:
        st.session_state.page = "功能介紹"

    # 自定義函數來切換頁面
    def switch_page(page_name):
        st.session_state.page = page_name

    # 直接顯示可點選的按鈕
    if st.sidebar.button("功能介紹", use_container_width=True):
        switch_page("功能介紹")

    if st.sidebar.button("隨機學習單字和句子", use_container_width=True):
        switch_page("隨機學習單字和句子")

    if st.sidebar.button("句子填空測驗", use_container_width=True):
        switch_page("句子填空測驗")

    # 根據選擇顯示對應的頁面內容
    if st.session_state.page == "功能介紹":
        home.home_page()
    elif st.session_state.page == "隨機學習單字和句子":
        random_sentence.random_sentence(df)
    elif st.session_state.page == "句子填空測驗":
        quiz.quiz_page(df)
    
    # # 在側邊欄中創建按鈕來選擇頁面
    # st.sidebar.title("目錄")
    # # 使用 Session State 保留頁面選擇狀態
    # if 'page' not in st.session_state:
    #     st.session_state.page = "功能介紹"  # 預設為首頁
    
    # # 這裡不需要用 button，因為這樣會觸發頁面重新加載，應該用選擇框選擇頁面
    # page = st.sidebar.radio("", ["功能介紹", "隨機學習單字和句子"], index=["功能介紹", "隨機學習單字和句子"].index(st.session_state.page))

    # # 將選擇的頁面存入 session_state
    # st.session_state.page = page

    # # 根據選擇顯示對應的頁面內容
    # if st.session_state.page == "功能介紹":
    #     home.home_page()  # 傳遞資料
    # elif st.session_state.page == "隨機學習單字和句子":
    #     random_sentence.random_sentence(df)  # 傳遞資料
    # else:
    #     st.write("請選擇一個頁面")