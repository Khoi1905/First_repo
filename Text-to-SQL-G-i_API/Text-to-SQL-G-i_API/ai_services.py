# core/ai_services.py
import requests
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLM_Service:
    def __init__(self, service_type: str = "ollama", model_name: str = "llama3"):        
        self.service_type = service_type
        self.model_name = model_name
        
        if self.service_type == "ollama":
            self.endpoint = "http://localhost:11434/api/generate"
            print(f"Đã cấu hình dịch vụ LLM để sử dụng Ollama với mô hình: {self.model_name}")
        
        elif self.service_type == "google":
            # self.api_key = os.getenv("GOOGLE_API_KEY")
            self.api_key = "AIzaSyDTSXAusP4MmCJ51Hv6pZXpE973v6sMEoc"
            if not self.api_key:
                raise ValueError("Vui lòng đặt biến môi trường GOOGLE_API_KEY trong file .env")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ Đã cấu hình dịch vụ LLM để sử dụng Google với mô hình: {self.model_name}")
        else:
            raise ValueError(f"Dịch vụ '{self.service_type}' chưa được hỗ trợ!")

    def _call_ollama(self, prompt: str) -> str:        
        try:
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.endpoint, json=data)
            response.raise_for_status()
            return json.loads(response.text)["response"].strip()
        except Exception as e:
            print(f"Lỗi khi gọi mô hình Ollama: {e}")
            return f"Lỗi: {e}"
        
    def _call_google(self, prompt: str) -> str:        
        try:            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f" Lỗi khi gọi API Google Gemini: {e}")
            return f"Lỗi: {e}"

    def generate(self, prompt: str) -> str:        
        if self.service_type == "ollama":
            return self._call_ollama(prompt)
        elif self.service_type == "google":
            return self._call_google(prompt)
        
        return "Lỗi: Không có dịch vụ nào được chọn."