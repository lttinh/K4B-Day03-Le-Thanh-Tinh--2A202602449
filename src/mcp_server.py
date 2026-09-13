"""
MCP Server quản lý Tools cho ReAct Agent (Bệnh viện Vinmec).
"""

class MCPAcademicServer:
    def __init__(self):
        self.server_name = "Vinmec Medical MCP Server"

    def list_tools(self) -> list:
        """Khai báo các Tool Schemas cho LLM phát hiện và gọi công cụ."""
        return [
            {
                "name": "search_doctor_schedule",
                "description": "Tra cứu lịch làm việc của bác sĩ theo chuyên khoa, tên bác sĩ hoặc mã bác sĩ tại chi nhánh Vinmec.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "specialty": {
                            "type": "string",
                            "description": "Tên chuyên khoa (ví dụ: Tiêu hóa, Tim mạch, Ung bướu)."
                        },
                        "doctor_id": {
                            "type": "string",
                            "description": "Mã số bác sĩ (ví dụ: DOC-TH-002, DOC-9999999)."
                        },
                        "date": {
                            "type": "string",
                            "description": "Ngày cần tra cứu lịch làm việc (định dạng YYYY-MM-DD hoặc DD/MM/YYYY)."
                        },
                        "location": {
                            "type": "string",
                            "description": "Chi nhánh bệnh viện Vinmec (ví dụ: Vinmec Times City)."
                        }
                    },
                    "required": ["date"]
                }
            },
            {
                "name": "book_medical_appointment",
                "description": "Đặt lịch hẹn khám bệnh với bác sĩ chuyên khoa tại Vinmec.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_name": {
                            "type": "string",
                            "description": "Họ và tên bệnh nhân."
                        },
                        "doctor_id": {
                            "type": "string",
                            "description": "Mã bác sĩ hoặc tên bác sĩ cần khám."
                        },
                        "date": {
                            "type": "string",
                            "description": "Ngày hẹn khám."
                        },
                        "time_slot": {
                            "type": "string",
                            "description": "Khung giờ hẹn khám (ví dụ: 09:00, ca sáng)."
                        }
                    },
                    "required": ["patient_name", "date"]
                }
            }
        ]

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Thực thi Tool và trả về kết quả Observation cho ReAct Agent."""
        if tool_name == "search_doctor_schedule":
            doctor_id = arguments.get("doctor_id", "")
            specialty = arguments.get("specialty", "")
            date = arguments.get("date", "")

            # Xử lý Edge Case: Mã bác sĩ không tồn tại
            if doctor_id == "DOC-9999999":
                return {
                    "result": {
                        "status": "NOT_FOUND",
                        "message": f"Không tìm thấy bác sĩ có mã '{doctor_id}' trong hệ thống Vinmec."
                    }
                }

            # Kết quả tra cứu bác sĩ hợp lệ
            return {
                "result": {
                    "status": "SUCCESS",
                    "data": {
                        "doctor_name": "TS.BS. Nguyễn Văn Bình",
                        "doctor_id": doctor_id or "DOC-TH-002",
                        "specialty": specialty or "Tiêu hóa",
                        "date": date,
                        "available_slots": ["08:30", "09:00", "10:30", "14:00"],
                        "location": "Vinmec Times City"
                    }
                }
            }

        elif tool_name == "book_medical_appointment":
            patient_name = arguments.get("patient_name", "")
            doctor_id = arguments.get("doctor_id", "")
            date = arguments.get("date", "")
            time_slot = arguments.get("time_slot", "09:00")

            return {
                "result": {
                    "status": "SUCCESS",
                    "message": f"Đặt lịch thành công cho bệnh nhân {patient_name} với bác sĩ {doctor_id} vào {time_slot} ngày {date}."
                }
            }

        return {
            "result": {
                "status": "NOT_FOUND",
                "message": f"Không tìm thấy công cụ tên '{tool_name}'."
            }
        }