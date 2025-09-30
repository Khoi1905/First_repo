import json
from utils import render_prompt, ask_llm
from z import get_all_table_summaries, get_table_details


class SqlGenerator:
    def __init__(self, llm):
        self.llm = llm

    def select_relevant_tables(self, all_table_summaries: list, user_question: str) -> list:
        """
        Chọn ra danh sách bảng có thể liên quan đến câu hỏi từ toàn bộ tài liệu tóm tắt các bảng.
        """
        prompt = render_prompt("prompts/0_select_relevant_tables.txt", table_summaries=all_table_summaries, question=user_question)
        response_str = ask_llm(self.llm, prompt)
        try:
            return json.loads(response_str.strip())
        except Exception as e:
            print("Error parsing relevant tables output:", e, response_str)
            return []

    def analyze_tables_and_questions(self, table_descriptions: list, user_question: str,) -> str:
        """
        Phân tích bảng liên quan + truy vấn cụ thể cho từng bảng
        """
        prompt = render_prompt("prompts/1_analyze_tables_and_questions.txt", table_descriptions=table_descriptions, question=user_question)
        response_str = ask_llm(self.llm, prompt)
        try:
            return json.loads(response_str.strip())
        except Exception as e:
            print("Error parsing analyze tables and questions output:", e, response_str)
            return []
    
    def review_plan(self, user_question: str, relevant_tables_details: list, step_requirements: list) -> list:
        """
        Xem xét và điều chỉnh kế hoạch thực hiện dựa trên câu hỏi của người dùng và các bảng liên quan.
        """
        prompt = render_prompt("prompts/2_review_plan.txt", user_question=user_question, relevant_tables=relevant_tables_details, step_requirements=step_requirements)
        response_str = ask_llm(self.llm, prompt)
        try:
            return json.loads(response_str.strip())
        except Exception as e:
            print("Error parsing review plan output:", e, response_str)
            return []
    
    def generate_sql_for_step(
        self,
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
            "prompts/3_generate_sql_for_step.txt",
            table_descriptions=table_descriptions,
            user_question=user_question,
            prev_context=prev_context,
            current_step=current_step,
        )

        response_str = ask_llm(self.llm, prompt)
        return response_str.strip() 

    def final_result_review(self, user_question: str, table_descriptions: list, step_requirements: list, step_sqls: list) -> str:
        step_sql_pairs = list(zip(step_requirements, step_sqls))
        prompt = render_prompt("prompts/4_final_result_review.txt", user_question=user_question, table_descriptions=table_descriptions, combined=step_sql_pairs)
        response_str = ask_llm(self.llm, prompt)
        return response_str.strip()

    def run(self, user_question: str):
        # Lấy tóm tắt ngắn gọn về các bảng trong database
        table_summaries = get_all_table_summaries()

        # Chọn ra các bảng có thể liên quan đến câu hỏi
        relevant_tables = self.select_relevant_tables(table_summaries, user_question)
        
        # Lấy mô tả chi tiết các bảng liên quan
        relevant_tables_details = get_table_details(relevant_tables)

        # Phân tích các bảng và câu hỏi người dùng, lên kế hoạch thực hiện theo từng bước
        step_requirements = self.analyze_tables_and_questions(relevant_tables_details, user_question)
        
        # Đánh giá, cải tiến kế hoạch thực hiện
        step_requirements = self.review_plan(user_question, relevant_tables_details, step_requirements)
        
        # Sinh SQL theo từng bước
        step_sqls = []
        for i in range(len(step_requirements)):
            sql = self.generate_sql_for_step(get_table_details(step_requirements[i]["used_tables"]), user_question, step_requirements, step_sqls, i)
            step_sqls.append(sql)

        print(step_sqls[-1])

        # Đánh giá lại toàn bộ quá trình, kết quả. Cuối cùng trả về kết quả cho người dùng
        final_output = self.final_result_review(user_question, relevant_tables_details, step_requirements, step_sqls)
        return final_output