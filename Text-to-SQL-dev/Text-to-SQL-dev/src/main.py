from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import time
import json
import asyncio
from fastapi.responses import StreamingResponse

# --- Định nghĩa mô hình dữ liệu cho request ---
class ChatRequest(BaseModel):
    question: str
    db_choice: str
    ai_service: str
    model_name: str

# --- Lớp mô phỏng logic Backend ---
# Phần tích hợp các lớp thật của a khôi ở đây
class FakeBackendLogic:
    async def run_step_1_planner(self, request: ChatRequest):
        print(f"Backend - Bước 1: Lập kế hoạch cho câu hỏi '{request.question}'...")
        await asyncio.sleep(1)
        plan = {
            "relevant_tables": ["users", "orders"],
            "analysis": "Để tìm người dùng đã đặt hàng, cần kết nối bảng 'users' và 'orders'. Điều kiện lọc là 'total_amount' > 1000 từ bảng 'orders'."
        }
        print("Backend - Bước 1: Hoàn thành.")
        return plan

    async def run_step_2_sql_gen(self, request: ChatRequest, plan):
        print("Backend - Bước 2: Tạo SQL...")
        await asyncio.sleep(1)
        final_sql = """SELECT T1.name, T1.email
FROM users AS T1
JOIN orders AS T2 ON T1.id = T2.user_id
WHERE T2.total_amount > 1000;"""
        print("Backend - Bước 2: Hoàn thành.")
        return final_sql

    async def run_step_3_execution(self, sql_query: str):
        print("Backend - Bước 3: Thực thi SQL...")
        await asyncio.sleep(1)
        result_df = pd.DataFrame({
            'Name': ['Nguyễn Văn A', 'Lê Thị C', 'Phạm Hùng'],
            'email': ['vana@example.com', 'thic@example.com', 'hungp@example.com']
        })
        print("Backend - Bước 3: Hoàn thành.")
        return result_df

# --- Khởi tạo ứng dụng FastAPI và các đối tượng logic ---
app = FastAPI(title="SQL Cortex Backend")
backend_logic = FakeBackendLogic()

# --- Định nghĩa API Endpoint Streaming ---
@app.post("/stream-pipeline")
async def handle_streaming_request(request: ChatRequest):
    
    async def event_stream():
        """Hàm generator sẽ gửi (yield) các sự kiện về cho frontend."""
        
        # --- BƯỚC 1: LẬP KẾ HOẠCH ---
        plan = await backend_logic.run_step_1_planner(request)
        event_data_step1 = json.dumps({"step": 1, "status": "complete", "payload": plan})
        yield f"data: {event_data_step1}\n\n"

        # --- BƯỚC 2: TẠO SQL ---
        final_sql = await backend_logic.run_step_2_sql_gen(request, plan)
        event_data_step2 = json.dumps({"step": 2, "status": "complete", "payload": final_sql})
        yield f"data: {event_data_step2}\n\n"
        
        # --- BƯỚC 3: THỰC THI ---
        result_df = await backend_logic.run_step_3_execution(final_sql)
        result_df_json = result_df.to_json(orient='split')
        event_data_step3 = json.dumps({"step": 3, "status": "complete", "payload": result_df_json})
        yield f"data: {event_data_step3}\n\n"
        
        # --- Gửi sự kiện kết thúc ---
        event_data_done = json.dumps({"step": "done"})
        yield f"data: {event_data_done}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")