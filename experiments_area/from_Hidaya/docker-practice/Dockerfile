# 1. Choose a small Python base image
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements into the image
COPY app/requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the application code
COPY app/ .

# 6. Run the API on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]