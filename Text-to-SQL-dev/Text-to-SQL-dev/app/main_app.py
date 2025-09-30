import streamlit as st
import pandas as pd
import requests
import json

# --- Cấu hình trang và Session State ---
st.set_page_config(
    page_title="Text To SQL Chatbot",    
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'history' not in st.session_state:
    st.session_state.history = []

# --- Hàm hiển thị kết quả từ lịch sử ---
def display_result_from_history(result_package):
    st.markdown("---")
    st.info(f"**Đang hiển thị lại kết quả cho câu hỏi:** {result_package['question']}")
    
    st.subheader("Bước 1: Kế hoạch của AI")
    with st.expander("Xem chi tiết", expanded=False):
        st.json(result_package['plan'])

    st.subheader("Bước 2: Câu lệnh SQL đã tạo")
    with st.expander("Xem chi tiết", expanded=True):
        st.code(result_package['final_sql'], language="sql")

    st.subheader("Bước 3: Kết quả Thực thi")
    st.dataframe(result_package['result_df'], use_container_width=True)
    if not result_package['result_df'].empty:
        st.bar_chart(result_package['result_df'])

# --- Giao diện Streamlit ---

# --- Thanh bên (Sidebar) ---
with st.sidebar:    
    st.image("assets/uet_logo.png", width=150)
    st.title("Text to SQL")
    st.markdown("Một trợ lý AI giúp bạn truy vấn cơ sở dữ liệu bằng ngôn ngữ tự nhiên.")
    st.markdown("---")

    st.header("1. Cấu hình Dữ liệu")
    db_choice = st.selectbox("Chọn Cơ sở dữ liệu:", ("Chinook",))

    st.markdown("---")
    st.header("2. Cấu hình AI")
    ai_service = st.selectbox("Chọn Dịch vụ AI:", ("Ollama (Local)", "Google Gemini", "OpenAI"))
    
    if ai_service == "Ollama (Local)":
        model_name = st.text_input("Model Ollama:", "llama3")
    elif ai_service == "Google Gemini":
        model_name = st.selectbox("Model Gemini:", ("gemini-1.5-pro-latest", "gemini-1.5-flash-latest"))
    else: # OpenAI
        model_name = st.selectbox("Model OpenAI:", ("gpt-4o", "gpt-4o-mini"))

    st.markdown("---")
    st.header("Lịch sử")
    if not st.session_state.history:
        st.info("Chưa có lịch sử.")
    else:
        for i, entry in enumerate(reversed(st.session_state.history)):
            if st.button(f"Q{len(st.session_state.history) - i}: {entry['question'][:30]}...", key=f"hist_{i}"):
                st.query_params["history_id"] = str(len(st.session_state.history) - 1 - i)
                st.rerun()

# --- Khu vực chính ---
st.header("Đặt câu hỏi về dữ liệu của bạn")
user_question = st.chat_input("Ví dụ: Đưa ra tất cả các users")

# --- Logic xử lý chính ---

# Xử lý xem lại lịch sử
query_params = st.query_params.to_dict()
if "history_id" in query_params:
    try:
        history_index = int(query_params["history_id"])
        if 0 <= history_index < len(st.session_state.history):            
            entry = st.session_state.history[history_index]
            if isinstance(entry['result_df'], str):
                 entry['result_df'] = pd.read_json(entry['result_df'], orient='split')
            display_result_from_history(entry)
    except (ValueError, IndexError):
        st.error("Không tìm thấy lịch sử.")
    st.query_params.clear()

# Xử lý câu hỏi mới
elif user_question:
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        status1 = st.status("**Bước 1: Lập kế hoạch...**", expanded=True)
        status2 = st.status("**Bước 2: Tạo SQL...**")
        status3 = st.status("**Bước 3: Thực thi và hiển thị kết quả...**")
        
        final_result_package = {"question": user_question}

        try:
            request_data = {
                "question": user_question,
                "db_choice": db_choice,
                "ai_service": ai_service,
                "model_name": model_name
            }
            
            s = requests.Session()
            with s.post("http://localhost:8000/stream-pipeline", json=request_data, headers=None, stream=True) as resp:
                for line in resp.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            event_data = json.loads(line_str[len('data: '):])
                            
                            if event_data.get("step") == 1:
                                plan = event_data["payload"]
                                final_result_package["plan"] = plan
                                with status1:                                    
                                    st.json(plan)
                                status1.update(label="✅ Bước 1: AI đã lập kế hoạch thành công!", state="complete", expanded=False)

                            elif event_data.get("step") == 2:
                                final_sql = event_data["payload"]
                                final_result_package["final_sql"] = final_sql
                                with status2:                                    
                                    st.code(final_sql, language="sql")
                                status2.update(label="✅ Bước 2: AI đã tạo SQL thành công!", state="complete", expanded=False)

                            elif event_data.get("step") == 3:
                                result_df_json = event_data["payload"]
                                final_result_package["result_df"] = result_df_json # Lưu dạng JSON cho session state
                                result_df = pd.read_json(result_df_json, orient='split')
                                with status3:                                    
                                    st.dataframe(result_df, use_container_width=True)                                                                                           
                                status3.update(label="✅ Bước 3: Hoàn tất!", state="complete", expanded=True)
                            
                            elif event_data.get("step") == "done":
                                st.success("Toàn bộ quá trình đã hoàn tất!")                                
                                # st.balloons()
                                break
            
            st.session_state.history.append(final_result_package)

        except Exception as e:
            st.error(f"Đã có lỗi xảy ra: {e}")

else:
    if not st.session_state.history:
        st.info("Chào mừng đến với SQL Chatbot! Hãy đặt một câu hỏi để bắt đầu.")