from langchain_ollama import ChatOllama                      # Lớp LangChain để nói chuyện với Ollama
from langchain_core.prompts import PromptTemplate            # Tạo mẫu prompt có chỗ trống {..} để điền
from langchain_core.output_parsers import JsonOutputParser   # Ép kết quả model về dạng JSON
from pydantic import BaseModel, Field                        # Khai báo "khuôn" dữ liệu mong muốn
from config import OLLAMA_HOST, MODEL_ID, PARAMETERS          # Cấu hình: địa chỉ Ollama, tên model, tham số


def initialize_model(model_id):
    """Khởi tạo và trả về một model Ollama theo model_id."""
    return ChatOllama(
        model=model_id,        # Tên model "qwen2.5:7b"
        base_url=OLLAMA_HOST,  # Địa chỉ server Ollama, http://localhost:11434
        **PARAMETERS,          # Trải dict thành các tham số: temperature, num_predict, top_p...
    )


qwen_llm = initialize_model(MODEL_ID)  # Tạo sẵn 1 model dùng chung cho cả file


# ---- Khuôn dữ liệu đầu ra mong muốn (model phải trả JSON đúng các field này) ----
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")                     # Tóm tắt câu hỏi của user
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")  # Điểm cảm xúc 0-100
    action: str = Field(description="Recommended next action to handle the user's request")  # Hành động nên làm tiếp theo
    response: str = Field(description="Suggested response to the user")                    # Câu trả lời gợi ý cho user


# Parser đọc text model trả về và parse thành JSON theo khuôn AIResponse ở trên
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# ---- Mẫu prompt: điền system/user/format vào các chỗ trống {..} ----
qwen_template = PromptTemplate(
    template='''<|im_start|>system
{system_prompt}
{format_prompt}<|im_end|>
<|im_start|>user
{user_prompt}<|im_end|>
<|im_start|>assistant
''',
    input_variables=["system_prompt", "user_prompt", "format_prompt"],  # 3 chỗ trống cần điền khi invoke
)


def get_ai_response(model, template, system_prompt, user_prompt):
    # Nối 3 bước thành 1 luồng: điền prompt -> gọi model -> parse JSON
    chain = template | model | json_parser

    # invoke: đưa dữ liệu vào luồng và chạy.
    # format_prompt = hướng dẫn "hãy trả JSON đúng các field" do parser tự sinh ra.
    return chain.invoke({
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "format_prompt": json_parser.get_format_instructions(),
    })


def qwen_response(system_prompt, user_prompt):
    # Hàm tiện dụng: gọi sẵn với model qwen và template qwen, trả về dict JSON
    return get_ai_response(qwen_llm, qwen_template, system_prompt, user_prompt)
