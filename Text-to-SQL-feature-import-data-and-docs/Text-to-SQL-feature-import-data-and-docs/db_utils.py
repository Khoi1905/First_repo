import os
import sqlite3
import pandas as pd
import difflib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Data", "chinook.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
#Dùng cấu trúc try/finally để đóng hàm nếu có lỗi
def get_table(table_name: str, limit: int = 10) -> pd.DataFrame:
    conn = get_connection()
    try:
        table_name = normalize_table_name(table_name)  #trả tên chuẩn nếu sai
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
    finally:
        conn.close()
    return df

#sql
def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        tables = list_tables()
        mapping = {t.lower(): t for t in tables}
        for lower_name, proper_name in mapping.items():
            query = query.replace(lower_name, proper_name)
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return df

#list bảng 
def list_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

#cấu trúc
def describe_table(table_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    conn.close()
    return schema

#chuẩn hóa
def normalize_table_name(name: str) -> str:
    tables = list_tables()
    mapping = {t.lower(): t for t in tables}
    key = name.lower()
    if key in mapping:
        return mapping[key]
    import difflib
    suggestion = difflib.get_close_matches(name, tables, n=1)
    if suggestion:
        print(f"[INFO] Bảng '{name}' không tồn tại. Dùng '{suggestion[0]}' thay thế.")
        return suggestion[0]  
    raise ValueError(f"Bảng '{name}' không tồn tại. Các bảng hiện có: {tables}")

#import csv vào 
def import_csv_to_db(csv_path: str, table_name: str, if_exists: str = "replace"):
  #  - if_exists: 'replace' để ghi đè, 'append' để thêm
    conn = get_connection()
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        print(f"[INFO] Đã import {len(df)} dòng vào bảng '{table_name}'.")
    finally:
        conn.close()
        
#sinh markdown
def doc_table(table_name: str, sample_limit: int = 5) -> str:
    schema = describe_table(table_name)
    sample = get_table(table_name, limit=sample_limit)

    md = [f"## Bảng: {table_name}", "### Schema:"]
    for col in schema:
        cid, name, ctype, notnull, dflt, pk = col
        md.append(f"- {name} ({ctype}){' [PK]' if pk else ''}")

    md.append("\n### Sample Data:")
    md.append(sample.to_markdown(index=False))

    return "\n".join(md)
#tạo file sau khi sinh
def export_table(table_name: str, sample_limit: int = 5):
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCS_DIR = os.path.join(BASE_DIR, "docs")
    os.makedirs(DOCS_DIR, exist_ok=True)  # tạo folder nếu chưa tồn tại

    md_content = doc_table(table_name, sample_limit=sample_limit)
    md_file = os.path.join(DOCS_DIR, f"{table_name}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[INFO] Đã ghi Markdown bảng '{table_name}' vào {md_file}")