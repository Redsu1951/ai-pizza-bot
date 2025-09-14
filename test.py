from langchain_ollama.llms import OllamaLLM

# Initialize model
model = OllamaLLM(model="llama3:8b", streaming=True, n_gpu_layers=12)

# Test a dummy prompt
result = model.invoke("Hello, are you running on GPU?")
print(result)
