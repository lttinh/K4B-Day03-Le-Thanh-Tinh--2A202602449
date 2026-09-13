import sys
import os
import json
import streamlit as st

# Thêm đường dẫn thư mục gốc vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers import get_llm_provider
from mcp_server import MCPAcademicServer
from prompts import REACT_AGENT_SYSTEM_PROMPT, MAX_ITERATIONS

# Thiết lập trang Streamlit
st.set_page_config(page_title="Vinmec ReAct Agent Demo", page_icon="🏥", layout="wide")

st.title("🏥 VINMEC AI AGENT DEMO")
st.caption("Hệ thống trợ lý y tế thông minh ReAct Agent kết nối MCP Server")

# Khởi tạo Provider & MCP Server trong Session State
@st.cache_resource
def init_agent():
    provider = get_llm_provider()
    mcp_server = MCPAcademicServer()
    return provider, mcp_server

provider, mcp_server = init_agent()

# Khởi tạo lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Tôi có thể giúp bạn tra cứu thông tin bác sĩ, lịch khám và đặt lịch tại Vinmec."}
    ]

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập câu hỏi của người dùng
if user_input := st.chat_input("Nhập câu hỏi hoặc yêu cầu đặt lịch..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Xử lý ReAct Agent Loop
    with st.chat_message("assistant"):
        tools_list = mcp_server.list_tools()
        step = 0
        final_answer = ""

        with st.spinner("🤖 Agent đang suy luận và xử lý..."):
            while step < MAX_ITERATIONS:
                step += 1
                
                # Gọi LLM
                llm_response = provider.generate_with_tools(user_input, tools_list, system_prompt=REACT_AGENT_SYSTEM_PROMPT)
                thought = llm_response.get("thought", "Đang suy luận...")
                
                # Hiển thị Thought dạng Expander cho trực quan
                with st.expander(f"🧠 Step {step}: Suy luận (Thought)", expanded=True):
                    st.write(thought)

                # Trường hợp 1: LLM trả lời trực tiếp bằng văn bản
                if llm_response.get("type") == "text":
                    final_answer = llm_response.get("content", "")
                    break
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                    break

                # Trường hợp 2: LLM đề xuất gọi Tool
                elif llm_response.get("type") == "tool_call":
                    tool_name = llm_response.get("tool_name")
                    arguments = llm_response.get("arguments", {})

                    st.info(f"🛠️ **Action Proposed:** `{tool_name}` với tham số: `{json.dumps(arguments, ensure_ascii=False)}`")

                    # Gọi Tool qua MCP Server
                    mcp_result = mcp_server.call_tool(tool_name, arguments)
                    obs_data = mcp_result.get("result", {})

                    st.success(f"👁️ **Observation:** `{json.dumps(obs_data, ensure_ascii=False)}`")

                    # Định dạng Final Answer dựa trên dữ liệu trả về
                    if obs_data.get("status") == "SUCCESS":
                        if "data" in obs_data:
                            d = obs_data["data"]
                            if "doctor_name" in d:
                                slots = ", ".join(d.get("available_slots", []))
                                final_answer = f"Bác sĩ **{d.get('doctor_name')}** (Mã: `{d.get('doctor_id')}`) thuộc khoa **{d.get('specialty')}** tại **{d.get('location')}**. Lịch trống ngày {d.get('date')}: **{slots}**."
                            else:
                                final_answer = f"Thành công: {json.dumps(d, ensure_ascii=False)}"
                        elif "message" in obs_data:
                            final_answer = obs_data["message"]
                        else:
                            final_answer = json.dumps(obs_data, ensure_ascii=False)
                    elif obs_data.get("status") == "NOT_FOUND":
                        final_answer = obs_data.get("message", "Không tìm thấy dữ liệu yêu cầu.")
                    else:
                        final_answer = f"Kết quả: {json.dumps(obs_data, ensure_ascii=False)}"
                    break

        # Hiển thị câu trả lời cuối cùng
        st.markdown(f"### 🏁 Kết quả:\n{final_answer}")
        st.session_state.messages.append({"role": "assistant", "content": final_answer})