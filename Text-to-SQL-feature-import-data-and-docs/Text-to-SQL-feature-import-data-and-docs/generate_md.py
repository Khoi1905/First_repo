from db_utils import list_tables, export_table
tables = list_tables()
# Test từng bảng: xuất Markdown vào docs/
for table in tables:
    export_table(table)  # tự ghi file docs/<table>.md
