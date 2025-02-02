import pandas as pd

def load_data(filepath):
    """讀取 CSV 文件並返回資料"""
    try:
        df = pd.read_csv('result.csv')
        return df
    except Exception as e:
        print(f"讀取 CSV 檔案時發生錯誤: {e}")
        return None
