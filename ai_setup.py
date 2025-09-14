from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from vector import retriever  # your existing Chroma vector retriever

# -----------------------------
# 1️⃣ Initialize the Ollama LLM (GPU-friendly)
# -----------------------------
model = OllamaLLM(
    model="llama3:8b",
    streaming=True,
    n_gpu_layers=12   # safe for 4GB VRAM
)

# -----------------------------
# 2️⃣ Create chat prompt
# -----------------------------
human_message = HumanMessagePromptTemplate.from_template("""
You are an expert in answering questions about a pizza restaurant.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
""")
prompt = ChatPromptTemplate(messages=[human_message])

# -----------------------------
# 3️⃣ Chain prompt and model
# -----------------------------
chain = prompt | model
