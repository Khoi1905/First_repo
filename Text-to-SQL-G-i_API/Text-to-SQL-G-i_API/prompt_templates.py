def get_sql_generation_prompt(question: str, context: str) -> str:
    """
    Tạo prompt hoàn chỉnh để sinh SQL, dựa trên kiến trúc RAG của Vanna.
    - question: Câu hỏi của người dùng.
    - context: Thông tin liên quan (DDL, docs, SQL mẫu) được tìm thấy từ Vector DB.
    """
    
    prompt = f"""Bạn là một chuyên gia SQL. Dựa vào thông tin cấu trúc bảng, tài liệu và các ví dụ dưới đây, hãy viết một câu lệnh SQL duy nhất, chính xác để trả lời câu hỏi của người dùng.
Chỉ trả về câu lệnh SQL và không có gì khác.
Thông tin ngữ cảnh:
{context}
Câu hỏi:
{question}
SQL:
"""
    return prompt
