import streamlit as st
import home, random_sentence, quiz
from read_csv import load_data

# 1️⃣ 嘗試載入 GA_ID，避免 KeyError
GA_ID = st.secrets["general"].get("GA_ID", None)

# 確保 GA_ID 存在
if GA_ID and GA_ID.startswith("G-"):
    GA_SCRIPT = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      // 啟用 GA4 追蹤
      gtag('config', '{GA_ID}');

      // 手動觸發頁面瀏覽追蹤
      function trackPage(page_name) {{
          gtag('event', 'page_view', {{
              'page_path': page_name
          }});
      }}

      // 自動追蹤首頁
      setTimeout(() => trackPage(window.location.pathname), 1000);
    </script>
    """

    # **使用 st.components.v1.html 來確保 JavaScript 正確載入**
    st.components.v1.html(GA_SCRIPT, height=0)
else:
    st.warning("未設定 Google Analytics ID，請在 Streamlit Secrets 設定 GA_ID。")

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
        st.session_state.page = page_name
        # 3️⃣ 確保 GA4 追蹤 `page_view`
        st.components.v1.html(f"<script>trackPage('/{page_name}');</script>", height=0)

    # 頁面按鈕
    if st.sidebar.button("功能介紹", use_container_width=True):
        switch_page("功能介紹")

    if st.sidebar.button("學習單字和句子", use_container_width=True):
        switch_page("學習單字和句子")

    if st.sidebar.button("句子填空測驗", use_container_width=True):
        switch_page("句子填空測驗")

    # 顯示對應的頁面內容
    if st.session_state.page == "功能介紹":
        home.home_page()
    elif st.session_state.page == "學習單字和句子":
        random_sentence.random_sentence(df)
    elif st.session_state.page == "句子填空測驗":
        quiz.quiz_page(df)
