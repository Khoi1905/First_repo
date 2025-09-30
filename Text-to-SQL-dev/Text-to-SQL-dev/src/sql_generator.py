import json
from src.utils import render_prompt, ask_llm


class SqlGenerator:
    def __init__(self, llm):
        self.llm = llm

    def select_relevant_tables(self, prompt_path: str, all_table_summaries: list, user_question: str) -> list:
        """
        Chọn ra danh sách bảng có thể liên quan đến câu hỏi từ toàn bộ tài liệu tóm tắt các bảng.
        """
        prompt = render_prompt(prompt_path, all_table_summaries, user_question)
        response_str = ask_llm(self.llm, prompt)
        try:
            return json.loads(response_str.strip())
        except Exception as e:
            print("Error parsing relevant tables output:", e, response_str)
            return []

    def analyze_tables_and_questions(self, prompt_path: str, table_descriptions: list, user_question: str,) -> str:
        """
        Phân tích bảng liên quan + truy vấn cụ thể cho từng bảng
        """
        prompt = render_prompt(prompt_path, table_descriptions, user_question)
        response_str = ask_llm(self.llm, prompt)
        try:
            return json.loads(response_str.strip())
        except Exception as e:
            print("Error parsing analyze tables and questions output:", e, response_str)
            return []
    
    def generate_sql_for_step(
        self,
        prompt_path: str,
        table_descriptions: list,
        user_question: str,
        step_requirements: list,    
        previous_sqls: list,        
        step_idx: int               
    ) -> str:
        current_step = step_requirements[step_idx]
        prev_steps = step_requirements[:step_idx]
        prev_sqls = previous_sqls[:step_idx]
        prev_context = list(zip(prev_steps, prev_sqls)) 
        prompt = render_prompt(
            prompt_path,
            table_descriptions=table_descriptions,
            user_question=user_question,
            prev_context=prev_context,
            current_step=current_step,
        )

        response_str = ask_llm(self.llm, prompt)
        return response_str.strip() 
    
    def review_plan(self):
        pass

    def final_result_review(self):
        pass

    def run(self, user_question: str) -> str:
        return "Con vịt có 4 chân"


