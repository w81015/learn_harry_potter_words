import streamlit as st
import home, random_sentence, quiz
from read_csv import load_data
import os
import dotenv

# 1. 在這裡加入 Google Analytics 追蹤碼
GA_ID = st.secrets["general"]["GA_ID"]  #使用streamlit cloud 的secrets載入
# dotenv.load_dotenv()  # 載入 .env 檔案
# GA_ID = os.getenv("GA_ID")  # 讀取 GA4 ID

# 2. 插入 GA 追蹤碼到 Streamlit
GA_SCRIPT = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}', {{ 'send_page_view': false }});

  function trackPage(page_name) {{
      gtag('event', 'page_view', {{
          'page_path': page_name
      }});
  }}
</script>
"""

st.markdown(GA_SCRIPT, unsafe_allow_html=True)

# 使用裝飾器來快取資料
@st.cache_data
def load_and_cache_data(filepath):
    return load_data(filepath)

# 讀取 CSV 資料，並使用快取
df = load_and_cache_data('result.csv')

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

        # 3. 每次切換頁面時，發送 `page_view` 事件
        st.markdown(f'<script>trackPage("/{page_name}")</script>', unsafe_allow_html=True)


    # 直接顯示可點選的按鈕
    if st.sidebar.button("功能介紹", use_container_width=True):
        switch_page("功能介紹")

    if st.sidebar.button("學習單字和句子", use_container_width=True):
        switch_page("學習單字和句子")

    if st.sidebar.button("句子填空測驗", use_container_width=True):
        switch_page("句子填空測驗")

    # 根據選擇顯示對應的頁面內容
    if st.session_state.page == "功能介紹":
        home.home_page()
    elif st.session_state.page == "學習單字和句子":
        random_sentence.random_sentence(df)
    elif st.session_state.page == "句子填空測驗":
        quiz.quiz_page(df)
    
