from model import qwen_response
from config import SYSTEM_PROMPT


def call_model(system_prompt, user_prompt):
    result = qwen_response(system_prompt, user_prompt)  # result là dict (đã được JsonOutputParser parse)
    print("Summary  :", result["summary"])    # Tóm tắt câu hỏi
    print("Sentiment:", result["sentiment"])  # Điểm cảm xúc 0-100
    print("Action   :", result["action"])     # Hành động đề xuất
    print("Response :", result["response"])   # Câu trả lời gợi ý


# Gọi thử: tham số 1 = system prompt từ config, tham số 2 = câu hỏi của user
call_model(
    SYSTEM_PROMPT,
    "What is the capital of Canada? Tell me a cool fact about it as well",
)
