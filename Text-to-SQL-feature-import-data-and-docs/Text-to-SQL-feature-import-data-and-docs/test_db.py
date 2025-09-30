# test_db.py
from db_utils import list_tables, get_table, run_query, describe_table, doc_table

print("=== Danh sách bảng trong DB ===")
tables = list_tables()
print(tables)
print()

print("=== Dữ liệu mẫu từ bảng Customers (auto-correct test) ===")
print(get_table("customers", 5))
print()

print("=== Thử run_query với tên bảng sai (tracks -> Track) ===")
q = "SELECT Name, Composer, UnitPrice FROM tracks WHERE UnitPrice >= 0.99 LIMIT 5;"
print("SQL (input):", q)
print("Result:")
print(run_query(q))
print()

print("=== Schema của bảng Invoice ===")
schema = describe_table("invoice")
for row in schema:
    print(row)
print()

print("=== Doc markdown for table Track ===")
md = doc_table("tracks", 3)
print(md[:1000])  