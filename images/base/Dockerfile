FROM python:3.11-slim
ENV PYTHONPATH=/root
WORKDIR /root

RUN apt-get update

# Upgrade PIP and Install dependencies
COPY images/base/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the data
COPY data/ ./data/

# Copy the source code.
COPY src/ ./src/

EXPOSE 5000
ENTRYPOINT ["python", "src/app.py"]
