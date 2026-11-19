
# Clinic Booking RAG Assistant

Issue #306 — PDF Ingestion, Qdrant and LangGraph

## Overview
This project uses RAG to answer clinic questions
based on fictional PDF documents.

## Technologies
- Python 3.14
- LangGraph
- OpenAI
- Qdrant
- PyPDF
- Docker

## Start Qdrant
docker start clinic-qdrant

For first-time setup, see the project instructions.

Dashboard: http://localhost:6333/dashboard

## Set up the API key
Create .env and add:
OPENAI_API_KEY=your-key-here

Never commit .env.

## Install dependencies
uv sync

## Ingest PDFs
uv run ingest.py

## Run the workflow
uv run clinic_rag.py

## Test Questions
1. What time does the clinic open on Friday?
2. Do you accept walk-ins?
3. How much does a blood test cost?
4. How do I cancel my appointment?
5. Do you sell car insurance?

## Test Results
Add your actual five answers here after running the code.

## Workflow
START -> retrieve -> generate/no_answer -> END
