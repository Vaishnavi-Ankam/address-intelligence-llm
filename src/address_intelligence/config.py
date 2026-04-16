from dataclasses import dataclass
import os


@dataclass
class ProjectConfig:
    project_id: str = os.getenv("PROJECT_ID", "")
    dataset_id: str = os.getenv("DATASET_ID", "address_intelligence_demo")
    table_employees: str = os.getenv("TABLE_EMPLOYEES", "employee_input")
    table_kb: str = os.getenv("TABLE_KB", "kb_documents")
    table_output: str = os.getenv("TABLE_OUTPUT", "agent_output_predictions")
    maps_api_key: str = os.getenv("MAPS_API_KEY", "")
    base_model_name: str = os.getenv("BASE_MODEL_NAME", "Qwen/Qwen2.5-3B-Instruct")
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    reranker_model_name: str = os.getenv("RERANKER_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")
