import subprocess
import threading
import time

def run_backend():
    """Chạy server FastAPI."""
    print("--- Khởi động Backend Server tại http://localhost:8000 ---")
    try:
        subprocess.run(["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"])
    except FileNotFoundError:
        print("\n!!! LỖI: Lệnh 'uvicorn' không được tìm thấy.")
        print("Vui lòng kích hoạt môi trường conda ('conda activate text_to_sql_env') và cài đặt ('pip install uvicorn').\n")


def run_frontend():
    """Chạy giao diện Streamlit."""
    print("--- Khởi động Frontend UI tại http://localhost:8501 ---")
    try:
        subprocess.run(["streamlit", "run", "app/main_app.py", "--server.port", "8501"])
    except FileNotFoundError:
        print("\n!!! LỖI: Lệnh 'streamlit' không được tìm thấy.")
        print("Vui lòng kích hoạt môi trường conda ('conda activate text_to_sql_env') và cài đặt ('pip install streamlit').\n")

if __name__ == "__main__":    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    print("Đợi backend khởi động trong vài giây...")
    time.sleep(5)
    
    run_frontend()