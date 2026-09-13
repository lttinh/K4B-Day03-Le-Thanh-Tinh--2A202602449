# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Lê Thanh Tình]  
> **Mã Sinh Viên / Mã Học viên:** [2A202602449]  
> **Chủ đề Lựa chọn:** [Trợ lý Tư vấn Sức khỏe Vinmec — Tra cứu lịch làm việc bác sĩ chuyên khoa và đặt lịch khám bệnh]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5/ 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |
| **2. Tool Interaction** | 5/ 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision** | 4/ 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |
| **4. Long Horizon Goal** | 4/ 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |
| **TỔNG ĐIỂM AGENTIC FIT** 18|20 **/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "thought": "Bệnh nhân có triệu chứng đau dạ dày muộn và ợ chua. Cần tra cứu bác sĩ thuộc chuyên khoa Tiêu hóa có lịch làm việc tại Vinmec Times City vào ngày 15/03/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_doctor_schedule",
    "arguments": {
      "specialization": "Tiêu hóa",
      "hospital_branch": "Vinmec Times City",
      "date": "2026-03-15"
    },
    "observation": {
      "status": "SUCCESS",
      "found_doctors": [
        {
          "doctor_id": "DOC-TH-002",
          "full_name": "TS.BS. Nguyễn Văn Bình",
          "specialization": "Tiêu hóa - Gan mật",
          "available_slots": ["09:00", "10:30", "14:00"]
        }
      ]
    },
    "latency_ms": 345.2
  },
  {
    "step": 2,
    "thought": "Đã tìm thấy BS. Nguyễn Văn Bình có lịch trống ca sáng 09:00 ngày 15/03/2026. Tiến hành kích hoạt tool đặt lịch khám bệnh cho bệnh nhân Lê Thanh Tình.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_medical_appointment",
    "arguments": {
      "patient_name": "Lê Thanh Tình",
      "doctor_id": "DOC-TH-002",
      "appointment_date": "2026-03-15",
      "appointment_time": "09:00",
      "symptoms": "Đau vùng thượng vị, ợ chua"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "VM-20260315-8832",
      "confirmation": "Xác nhận đặt lịch khám thành công",
      "details": {
        "patient": "Lê Thanh Tình",
        "doctor": "TS.BS. Nguyễn Văn Bình",
        "specialization": "Tiêu hóa",
        "location": "Phòng khám 302, Vinmec Times City",
        "time": "09:00 - 15/03/2026"
      }
    },
    "latency_ms": 298.6
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5/ 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 11 lượt.
- **Kết quả đẩy Repo nộp bài:** [X] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
