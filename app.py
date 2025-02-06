import streamlit as st
import home, random_sentence, quiz
from read_csv import load_data

from bs4 import BeautifulSoup
import shutil
import pathlib
import logging

def inject_ga():

    # new tag method
    GA_ID = "G-02NL6W1HZJ"
    GA_JS = """
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-02NL6W1HZJ"> id="google_analytics" </script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-02NL6W1HZJ');
</script>
"""
    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="lxml")
    if not soup.find(id=GA_ID):  # if cannot find tag
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)

inject_ga()

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
