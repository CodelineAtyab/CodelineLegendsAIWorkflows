# Clinic Booking Assistant: RAG with LangGraph and Qdrant

A customer asks a question and gets an answer grounded in the clinic's own PDFs
(`sample_pdfs/`, made-up data).

```
INGEST   PDF ──► chunks ──► embeddings ──► Qdrant
ANSWER   question ──► retrieve ──► (chunks found?) ──► generate ──► answer
                                          └─ no ───► no_answer ──► polite fallback
```

## Setup

1. **Start Qdrant** (dashboard at http://localhost:6333/dashboard):

   ```
   docker compose up -d
   ```

2. **Set the API key.** Copy `.env.example` to `.env` and put your key in it. `.env` is git-ignored.

   ```
   OPENAI_API_KEY=your-key-here
   ```

3. **Ingest the PDFs** (once; it empties and refills the `clinic_docs` collection):

   ```
   uv run ingest.py
   ```

   Prints one line per PDF, e.g. `opening_hours.pdf: 2 chunks stored`.

4. **Ask questions** (runs the 6 test questions and saves the graph as `clinic_rag.png`):

   ```
   uv run clinic_rag.py
   ```

Each question prints the plain dict from `workflow.invoke(...)` with `question`, `chunks` and
`answer`, so you can check which chunks an answer was based on.

## How it works

- `ingest.py`: `load_pdf_text` → `split_into_chunks` (300 characters, 60 overlap) → `embed_texts`
  (`text-embedding-3-small`) → `store_chunks` (vector + chunk text + PDF name in Qdrant).
- `clinic_rag.py`: state `{question, chunks, answer}`. `retrieve` embeds the question and keeps the
  top 3 chunks scoring at least `MIN_SCORE`. The decider sends the flow to `generate`
  (`gpt-4.1-mini`, told to answer only from the chunks) or to `no_answer`.
- The question is embedded with the same `embed_texts` function that embeds the chunks, so both
  always use the same model.

## Test questions and answers

Run `uv run clinic_rag.py` and paste the answers you got here (one is deliberately not in the PDFs):

| # | Question | Answer |
|---|----------|--------|
| 1 | What time do you open on Friday? | _paste result_ |
| 2 | Do you accept walk-ins? | _paste result_ |
| 3 | How do I cancel an appointment? | _paste result_ |
| 4 | How much is a dental check-up? | _paste result_ |
| 5 | Is there a fee if I cancel late? | _paste result_ |
| 6 | Do you sell car insurance? (not in the PDFs) | _paste result_ |
