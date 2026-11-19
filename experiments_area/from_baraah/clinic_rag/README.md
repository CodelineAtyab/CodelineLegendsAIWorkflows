
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

### Test 1: Clinic Opening Hours
Question: What time does the clinic open on Friday?

Answer: The clinic opens at 9:00 AM on Friday.

### Test 2: Walk-in Appointments
Question: Do you accept walk-ins?

Answer: Yes, the clinic accepts walk-in patients only when a doctor is available. However, an appointment is recommended.

### Test 3: Blood Test Price
Question: How much does a blood test cost?

Answer: A blood test at Owlgent Sample Clinic costs 8 OMR.

### Test 4: Appointment Cancellation
Question: How do I cancel my appointment?

Answer: To cancel your appointment, you should contact reception at least 24 hours before the scheduled appointment time.

### Test 5: Unrelated Question
Question: Do you sell car insurance?

Answer: Sorry, I could not find this information in our clinic documents. Please contact the clinic for assistance.


## Workflow
START -> retrieve -> generate/no_answer -> END
