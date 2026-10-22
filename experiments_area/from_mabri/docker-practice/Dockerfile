# The base image: a minimal Linux with Python. slim keeps it around 150 MB instead of about 1 GB
From python:3.12-slim

# Creates /app and cds into it. Every later command runs from there
WORKDIR /app

# Copies only the dependency list. The path is relative to the build context, which is why it starts with "app/"
COPY app/requirements.txt .

# Installs deps at build time and stores them in an image layer. --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copies the rest of the code. The path is relative to the build context, which is why it starts with "app/" 
COPY app/ .

# CMD runs when the container starts. 0.0.0.0 listens on all interfaces, which is needed because 127.0.0.1 inside a container isn't reachable from your host. EXPOSE is documentation only
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]