TOOLS_SCHEMA = [
    {
        "name": "search_doctor_schedule",
        "description": "Tra cứu danh sách bác sĩ và lịch trực trống theo chuyên khoa, chi nhánh bệnh viện và ngày khám.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "specialization": {
                    "type": "STRING",
                    "description": "Tên chuyên khoa (ví dụ: Tiêu hóa, Tim mạch, Nhi, Cơ xương khớp)"
                },
                "hospital_branch": {
                    "type": "STRING",
                    "description": "Chi nhánh Vinmec (ví dụ: Vinmec Times City, Vinmec Central Park)"
                },
                "date": {
                    "type": "STRING",
                    "description": "Ngày khám định dạng YYYY-MM-DD"
                }
            },
            "required": ["specialization"]
        }
    },
    {
        "name": "book_medical_appointment",
        "description": "Đặt lịch khám bệnh với bác sĩ cụ thể tại bệnh viện Vinmec.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "patient_name": {"type": "STRING", "description": "Họ và tên bệnh nhân"},
                "doctor_id": {"type": "STRING", "description": "Mã định danh bác sĩ (ví dụ: DOC-TH-002)"},
                "appointment_date": {"type": "STRING", "description": "Ngày khám (YYYY-MM-DD)"},
                "appointment_time": {"type": "STRING", "description": "Giờ khám (ví dụ: 09:00)"},
                "symptoms": {"type": "STRING", "description": "Mô tả ngắn triệu chứng bệnh"}
            },
            "required": ["patient_name", "doctor_id", "appointment_date", "appointment_time"]
        }
    }
]