# FROM selects a small Python base image
FROM python:3.12-slim

# sets /app as the working directory inside the image.
WORKDIR /app

# copies dependencies first, allowing Docker to cache that layer.
COPY app/requirements.txt .

# installs the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# copies main.py into the image.
COPY app/ .

# documents the port used by the API.
EXPOSE 8000

# starts Uvicorn and makes the API reachable outside its container by binding to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
