from langchain_huggingface import HuggingFaceEmbeddings



MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
)