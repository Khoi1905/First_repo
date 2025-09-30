from llm.llm_integrations import get_llm
from sql_generator import SqlGenerator
from utils import ask_llm, render_prompt


sql_generator = SqlGenerator(get_llm())
question = "Lấy danh sách tất cả người dùng đã đặt hàng với tổng tiền trên 1000."

print(sql_generator.run(question))
