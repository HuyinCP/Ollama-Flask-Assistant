<div align="center">

<a href="https://docs.langchain.com/oss/python/langchain/overview">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/images/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset=".github/images/logo-light.svg">
    <img alt="LangChain Logo" src=".github/images/logo-dark.svg" width="50%">
  </picture>
</a>

# Ollama Gradio Assistant

**A local AI assistant for structured customer inquiry analysis.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-F97316?logo=gradio&logoColor=white)](https://gradio.app/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Qwen_2.5-000000)](https://ollama.com/)

</div>

Ollama Gradio Assistant is a local LLM-powered app built with **Gradio**, **LangChain**, and **Ollama**. It analyzes a customer message and returns a structured summary, sentiment score, recommended action, and suggested response — all without sending prompts to an external model provider.

> [!TIP]
> This project uses `qwen2.5:7b` by default. Switch to another Ollama chat model by changing `MODEL_ID` in `config.py`.

## Quickstart

### Prerequisites

- Python 3.12
- [Ollama](https://ollama.com/) installed and running

### Install

```powershell
ollama pull qwen2.5:7b

py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

pip install gradio langchain-ollama langchain-core pydantic
```

### Run

```powershell
python app.py
```

Gradio opens a local URL in your browser (default: [http://127.0.0.1:7860](http://127.0.0.1:7860)).

To test the model pipeline without the UI:

```powershell
python llm_test.py
```

## Architecture

<div align="center">

![System Architecture](docs/diagram-export-6-30-2026-3_35_28-PM.png)

</div>

<details>
<summary>Mermaid version (renders on GitHub)</summary>

```mermaid
flowchart LR
    U[User] -->|Submit message| UI[Gradio UI]
    UI --> APP[app.py]
    APP --> CFG[System Configuration]
    APP --> CHAIN[LangChain Pipeline]

    subgraph PIPELINE[Model Pipeline]
        CHAIN --> PROMPT[PromptTemplate]
        PROMPT --> CHAT[ChatOllama]
        CHAT --> OLLAMA[Ollama Server]
        OLLAMA --> QWEN[Qwen 2.5 7B]
        QWEN --> PARSER[JsonOutputParser]
    end

    PARSER -->|Structured result| APP
    APP -->|Display fields| UI
    UI -->|Render result| U
```

</details>

### Request flow

1. The user enters a message and clicks **Analyze** in the Gradio UI.
2. `app.py` calls `qwen_response()` with the system prompt and user message.
3. `model.py` runs the LCEL pipeline:

   ```text
   PromptTemplate | ChatOllama | JsonOutputParser
   ```

4. `PromptTemplate` combines the system prompt, user message, and JSON formatting instructions.
5. `ChatOllama` sends the formatted prompt to the local `qwen2.5:7b` model.
6. `JsonOutputParser` converts the model output into a structured Python dictionary.
7. Gradio displays summary, sentiment, action, response, and processing duration.

### Response format

```json
{
  "summary": "The user needs help resetting a password.",
  "sentiment": 50,
  "action": "Provide password reset instructions.",
  "response": "Use the Forgot Password link on the sign-in page.",
  "duration": 2.31
}
```

## Project components

- **Gradio UI** — Collects messages and displays the generated response and analysis.
- **app.py** — Wires the UI to the model pipeline and adds timing metadata.
- **LangChain LCEL** — Connects prompt formatting, model inference, and output parsing.
- **Ollama** — Hosts and runs the model locally.
- **Qwen 2.5** — Generates the structured customer inquiry analysis.

## Why this project?

- **Local inference** — Prompts are processed by Ollama on your machine.
- **Structured output** — Pydantic and `JsonOutputParser` produce a predictable response shape.
- **Model flexibility** — The configured Ollama model can be replaced without changing the Gradio handler.
- **Clear separation of concerns** — UI, configuration, and model logic live in separate modules.
- **Simple development workflow** — The model pipeline can be tested independently through `llm_test.py`.

## Project structure

```text
Ollama-Gradio-Assistant/
├── app.py                 # Gradio UI and handler
├── config.py              # Model settings and system prompt
├── model.py               # LangChain pipeline and output schema
└── llm_test.py            # Standalone model test
```

## Roadmap

Planned directions to grow this assistant from a single-turn analyzer into a full retrieval-augmented, multimodal, agentic application:

- [ ] **Retrieval-Augmented Generation (RAG)** — Ground responses in a knowledge base so the assistant can answer from your own documents.
- [ ] **Vector database integration** — Store and retrieve embeddings (e.g. Chroma, FAISS, or Qdrant) to power semantic search over support content.
- [ ] **Advanced RAG** — Add retrievers, re-ranking, and citation of source passages for more accurate answers.
- [ ] **Multimodal input** — Accept images alongside text (e.g. screenshots of an error) using a multimodal Ollama model.
- [ ] **AI agents** — Let the assistant call tools (order lookup, refund processing) instead of only suggesting an action.
- [ ] **Agentic workflows with LangGraph** — Orchestrate multi-step reasoning and stateful conversations with LangChain + LangGraph.
- [ ] **Conversation memory** — Maintain multi-turn context across a chat session.

## Next Steps

Ideas to further enhance the application and your skills:

- **Implement caching** — Cache repeated queries to improve performance and reduce model calls.
- **Explore advanced LangChain features** — Add memory to maintain conversation context across turns.
- **Add more models** — Integrate other chat models (e.g. additional Ollama models or other providers).
- **Implement A/B testing** — Compare responses from different models for the same query.
- **Enhance error handling** — Add more robust error handling and structured logging.
- **Explore cloud services** — Consider integrating cloud services to expand the application's capabilities.

## Resources

- [Ollama documentation](https://docs.ollama.com/)
- [LangChain Python documentation](https://docs.langchain.com/oss/python/langchain/overview)
- [Gradio documentation](https://www.gradio.app/docs)
- [Qwen 2.5 model on Ollama](https://ollama.com/library/qwen2.5)
