import streamlit as st
import pandas as pd
import time
import json

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Text To SQL Chatbot",    
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- KHỞI TẠO DỮ LIỆU VÀ CÁC LỚP MÔ PHỎNG ---
TABLE_SUMMARIES = [{"id_table": "users", "description": "Chứa thông tin người dùng."}, {"id_table": "orders", "description": "Chứa thông tin đơn hàng."}]
TABLE_DESCRIPTIONS = [{"id_table": "users", "description": "Bảng người dùng chi tiết..."}, {"id_table": "orders", "description": "Bảng đơn hàng chi tiết..."}]

class FakeSqlGenerator:
    def select_relevant_tables(self, table_summaries, question):
        time.sleep(1.5)
        return {"relevant_tables": ["users", "orders"], "analysis": "Để tìm người dùng đã đặt hàng, cần kết nối bảng 'users' và 'orders'. Điều kiện lọc là 'total_amount' > 1000 từ bảng 'orders'."}

    def analyze_and_generate_sql(self, table_descriptions, question, plan):
        time.sleep(2)
        return """SELECT T1.name, T1.email
FROM users AS T1
JOIN orders AS T2 ON T1.id = T2.user_id
WHERE T2.total_amount > 1000;"""

class FakeDatabase:
    def execute_sql(self, sql_query):
        time.sleep(0.5)
        if "orders" in sql_query and "users" in sql_query:
            return pd.DataFrame({'name': ['Nguyễn Văn A', 'Lê Thị C', 'Phạm Hùng'], 'email': ['vana@example.com', 'thic@example.com', 'hungp@example.com']})
        return pd.DataFrame()

sql_generator = FakeSqlGenerator()
db = FakeDatabase()

# --- KHỞI TẠO SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- HÀM XỬ LÝ & HIỂN THỊ ---
def display_result(result_package):
    """Hàm riêng để hiển thị một gói kết quả, tránh lặp code."""
    st.markdown("---")
    st.info(f"**Đang hiển thị kết quả cho câu hỏi:** {result_package['question']}")

    # --- Trực quan hóa Bước 1 ---
    st.subheader("Bước 1: Lập Kế hoạch (AI Planner)")
    with st.expander("Xem chi tiết Kế hoạch của AI", expanded=False):
        # st.write("**Các bảng được chọn:**")
        # st.json(result_package['plan']['relevant_tables'])
        # st.write("**Phân tích của AI:**")
        # st.info(result_package['plan']['analysis'])
        st.write("**Phần này đang được ẩn**")

    # --- Trực quan hóa Bước 2 & 3 ---
    st.subheader("Bước 2: Tạo SQL (AI Synthesizer)")
    with st.expander("Xem chi tiết Câu lệnh SQL", expanded=True):
        st.code(result_package['final_sql'], language="sql")

    # --- Trực quan hóa Kết quả Cuối cùng ---
    st.subheader("Bước 3: Kết quả Thực thi")
    st.dataframe(result_package['result_df'], use_container_width=True)
    # if not result_package['result_df'].empty:
    #     st.bar_chart(result_package['result_df'])

# --- GIAO DIỆN STREAMLIT ---

# --- Thanh bên (Sidebar) ---
with st.sidebar:
    st.image("C:/Users/Admin/Downloads/Text-to-SQL-dev/Text-to-SQL-dev/assets/uet_logo.png", width=150)
    st.title("Text to SQL")
    st.markdown("Một trợ lý AI giúp bạn truy vấn cơ sở dữ liệu bằng ngôn ngữ tự nhiên.")
    st.markdown("---")

    st.header("1. Cấu hình Dữ liệu")
    db_choice = st.selectbox("Chọn Cơ sở dữ liệu:", ("Chinook (Sample)",))

    st.markdown("---")
    st.header("2. Cấu hình AI")
    ai_service = st.selectbox("Chọn Dịch vụ AI:", ("Ollama (Local)", "Google Gemini", "OpenAI"))
    
    # Phần chọn model

    st.markdown("---")
    st.header("Lịch sử")
    if not st.session_state.history:
        st.info("Chưa có lịch sử.")
    else:
        # Đảo ngược danh sách để câu hỏi mới nhất ở trên cùng
        for i, entry in enumerate(reversed(st.session_state.history)):
            # Tạo một ID duy nhất cho mỗi nút
            if st.button(f"Q{len(st.session_state.history) - i}: {entry['question'][:30]}...", key=f"hist_{i}"):
                # Khi nút được nhấn, chạy lại script và truyền tham số
                st.query_params["history_id"] = str(len(st.session_state.history) - 1 - i)
                st.rerun()

# --- Khu vực chính ---
st.header("Đặt câu hỏi về dữ liệu của bạn")
user_question = st.chat_input("Ví dụ: Lấy danh sách người dùng đã đặt hàng với tổng tiền trên 1000")

# --- Logic xử lý chính ---

# KIỂM TRA XEM CÓ CẦN HIỂN THỊ LẠI LỊCH SỬ KHÔNG
query_params = st.query_params.to_dict()
if "history_id" in query_params:
    try:
        history_index = int(query_params["history_id"])
        if 0 <= history_index < len(st.session_state.history):
            # Hiển thị kết quả cũ
            display_result(st.session_state.history[history_index])
    except (ValueError, IndexError):
        st.error("Không tìm thấy lịch sử.")
    # Xóa param để tránh bị lặp lại
    st.query_params.clear()

# NẾU CÓ CÂU HỎI MỚI
elif user_question:
    # Hiển thị câu hỏi của người dùng
    with st.chat_message("user"):
        st.markdown(user_question)

    # Vùng chứa để hiển thị quá trình suy luận
    with st.chat_message("assistant"):
        thinking_area = st.container()
        
        # BƯỚC 1: LẬP KẾ HOẠCH
        status1 = thinking_area.status("**Bước 1: Lập kế hoạch...**", expanded=True)
        with status1:
            st.write("Phân tích câu hỏi và chọn các bảng dữ liệu liên quan...")
            plan = sql_generator.select_relevant_tables(TABLE_SUMMARIES, user_question)
            status1.update(label="Bước 1: Lập kế hoạch hoàn tất!", state="complete", expanded=False)

        # BƯỚC 2: TẠO SQL
        status2 = thinking_area.status("**Bước 2: Tạo SQL...**", expanded=True)
        with status2:
            st.write("Phân tích sâu cấu trúc các bảng đã chọn để viết câu lệnh SQL...")
            relevant_descriptions = [tbl for tbl in TABLE_DESCRIPTIONS if tbl["id_table"] in plan["relevant_tables"]]
            final_sql = sql_generator.analyze_and_generate_sql(relevant_descriptions, user_question, plan)
            status2.update(label="Bước 2: Tạo SQL hoàn tất!", state="complete", expanded=False)

        # BƯỚC 3: THỰC THI
        status3 = thinking_area.status("**Bước 3: Thực thi và hiển thị kết quả...**", expanded=True)
        with status3:
            st.write("Đang chạy câu lệnh SQL trên cơ sở dữ liệu...")
            result_df = db.execute_sql(final_sql)
            status3.update(label="Bước 3: Hoàn tất!", state="complete")
        
        # Đóng gói tất cả kết quả vào một dictionary
        result_package = {
            "question": user_question,
            "plan": plan,
            "final_sql": final_sql,
            "result_df": result_df,
        }
        
        # Lưu vào lịch sử
        st.session_state.history.append(result_package)
        
        # Hiển thị kết quả vừa tạo
        display_result(result_package)

# Trang thái mặc định khi chưa có câu hỏi
else:
    if not st.session_state.history:
        st.info("Chào mừng đến với SQL Chatbot! Hãy đặt một câu hỏi để bắt đầu.")