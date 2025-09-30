from ai_services import LLM_Service
from prompt_templates import get_sql_generation_prompt

fake_context = """
-- Cấu trúc bảng (DDL)
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100), -- Tên của nhân viên
    salary INT, -- Lương tháng tính bằng USD
    department_id INT
);

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100) -- Tên phòng ban
);

-- SQL mẫu
-- Câu hỏi: Ai có lương cao nhất?
SELECT name FROM employees ORDER BY salary DESC LIMIT 1;
"""
fake_question = "Tên của các nhân viên trong phòng 'Sales' là gì?"

final_prompt = get_sql_generation_prompt(fake_question, fake_context)

# print("--- Thử nghiệm với Ollama ---")
# llm_ollama = LLM_Service(service_type="ollama", model_name="llama3")
# response_ollama = llm_ollama.generate(final_prompt)
# print(response_ollama)

print("\n--- Thử nghiệm với Google Gemini ---")
llm_gemini = LLM_Service(service_type="google", model_name="gemini-2.5-pro")
response_gemini = llm_gemini.generate(final_prompt)
print(response_gemini)