FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    TEMPORAL_HOST=temporal:7233 \
    TASK_QUEUE=nasa-task-queue

CMD ["python", "worker.py"]
