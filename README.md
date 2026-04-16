# Address Intelligence System

A GitHub-ready project package for an **LLM-powered address intelligence workflow** built in Google Colab using independent notebooks.

This repository packages the final uploaded notebooks into a cleaner project structure suitable for:
- GitHub portfolio presentation
- resume linking
- interview walkthroughs
- future refactoring from notebooks into a Python package

## What this project does

The system processes employee home addresses and combines:
- retrieval over enterprise policy / typo-example knowledge base
- LLM-based address standardization
- commute estimation and confidence scoring
- eligibility decisioning
- escalation / manual review logic
- QLoRA fine-tuning for the address standardization agent
- evaluation and BigQuery logging

## Included notebooks

The uploaded set contains **4 notebooks** corresponding to stages **02-05** of the workflow:

1. `02_rag_pipeline_final_uv.ipynb`  
   Builds the retrieval pipeline with:
   - Hugging Face query rewriting
   - sentence-transformer embeddings
   - FAISS vector search
   - cross-encoder reranking

2. `03_multi_agent_workflow_uv.ipynb`  
   Runs the end-to-end multi-agent workflow:
   - Retrieval Agent
   - Address Standardization Agent
   - Commute & Confidence Agent
   - Eligibility Agent
   - Escalation Agent
   - Coordinator Agent

3. `04_qlora_finetuning_uv.ipynb`  
   Fine-tunes the address standardization model using QLoRA.

4. `05_evaluation_bigquery_logging_uv.ipynb`  
   Evaluates base vs fine-tuned model outputs and logs results to BigQuery.

> Note: Notebook `01` was not included in the uploaded files, so this repository preserves the notebooks that were provided and documents the missing stage clearly.

## Project architecture

```text
Employee Input + Office Address
        │
        ▼
Retrieval Query Rewriter (Qwen2.5-3B-Instruct)
        │
        ▼
Embedding Search (all-MiniLM-L6-v2 + FAISS)
        │
        ▼
Cross-Encoder Reranker (ms-marco-MiniLM-L-6-v2)
        │
        ▼
Address Standardization Agent
        │
        ├── corrected address
        ├── correction confidence
        └── reasoning
        ▼
Commute + Confidence Agent
        │
        ├── distance / commute estimate
        ├── combined confidence score
        └── review triggers
        ▼
Eligibility Agent
        │
        ▼
Escalation Agent
        │
        ▼
BigQuery output + evaluation artifacts
```

## Repository structure

```text
address-intelligence-github-project/
├── notebooks/
│   ├── 02_rag_pipeline_final_uv.ipynb
│   ├── 03_multi_agent_workflow_uv.ipynb
│   ├── 04_qlora_finetuning_uv.ipynb
│   └── 05_evaluation_bigquery_logging_uv.ipynb
├── src/
│   └── address_intelligence/
│       ├── __init__.py
│       ├── agents.py
│       ├── bigquery_io.py
│       ├── config.py
│       ├── evaluation.py
│       ├── finetune.py
│       ├── prompts.py
│       ├── retrieval.py
│       └── utils.py
├── scripts/
│   ├── bootstrap_repo.py
│   └── notebook_inventory.py
├── docs/
│   ├── architecture.md
│   └── resume_project_summary.md
├── data/
│   ├── raw/
│   └── processed/
├── artifacts/
│   ├── evaluation/
│   ├── logs/
│   └── models/
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Core models and components used in the notebooks

- **Base / agent model:** `Qwen/Qwen2.5-3B-Instruct`
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Reranker:** `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **Vector store:** `FAISS`
- **Fine-tuning:** `PEFT + LoRA + bitsandbytes QLoRA`
- **Storage / evaluation:** `BigQuery`
- **Tracking:** `Weights & Biases`

## Setup

### Option 1: run in Colab
Open the notebooks in order and run them individually.

### Option 2: local environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file or set environment variables before running local code:

```bash
PROJECT_ID=your-gcp-project
DATASET_ID=address_intelligence_demo
TABLE_EMPLOYEES=employee_input
TABLE_KB=kb_documents
TABLE_OUTPUT=agent_output_predictions
MAPS_API_KEY=optional
WANDB_PROJECT=address-intelligence
```

## Important notes before publishing

- Review notebook outputs and clear sensitive execution data before making the repository public.
- Replace hardcoded project identifiers if needed.
- Add your own license before open-sourcing.
- If Notebook 01 exists elsewhere, add it under `notebooks/01_...` to complete the sequence.

## Resume-friendly project summary

Built an **LLM-powered address intelligence system** that combined **RAG, reranking, multi-agent orchestration, QLoRA fine-tuning, and BigQuery-based evaluation** to standardize employee addresses, estimate commute eligibility, assign confidence scores, and route uncertain cases to manual review.

## Suggested GitHub description

`LLM-powered address intelligence system with RAG, multi-agent orchestration, QLoRA fine-tuning, and BigQuery evaluation.`

## Suggested repo topics

`llm`, `rag`, `multi-agent`, `qlora`, `peft`, `bigquery`, `faiss`, `langchain`, `transformers`, `address-standardization`, `mlops`
