import time

import gradio as gr

from config import SYSTEM_PROMPT
from model import qwen_response


def analyze(message):
    if not message or not message.strip():
        return "", None, "", "", None

    start_time = time.time()
    result = qwen_response(SYSTEM_PROMPT, message)
    duration = round(time.time() - start_time, 2)

    return (
        result["summary"],
        result["sentiment"],
        result["action"],
        result["response"],
        duration,
    )


with gr.Blocks(title="Ollama Assistant") as demo:
    gr.Markdown("# Customer Inquiry Analyzer")
    gr.Markdown("Local AI assistant powered by **Qwen 2.5 7B** via Ollama + LangChain LCEL.")

    message = gr.Textbox(
        label="Customer message",
        lines=4,
        placeholder="Enter a customer inquiry...",
    )
    submit = gr.Button("Analyze", variant="primary")

    with gr.Row():
        summary = gr.Textbox(label="Summary")
        sentiment = gr.Number(label="Sentiment (0–100)", precision=0)
    action = gr.Textbox(label="Recommended action")
    response = gr.Textbox(label="Suggested response", lines=4)
    duration = gr.Number(label="Duration (seconds)", precision=2)

    submit.click(
        analyze,
        inputs=message,
        outputs=[summary, sentiment, action, response, duration],
    )
    message.submit(
        analyze,
        inputs=message,
        outputs=[summary, sentiment, action, response, duration],
    )

if __name__ == "__main__":
    demo.launch()
